from django.db import models
from django import forms
from django.contrib.auth.models import User



class Resume(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)


class ResumeCreateForm(forms.Form):
    description = forms.CharField()
