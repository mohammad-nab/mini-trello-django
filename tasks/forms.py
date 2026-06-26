from django import forms
from .models import Column, Task
from projects.models import ProjectMember


class titleColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','assigned_to']

#TODO filter user that can assign to a task
    '''
    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = ProjectMember.objects.filter(project=kwargs['instance'].project)
        '''