from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('library/', views.articleList, name='articlelist'),
    path('library/<category>/', views.articleList, name='articlecategory'),
    path('articlecreator/<articleID>/', views.articleCreator, name='articleeditor'),
    path('articlecreator/<articleID>/<sectionID>/', views.articleCreator, name='articlesectioneditor'),
    path('articlecreator/<articleID>/<sectionID>/<action>/', views.articleCreator, name='articlesectionaction'),
    path('publisher/<articleID>/', views.publishArticle, name='publisharticle'),
    path('<slug:slug>/', views.article, name='article'),
]