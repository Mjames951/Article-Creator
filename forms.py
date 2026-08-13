from django import forms
from .models import *

class TodoSectionForm(forms.ModelForm):
    class Meta:
        model = PlumTodoSection
        fields = ['name']

class TodoForm(forms.ModelForm):
    class Meta:
        model = PlumTodo
        fields = ['name', 'description']

class BubbleForm(forms.ModelForm):
    class Meta:
        model = Bubble
        fields = ['name',  'link', 'linkdesc', 'image', 'description', 'embed', 'order']
        widgets = {
            'description': forms.Textarea(),
            'embed': forms.TextInput(),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'categories', 'price', 'image', 'description', 'quantity', 'shipping', 'emailComment', 'published']
        widgets = {
                'categories': forms.CheckboxSelectMultiple(),
            }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class AddressForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        fields = [ 'line1', 'city', 'state', 'zipcode', 'country']
        labels = {
            'line1': 'Shipping Address'
        }

class SubProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'image', 'description']

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['name', 'price', 'additionalShipping']
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email']

class InPersonOrderForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()
    email = forms.EmailField()
    name = forms.CharField(max_length=100)