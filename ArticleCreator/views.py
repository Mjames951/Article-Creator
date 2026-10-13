from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from .tools.imagehandler import addImage
import markdown
from django.utils import timezone

MarkDown = markdown.Markdown(extensions=["fenced_code"])

def index(request):
    return None

# Create your views here.
def articleList(request, category=None):
    articles = Article.objects.filter(published=True)
    return render(request, 'articlelist/articlelist.html', {
        'articles': articles,
    })

def articleCreator(request):
    return render(request, 'editor/editor.html', {
    })

def textbox(request):
    return render(request, 'editor/textbox.html', {

    })

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'article/article.html', {
        'article': article,
    })

def publishArticle(request, articleID):
    article = get_object_or_404(Article, id=articleID)
    if article.published:
        article.published = False
    else:
        article.published = True
        article.date = timezone.now()
        article.slug = slugify(article.title)
    article.save()
    return redirect('article', slug=article.slug)
