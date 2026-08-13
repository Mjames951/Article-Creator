from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .tools.imagehandler import addImage
from .models import *
from .forms import *
from .tools import emailhandler

from ArticleCreator.models import Article, Author
from ArticleCreator.models import Category as ArticleCategory
from ArticleCreator.forms import ArticleStarterForm, AuthorForm, ArticleCategoryForm 

Forms = {
    'article': ArticleStarterForm,
    'author': AuthorForm,
    'articlecategory': ArticleCategoryForm,
}

def CRUD(request, modelname, id=None, parentid=None):
    if id: 
        model = getModel(modelname)
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
                
            model.save()
            return redirect(model.get_absolute_url())
            
    else: form = Forms[modelname](instance=model)
    return render(request, "admin/form.html", {
        "form": form,
        "model": modelname,
    })

def DELETE(request, modelname, id):
    if not modelname in Models: return redirect("index")
    model = Models[modelname]
    model = get_object_or_404(model, id=id)
    try:
        if model.image:
            model.image.delete()
    except: pass
    model.delete()
    return redirect(adminURL)