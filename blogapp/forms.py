from django import forms
from .models import Post
from froala_editor.widgets import FroalaEditor
from .models import *


class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content']
        