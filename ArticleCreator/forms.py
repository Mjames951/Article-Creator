from django import forms
from .models import Article, Author, Category

class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'author', 'title', 'image', 'content']
        labels = {
            'image': 'Main Article Image',
            'description': 'Description (first paragraph - summary / hook)'
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'image']


