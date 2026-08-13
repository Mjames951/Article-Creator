from django.urls import path
from . import views

urlpatterns = [
    path('articlecreator/<articleID>/', views.articleCreator, name='articleeditor'),
    path('articlecreator/<articleID>/<sectionID>/', views.articleCreator, name='articlesectioneditor'),
    path('articlecreator/<articleID>/<sectionID>/<action>/', views.articleCreator, name='articlesectionaction'),
    path('publisher/<articleID>/', views.publishArticle, name='publisharticle'),
    path('<slug:slug>/', views.article, name='article'),
]