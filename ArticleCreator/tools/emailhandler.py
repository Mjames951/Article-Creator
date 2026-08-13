from django.core.mail import send_mail
from django.conf import settings

sender = settings.EMAIL_HOST_USER

def testMail():
    send_mail('hello', 'wuddup dude', sender, ['aspc.james2@gmail.com'])

def orderSuccess(order):
    orderMessage=''
    emailComment=''
    for item in order.cart.items.all():
        orderMessage+=f"{item}"
        if item.product.emailComment:
            emailComment+=f'{item.product.name}: {item.product.emailComment}'

    subject = 'SPP Order Confirmation'
    message = f'''
Thank you so much for your order!
You're supporting small business, small artists, and regular people.
You must be really cool!

{emailComment}

Order Details
-----
{ orderMessage }--------
If you ordered physical merchandise then expect a shipment confirmation email in the coming days.


Planet Plum Records LLC
            '''
    receiver=[order.email,]
    send_mail(
        subject,
        message,
        sender,
        receiver,
        fail_silently=False
    )

def orderShipped(order):
    orderMessage=''
    for item in order.cart.items.all():
        orderMessage+=f"{item}"

    subject = 'SPP Shipment Confirmation'
    message = f'''
Your order has been shipped!!
Feel free to contact us if it doesn't show up within a week.

Order Details
-----
{ orderMessage }--------


Planet Plum Records LLC
            '''
    receiver=[order.email,]
    send_mail(
        subject,
        message,
        sender,
        receiver,
        fail_silently=False
    )