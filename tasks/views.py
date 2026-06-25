from django.shortcuts import render, redirect
from django import views
from projects.models import Project
from .forms import CreateColumnForm


class CreateColumnView(views.View):
    form_class = CreateColumnForm
    template_name = 'tasks/create_column.html'

    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():

            project = Project.objects.get(pk=pk)
            column = form.save(commit=False)
            column.project = project
            form.save()

            return redirect('projects:detail-project')
        return render(request, self.template_name, {'form': form})