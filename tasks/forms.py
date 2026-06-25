from django import forms
from .models import Column

class CreateColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title']
