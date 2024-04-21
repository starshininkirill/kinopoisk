from django import forms
from kino.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'type', ]
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Текст'
            }),
        }