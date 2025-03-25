from .models import Article, InstructionText, InstructionImage
from django.forms import ModelForm, TextInput, Textarea, DateInput
from django import forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
import json


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'photo', 'description', 'ingredients', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва рецепту'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Короткий опис'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Інгредієнти'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Примітки (необов’язково)'}),
        }


class InstructionTextForm(forms.ModelForm):
    class Meta:
        model = InstructionText
        fields = ['text']

class InstructionImageForm(forms.ModelForm):
    class Meta:
        model = InstructionImage
        fields = ['image']


# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['rating']
#
#     rating = forms.ChoiceField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
#                                widget=forms.RadioSelect)

