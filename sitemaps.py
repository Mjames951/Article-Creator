from django.contrib.sitemaps import Sitemap
from shop.models import Product
from blog.models import Article
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 1
    changefreq = 'monthly'
    
    def items(self):
        return ['index', 'storeall', 'articlelist', 'about']
    def location(self, item):
        return reverse(item)
    
class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Product.objects.filter(parent=None, published=True)
    
class ArticleSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Article.objects.filter(published=True)