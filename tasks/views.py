from django.shortcuts import render, redirect, get_object_or_404
from django import views
from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Column, Task
from .forms import titleColumnForm, TaskForm


class CreateColumnView(LoginRequiredMixin, views.View):
    form_class = titleColumnForm
    template_name = 'tasks/title_column.html'

    def get(self,request,pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():

            project = get_object_or_404(Project,pk=pk)
            column = form.save(commit=False)
            column.project = project
            form.save()

            return redirect('projects:detail-project',pk=pk)
        return render(request, self.template_name, {'form': form})


class UpdateColumnView(LoginRequiredMixin, views.View):
    form_class = titleColumnForm
    template_name = 'tasks/title_column.html'

    def get(self, request, pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,pk):
        column = get_object_or_404(Column,pk=pk)
        form = self.form_class(request.POST, instance=column)
        if form.is_valid():
            form.save()
            return redirect('projects:detail-project',pk=column.project.pk)

        return render(request, self.template_name, {'form': form})


class DeleteColumnView(LoginRequiredMixin, views.View):
    def get(self, request,pk):
        column = get_object_or_404(Column,pk=pk)
        column.delete()
        return redirect('projects:detail-project',pk=column.project.pk)


class CreateTaskView(LoginRequiredMixin, views.View):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    def get(self, request,pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            column = get_object_or_404(Column, pk=pk)
            task = form.save(commit=False)
            task.column = column
            task.save()
            return redirect('projects:detail-project',pk=column.project.pk )


class UpdateTaskView(LoginRequiredMixin, views.View):
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    def get(self, request,pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        form = self.form_class(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('projects:detail-project',pk=task.column.project.pk)