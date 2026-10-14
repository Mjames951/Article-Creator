from django.urls import path
from . import views
from . import CRUD

urlpatterns = [
    path('', views.articleList, name='index'),
    path('list/', views.articleList, name='articlelist'),

    path('articlecreator/', views.articleCreator, name='editor'),
    path('articlecreator/form/', views.editorForm, name='editorform'),
    
    path('publisher/<articleID>/', views.publishArticle, name='publisharticle'),
    path('<slug:slug>/', views.article, name='article'),
]