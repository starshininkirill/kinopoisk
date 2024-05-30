from django import forms
from kino.models import Review, Film, Genre, Year


class FilterForm(forms.ModelForm):
    year = forms.ModelChoiceField(queryset=Year.objects.order_by('-year'))
    genres = forms.ModelChoiceField(queryset=Genre.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Все страны'
        self.fields['country'].label = 'Страны'
        self.fields['year'].empty_label = 'Все Годы'
        self.fields['year'].label = 'Годы'
        self.fields['genres'].label = 'Жанры'
        self.fields['genres'].empty_label = 'Все жанры'
        self.fields['country'].required = False
        self.fields['year'].required = False
        self.fields['genres'].required = False

    class Meta:
        model = Film
        fields = ['country', 'genres', 'year']


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
