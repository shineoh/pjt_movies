from django import forms
from .models import MovieComment


class MovieCommentForm(forms.ModelForm):
    rating_choices = ((5, 'Five points'),(4, 'Four points'),(3, 'Three points'),(2, 'Two points'),(1, 'One point'))
    rating = forms.ChoiceField(
        label='',
        choices=rating_choices,
        widget=forms.Select(
            attrs={
                'class': ''
            }
        ),
        required=True
    )
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content mx-3 form-control',
                'rows': 1,
                'cols': 40,
                'placeholder': '여러분의 소감을 남겨주세요 :)'
            }
        ),
        required=True
    )
    class Meta:
        model = MovieComment
        fields = ('rating', 'content',)


class MovieCommentUpdateForm(forms.ModelForm):
    rating_choices = ((5, 'Five points'),(4, 'Four points'),(3, 'Three points'),(2, 'Two points'),(1, 'One point'))
    rating = forms.ChoiceField(
        label='',
        choices=rating_choices,
        widget=forms.Select(
            attrs={
                'class': ''
            }
        ),
        required=True
    )
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content mx-3 form-control',
                'rows': 1,
                'cols': 40,
                'placeholder': '여러분의 소감을 남겨주세요 :)'
            }
        ),
        required=True
    )
    class Meta:
        model = MovieComment
        fields = ('rating', 'content',)