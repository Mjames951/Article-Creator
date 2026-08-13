from django import forms
from .models import Article, Section, Author, Category

class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['text', 'image', 'caption']
        labels = {
            'caption': 'Image Caption'
        }
        widgets = {
            'text': forms.Textarea
        }

class ArticleStarterForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'author', 'image', 'caption', 'description']
        labels = {
            'image': 'Main Article Image',
            'description': 'Description (first paragraph - summary / hook)'
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'image']


