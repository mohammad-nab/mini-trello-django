from django.contrib.auth.models import User
from django.db import models
from projects.models import Project


class Column(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='columns')
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.project}:{self.title}'


class Task(models.Model):
    column = models.ForeignKey(Column,on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_to')
    order = models.PositiveIntegerField(default=0)