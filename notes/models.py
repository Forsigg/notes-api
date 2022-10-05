from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=30)


class Note(models.Model):
    text = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateField(auto_created=True, auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
