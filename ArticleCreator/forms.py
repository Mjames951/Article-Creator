from django import forms
from .models import Article, Author, Category

class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ArticleStarterForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'author', 'image', 'content']
        labels = {
            'image': 'Main Article Image',
            'description': 'Description (first paragraph - summary / hook)'
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'image']


