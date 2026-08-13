from django.contrib.sitemaps import Sitemap
from ArticleCreator.models import Article
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 1
    changefreq = 'monthly'
    
    def items(self):
        return ['index', 'articlelist', 'about']
    def location(self, item):
        return reverse(item)
    
class ArticleSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Article.objects.filter(published=True)