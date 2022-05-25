from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['title', 'classification', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '리뷰를 남길 경우, 영화명과 10점 만점으로 평점을 남겨주세요 \'^\''}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }
