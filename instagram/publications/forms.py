from django import forms

from .models import Post


class PostCreateView(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
