from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from projects.models import ProjectMember


class Column(models.Model):
    project = models.ForeignKey("projects.Project",on_delete=models.CASCADE,related_name='columns')
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return f'{self.project}:{self.title}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_column = (
                Column.objects
                .filter(project=self.project)
                .order_by('-order')
                .first()
            )

            self.order = 0 if last_column is None else last_column.order + 1

        super().save(*args, **kwargs)



class Task(models.Model):
    column = models.ForeignKey(Column,on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='assigned_to')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_task = (
                Task.objects.filter(column=self.column).order_by('-order').first()
            )
            self.order = 0 if last_task is None else last_task.order + 1
        
        super().save(*args,**kwargs)


    def __str__(self):
        return f'{self.column.project}:{self.column}:{self.title}'


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='activity_logs')
    project = models.ForeignKey("projects.Project",on_delete=models.CASCADE,related_name='activity_logs')
    activity_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return f'{self.user}:{self.activity_type} - {self.project}'