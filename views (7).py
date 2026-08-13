from django.shortcuts import render
import stripe
from .forms import *
from .models import *
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
from .tools import emailhandler
stripe.api_key = settings.STRIPE_KEY

def index(request):
    return render(request, 'index.html', {
        'bubbles': Bubble.objects.all().order_by('order')
    })

def about(request):
    return render(request, 'about.html', {})

def store(request, category=None):
    expiredOrders()
    if category:
        category = Category.objects.get(name=category)
        products=category.products.filter(parent=None, published=True)
    else:
        products = Product.objects.filter(parent=None, published=True)
    categories = Category.objects.all()
    return render(request, 'shop/store.html', {
        'products': products,
        'categories': categories,
        'category': category
    })

def product(request, productid):
    product = get_object_or_404(Product, id=productid)
    cart_id = request.session.get('cart_id')
    item = None
    print('LOOKING')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        print('cart found')
        for cartitem in cart.items.all():
            print(cartitem, product)
            if product == cartitem.product:
                item = cartitem
            print(f"item {item}")
    if product.parent or product.subs.all():
        print('sun')
        if not product.parent:
            product = product.subs.all()[0]
            try:item=cart.items.get(product=product)
            except:pass
            print(item)
        return render(request, 'shop/subsproduct.html', {
            'product': product,
            'item': item,
        })
    else: 
        return render(request, 'shop/product.html', {
            'product': product,
            'item': item,
        })


def addCart(request, productid, checkout=False):
    expiredCarts()
    product = get_object_or_404(Product, id=productid)
    cart_id = request.session.get('cart_id')
    print(cart_id)
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart, cartcreated = Cart.objects.get_or_create(id=cart_id)

    cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cartItem.quantity += 1

    if product.quantity < cartItem.quantity:
        if cartItem.quantity<=1:
            cartItem.delete()
        else:
            cartItem.quantity -= 1
    cartItem.save()
    if checkout:
        return redirect('checkout')
    return redirect(product.get_absolute_url())

def removeCart(request, productid, checkout=False):
    cart_item = get_object_or_404(CartItem, id=productid)
    cart_item.quantity = cart_item.quantity - 1
    cart_item.save()
    if cart_item.quantity == 0:
        cart_item.delete()
    if checkout:
        return redirect('checkout')
    else:
        return redirect(cart_item.product.get_absolute_url())

def cart(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return render(request, 'shop/form.html', {'cart': None, 'total_price': 0})

    cart = get_object_or_404(Cart, id=cart_id)
    total_price = sum(item.total_price() for item in cart.cartitem_set.all())

    return render(request, 'shopform.html', {'cart': cart, 'total_price': total_price})

def emptyCart(request):
    cartID = request.session.get('cart_id')
    if cartID:
        print("HOTHEOHO")
        cart = Cart.objects.get(id=cartID)
        for item in cart.items.all():
            item.delete()
    return redirect('checkout')

def successfulOrder(request, orderid, string):
    pass
    #compare the string given to the string stored in the order

#checkout stuff below

def calcShipping(cart):
    baseShipping=None
    totalShipping=0
    for item in cart.items.all():
        product = item.product
        if product.shipping:
            if baseShipping == None:
                baseShipping = product.shipping
            elif product.shipping.price > baseShipping.price:
                totalShipping+=baseShipping.additionalShipping
                baseShipping=product.shipping
            else:
                totalShipping+=product.shipping.additionalShipping
            if item.quantity>1: totalShipping+=(item.quantity-1)*product.shipping.additionalShipping
    if baseShipping: totalShipping+=baseShipping.price
    return totalShipping

def destroyOrder(order):
    for item in order.cart.items.all():
        product = item.product
        product.quantity+=item.quantity
        product.save()
    order.delete()

def expiredOrders():
    orders = Order.objects.filter(paid=False, created_at__lt=timezone.now() - timedelta(hours=1))
    for order in orders:
        destroyOrder(order)

def expiredCarts():
    carts = Cart.objects.filter(order=None, created_at__lt=timezone.now() - timedelta(days=1))
    for cart in carts:
        cart.delete()
def validateCartQuantities(cart):
    valid=True
    #check that the order quantities are valid
    for item in cart.items.all():
        product = item.product
        if product.quantity < item.quantity:
            if product.quantity==0:
                item.delete()
            else:
                item.quantity=product.quantity
                item.save()
            valid=False
    return valid

def cancelOrder(request, orderID):
    order=get_object_or_404(Order, id=orderID)
    destroyOrder(order)
    return redirect('checkout')

def checkoutfr(request, orderID, client_secret):
    return render(request, 'shop/checkout.html', {
        'client_secret': client_secret,
        'orderID': orderID,
    })


def checkout(request, errorMessage=False):
    #getting the cart
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return render(request, 'shop/form.html', {'cart': None, 'total_price': 0})
    cart = get_object_or_404(Cart, id=cart_id)

    # checkout fr!
    if request.method == 'POST':
        orderform = OrderForm(request.POST, prefix='ord')
        if not orderform.is_valid():
            return redirect('checkout')
        #remove expired orders
        expiredOrders()
        #check that the order quantities are valid
        if not validateCartQuantities(cart):
            return redirect('checkoutError', errorMessage=True)
        #create the Order
        order = Order(
            cart = cart, 
            successString=get_random_string(length=32),
            name=orderform.cleaned_data['name'],
            email=orderform.cleaned_data['email'],
        )
        order.save()
        #subtract from actual product quantity
        for item in order.cart.items.all():
            product=item.product
            product.quantity-=item.quantity
            product.save()

        #get their address if they put it
        addressForm = AddressForm(request.POST, prefix='add')
        if addressForm.is_valid():
            print("pooping basll")
            data=addressForm.cleaned_data
            address=OrderAddress(
                line1=data['line1'],
                city=data['city'],
                state=data['state'],
                zipcode=data['zipcode'],
                country=['country'],
            )
            address.order=order
            address.save()
            print(address)

        #create the STRIPE checkout order stuff
        items = []
        total = 0
        for item in cart.items.all():
            product = item.product
            #products pricing
            items.append({
                "price_data": {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.get_name(),
                        'images': [request.build_absolute_uri(product.get_image_url)],
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': item.quantity,
            })
            total+=product.price*item.quantity
        #get shipping total
        totalShipping=calcShipping(cart)
        if totalShipping: 
            items.append({
                    "price_data": {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'shipping',
                        },
                        'unit_amount': int(totalShipping * 100),
                    },
                    'quantity': 1,
                })
            total+=totalShipping

        session = stripe.checkout.Session.create(
            line_items=items,
            customer_email=order.email,
            mode="payment",
            ui_mode='embedded',
            return_url=f'https://planetplum.net/success/{order.id}/{order.successString}',
        )

        order.checkoutID = session['id']
        order.save()
        print('okay heres where we check shit out')
        print(order.successString)
        print(f'127.0.0.1:8000/success/{order.id}/{order.successString}/')
        if totalShipping:
            print(order.address.all())
        for item in cart.items.all():
            print(item)
        return redirect('checkoutfr', orderID=order.id, client_secret=session['client_secret'])
        return render(request, 'shop/checkout.html', {
            'client_secret': session["client_secret"],
            'order': order,
        })
    #just viewing cart
    else:
        orderForm = OrderForm(prefix='ord')
        total = 0
        for item in cart.items.all():
            product = item.product
            total+=product.price*item.quantity
        totalShipping = calcShipping(cart)
        total+=totalShipping
        if totalShipping > 0:
            addressForm = AddressForm(prefix='add', initial={'country': 'United States'})
        else: addressForm = None
        return render(request, 'shop/form.html', {
            'orderform': orderForm,
            'addressform': addressForm,
            'cart': cart,
            'total': total,
            'shipping': totalShipping,
            'errorMessage': errorMessage,
        })

def paymentSuccess(request, orderID, successString):
    order = get_object_or_404(Order, id=orderID)
    if order.successString == successString and order.paid == False:
        try:
            del request.session['cart_id']
        except:
            pass
        order.paid=True
        if not order.address.all():
            order.fulfilled = True
        order.save()
        try:
            emailhandler.orderSuccess(order)
        except:
            return render(request, 'shop/failedemail.html', {})
    return render(request, 'shop/successfulpayment.html', {'order': order})
    
        
