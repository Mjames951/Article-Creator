from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .tools.imagehandler import addImage
from .models import *
from .forms import *
from .tools import emailhandler

from blog.models import Article, Section, Author
from blog.models import Category as ArticleCategory
from blog.forms import ArticleStarterForm, ArticleForm, AuthorForm, ArticleCategoryForm 

Models = {
    "product": Product,
    'category': Category,
    "subproduct": Product,
    'shipping': Shipping,
    'article': Article,
    'articlesection': Section,
    'author': Author,
    'bubble': Bubble,
    'articlecategory': ArticleCategory,
    'todosection': PlumTodoSection,
    'todo': PlumTodo
}

Forms = {
    "product": ProductForm,
    'category': CategoryForm,
    'subproduct': SubProductForm,
    'shipping': ShippingForm,
    'article': ArticleStarterForm,
    'articlesection': ArticleForm,
    'author': AuthorForm,
    'bubble': BubbleForm,
    'articlecategory': ArticleCategoryForm,
    'todosection': TodoSectionForm,
    'todo': TodoForm
}

@login_required
def admin(request):
    if not request.user.is_admin(): return redirect("index")
    products = Product.objects.filter(parent=None)
    categories = Category.objects.all()
    shipping = Shipping.objects.all()
    unpaidOrders = Order.objects.filter(paid=False)
    orders = Order.objects.filter(paid=True, fulfilled=False)
    
    return render(request, "admin/admin.html", {
        'bubbles': Bubble.objects.all().order_by('order'),
        "products": products,
        'categories': categories,
        'shipping': shipping,
        'orders': orders,
        'allorders': Order.objects.all().order_by('paid'),
        'authors': Author.objects.all(),
        'articlecategories': ArticleCategory.objects.all(),
        'todosections': PlumTodoSection.objects.all(),
    })

@login_required
def CRUD(request, modelname, id=None, parentid=None):
    if not request.user.is_admin(): return redirect("index")
    if not modelname in Models: return redirect("index")
    if id: 
        model = Models[modelname]
        model = get_object_or_404(model, id=id)
    else:
        model = None

    if request.method == "POST":
        form = Forms[modelname](request.POST, request.FILES, instance=model)
        if form.is_valid():
            try:
                if request.FILES['image']:
                    model = addImage(form, modelInstance=model)
                    if not model: return redirect("index")
                    model.save()
                else:
                    model = form.save(commit=False)
            except:
                model = form.save(commit=False)

            if parentid:
                match modelname:
                    case 'subproduct':
                        parent = get_object_or_404(Product, id=parentid)
                        model.parent = parent
                        model.price = parent.price
                        model.shipping = parent.shipping
                        print(model.shipping)
                    case 'todo':
                        model.section = get_object_or_404(PlumTodoSection, id=parentid)
                

            model.save()

            match modelname:
                case 'product':
                    categories = form.cleaned_data['categories']
                    model.categories.set(categories)

            return redirect(model.get_absolute_url())
            
    else: form = Forms[modelname](instance=model)
    return render(request, "admin/form.html", {
        "form": form,
        "model": modelname,
    })

def DELETE(request, modelname, id):
    if not request.user.is_admin() or not modelname in Models: return redirect("index")
    model = Models[modelname]
    model = get_object_or_404(model, id=id)
    try:
        if model.image:
            model.image.delete()
    except: pass
    model.delete()
    return redirect(adminURL)


def fulfillOrder(request, orderID):
    if not request.user.is_admin(): return redirect("index")
    order = get_object_or_404(Order, id=orderID)
    order.fulfilled=True
    order.save()
    emailhandler.orderShipped(order)
    return redirect("admin")

def inpersonOrder(request):
    if not request.user.is_admin(): return redirect("index")
    if request.method == 'POST':
        form = InPersonOrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quantity = data['quantity']
            email = data['email']
            name = data['name']
            product = data['product']
            cart = Cart()
            cart.save()
            cartitem = CartItem(product=product, cart=cart, quantity=quantity)
            cartitem.save()
            order = Order(
                cart=cart, 
                successString='Plum', 
                email=email, 
                name=name,
                paid=True,
                fulfilled=True
                )
            order.save()
            return redirect('admin')
    form = InPersonOrderForm()
    return render(request, 'admin/form.html', {
        'form': form
    })

