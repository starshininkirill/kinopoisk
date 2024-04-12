from django import forms
from kino.models import Review


class ReviewForm(forms.ModelForm):

    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Текст'
    }))

    type = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'тайп'
    }))

    class Meta:
        model = Review
        fields = ('text', 'type', )
