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
    categories = Category.objects.all()
    if category: articles = articles.filter(category__name=category) 
    print(categories)
    return render(request, 'list.html', {
        'articles': articles,
        'categories': categories,
        'category': category,
    })

def articleCreator(request, articleID, sectionID=None, action=None):

    article = get_object_or_404(Article, id=articleID)
    section = get_object_or_404(Section, id=sectionID) if sectionID else None

    #POST they hit submit yo
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=section)

        if form.is_valid():
            if form.cleaned_data['text'] == "" and form.cleaned_data['image'] == None: return redirect("articlecreator", articleID)

            section = form.save(commit=False)
            section.article = article

            if not section.order: section.order = article.sections.all().count() + 1

            addImage(form)
            
            section.save()
            section.article.save()
            return redirect('articleeditor', articleID)
    else:
        def futureSectionShift(value):
            #shift all future section 'order' values by 'value' interval
            nextSections = article.sections.all().filter(order__gt=section.order)
            for foo in nextSections:
                foo.order += value
                foo.save()

        def swapSection(value):
            #swap current section order with the order of current section order + value
            otherSection = article.sections.get(order=section.order + value)
            otherSectionOrder = otherSection.order
            otherSection.order = section.order
            otherSection.save()
            section.order = otherSectionOrder
            section.save()

        match action:
            case 'up':
                swapSection(-1)
                return redirect('articleeditor', articleID)
            case 'add':
                futureSectionShift(1)
                newSection = Section(article=article, order=section.order + 1, text="This the new section!")
                newSection.save()
                return redirect('articlesectioneditor', articleID=articleID, sectionID=newSection.id)
            case 'down':
                swapSection(1)
                section.save()
                return redirect('articleeditor', articleID)
            case 'delete':
                futureSectionShift(-1)
                section.delete()
                return redirect('articleeditor', articleID)

    form = ArticleForm(instance=section)
    sections = []
    articleSections = article.sections.all()
    articleSections = articleSections.order_by("order")
    article.description = MarkDown.convert(article.description) if article.description else None
    article.caption = MarkDown.convert(article.caption) if article.caption else None
    for section in articleSections:
        section.text = MarkDown.convert(section.text) if section.text else None
        section.caption = MarkDown.convert(section.caption) if section.caption else None
        sections.append(section)
    return render(request, 'editor.html', {
        'article': article,
        'form': form,
        'sections': sections,
    })

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    sections = []
    articleSections = article.sections.all()
    articleSections = articleSections.order_by("order")
    article.description = MarkDown.convert(article.description) if article.description else None
    article.caption = MarkDown.convert(article.caption) if article.caption else None
    for section in articleSections:
        section.text = MarkDown.convert(section.text) if section.text else None
        section.caption = MarkDown.convert(section.caption) if section.caption else None
        sections.append(section)
    return render(request, 'ArticleCreator.html', {
        'article': article,
        'sections': sections
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
