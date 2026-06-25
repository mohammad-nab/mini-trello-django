from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Column(models.Model):
    project = models.ForeignKey("projects.Project",on_delete=models.CASCADE,related_name='columns')
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.project}:{self.title}'


class Task(models.Model):
    column = models.ForeignKey(Column,on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='assigned_to')
    order = models.PositiveIntegerField(default=0)