from django.db import models
from django.conf import settings


class Review(models.Model):
    title = models.CharField(max_length=100)
    c_Question = '[질문]'
    c_Review = '[리뷰]'
    c_Free = '[자유]'
    Classification_choices = [(c_Question, '[질문]'), (c_Review, '[리뷰]'), (c_Free, '[자유]')]
    classification = models.CharField(max_length=10, choices=Classification_choices, default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')


class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
