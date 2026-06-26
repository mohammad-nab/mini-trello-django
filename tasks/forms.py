from django import forms
from .models import Column

class titleColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title']
