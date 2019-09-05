from django import forms

from .models import InstagramUser


class InstagramUserCreationForm(forms.ModelForm):
    class Meta:
        model = InstagramUser
        exclude = []


class InstagramUserChangeForm(forms.ModelForm):
    class Meta:
        model = InstagramUser
        exclude = []
