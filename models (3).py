from django.db import models
from django.urls import reverse_lazy

adminURL = reverse_lazy('admin')

class PlumTodoSection(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return adminURL

class PlumTodo(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    section = models.ForeignKey(PlumTodoSection, on_delete=models.CASCADE, related_name='todos')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return adminURL

class Bubble(models.Model):
    name = models.CharField(max_length=256)
    link = models.URLField(null=True, blank=True)
    linkdesc = models.CharField(max_length=32, null=True, blank=True)
    image = models.ImageField(upload_to='bubbles/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    embed = models.TextField(null=True, blank=True)
    order = models.SmallIntegerField()
    def get_absolute_url(self):
        return adminURL
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        try:
            this = Bubble.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return adminURL
    
class Shipping(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    additionalShipping = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return f"{self.name}: {self.price}"
    def get_absolute_url(self):
        return adminURL

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    quantity = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='productimages/', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products')
    shipping = models.ForeignKey(Shipping, on_delete=models.RESTRICT, related_name='products', null=True, blank=True)
    emailComment = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subs')
    created_at = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} : ${self.price}"
    def save(self, *args, **kwargs):
        try:
            this = Product.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(Product, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse_lazy('product', args=[self.id])
    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return self.parent.image.url
    def get_name(self):
        if self.parent:
            return f"{self.parent.name}\n[{self.name}]"
        else:
            return self.name

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)
    def price(self):
        return self.quantity * self.product.price
    def __str__(self):
        return f" - {self.product.name} (x{self.quantity})\n"

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT)
    successString = models.CharField()
    email = models.EmailField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)
    checkoutID = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f'FULFILLED: {self.fulfilled} PAID: {self.paid} ...created:{self.created_at}.'
    
class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='address')
    line1 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    country = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.line1} {self.city}, {self.state}, {self.country}. {self.zipcode}"