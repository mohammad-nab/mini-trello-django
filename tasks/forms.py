from django import forms
from .models import Column, Task
from .utils import project_members


class titleColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','assigned_to']

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

        if project:
            self.fields["assigned_to"].queryset = project_members(project)
