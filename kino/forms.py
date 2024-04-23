from django import forms
from kino.models import Review, Film


class FilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Все страны'
        self.fields['year'].empty_label = 'Все Годы'
        self.fields['genres'].empty_label = 'Все жанры'
        self.fields['country'].required = False
        self.fields['year'].required = False
        self.fields['genres'].required = False



    class Meta:
        model = Film
        fields = ['country', 'genres', 'year']
        widgets = {
            'genres': forms.Select(choices=Film.genres)
        }


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