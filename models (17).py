from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

adminURL = reverse_lazy('admin')

class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='authorimgs/', null=True, blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return adminURL
    def save(self, *args, **kwargs):
        try:
            this = Author.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)
    
class Category(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return adminURL

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='articleheaderimages/', blank=True, null=True)
    caption = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article', args=[self.slug])
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        try:
            this = Article.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

class Section(models.Model):
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articleImages/', blank=True, null=True)
    caption = models.CharField(max_length=256, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='sections')
    order = models.IntegerField(null=True)
    def save(self, *args, **kwargs):
        try:
            this = Section.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)


