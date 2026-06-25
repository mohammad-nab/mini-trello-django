from django.contrib import admin
from tasks.models import Column
from tasks.models import Task


admin.site.register(Task)
admin.site.register(Column)