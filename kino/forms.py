from django import forms
from kino.models import Review


class ReviewForm(forms.ModelForm):

    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Текст'
    }))
    type = forms.MultipleChoiceField(
        widget=forms.Select(choices=Review.REVIEW_TYPES),
        choices=Review.REVIEW_TYPES
    )

    class Meta:
        model = Review
        fields = ('text', 'type', )
        # widgets = {
        #     'text': forms.CharField(widget=forms.TextInput(attrs={
        #                 'class': 'form-input',
        #                 'placeholder': 'Текст'
        #             })),
        #     'type': forms.MultipleChoiceField(
        #                 widget=forms.Select(choices=Review.REVIEW_TYPES),
        #                 choices=Review.REVIEW_TYPES
        #             ),
        # }
