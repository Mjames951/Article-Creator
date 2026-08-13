from django.urls import path
from . import views
from . import adminviews
from blog import views as articleviews

urlpatterns = [
    path('', views.index, name='index'),
    path('library/', articleviews.articleList, name='articlelist'),
    path('library/<category>/', articleviews.articleList, name='articlecategory'),
    path('about/', views.about, name='about'),
    path('store/', views.store, name='storeall'),
    path('store/<category>/', views.store, name='store'),
    path('view/<productid>/', views.product, name='product'),

    path('store/add/<productid>/', views.addCart, name='addcart'),
    path('store/add/<productid>/<checkout>/', views.addCart, name='addcartcheckout'),

    path('store/remove/<productid>/', views.removeCart, name='removecart'),
    path('store/remove/<productid>/<checkout>/', views.removeCart, name='removecartcheckout'),

    path('checkout', views.checkout, name='checkout'),

    path('checkout/emptycart/', views.emptyCart, name='emptycart'),
    path('checkout/<errorMessage>/', views.checkout, name='checkoutError'),

    path('checkout/cancel/<orderID>/', views.cancelOrder, name='cancelorder'),
    path('checkout/<orderID>/<client_secret>/', views.checkoutfr, name='checkoutfr'),

    path('super/secret/admin/', adminviews.admin, name='admin'),

    path('super/secret/fullfill/<orderID>/', adminviews.fulfillOrder, name='fulfillorder'),

    path('crud/<modelname>/', adminviews.CRUD, name='addmodel'),
    path('crud/<modelname>/<id>/', adminviews.CRUD, name='editmodel'),
    path('crud/<modelname>/None/<parentid>/', adminviews.CRUD, name='addmodelparent'),
    path('crud/<modelname>/<id>/delete/', adminviews.DELETE, name='deletemodel'),
    path('crud/<modelname>/<id>/<parentid>/', adminviews.CRUD, name='editmodelparent'),

    path('super/secret/inpersonorder/', adminviews.inpersonOrder, name='inpersonorder'),


    path('success/<orderID>/<successString>/', views.paymentSuccess, name='paymentsuccess'),
]