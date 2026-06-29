from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django import views
from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from conf import permissions
from .models import Column, Task, ActivityLog
from .forms import titleColumnForm, TaskForm
import json


class CreateColumnView(LoginRequiredMixin, views.View):
    form_class = titleColumnForm
    template_name = 'tasks/title_column.html'

    def dispatch(self, request, *args, **kwargs):
        project = get_object_or_404(Project,pk=self.kwargs['pk'])
        if not permissions.is_project_owner(request.user, project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
            ActivityLog.objects.create(
                user=request.user,
                project=column.project,
                activity_type="create-column",
                description=f"{request.user} created {column.name} column",
            )

            return redirect('projects:detail-project',pk=pk)
        return render(request, self.template_name, {'form': form})


class UpdateColumnView(LoginRequiredMixin, views.View):
    form_class = titleColumnForm
    template_name = 'tasks/title_column.html'

    def dispatch(self, request, *args, **kwargs):
        column = get_object_or_404(Column,pk=self.kwargs['pk'])
        if not permissions.is_project_owner(request.user, column.project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,pk):
        column = get_object_or_404(Column,pk=pk)
        form = self.form_class(request.POST, instance=column)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user,
                project=column.project,
                activity_type="edit-column",
                description=f"{request.user} edited {column.name} column",
            )
            return redirect('projects:detail-project',pk=column.project.pk)

        return render(request, self.template_name, {'form': form})


class DeleteColumnView(LoginRequiredMixin, views.View):
    def dispatch(self, request, *args, **kwargs):
        column = get_object_or_404(Column,pk=self.kwargs['pk'])
        if not permissions.is_project_owner(request.user, column.project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,pk):
        column = get_object_or_404(Column,pk=pk)
        project = column.project
        name = column.title
        column.delete()
        ActivityLog.objects.create(
            user=request.user,
            project=column.project,
            activity_type="delete-column",
            description=f"{request.user} deleted {name} column",
        )
        return redirect('projects:detail-project',pk=project.pk)


class CreateTaskView(LoginRequiredMixin, views.View):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'

    def dispatch(self, request, *args, **kwargs):
        self.column = get_object_or_404(Column,pk=self.kwargs['pk'])
        if not permissions.is_project_member(request.user, self.column.project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,pk):
        form = self.form_class(project=self.column.project)
        return render(request, self.template_name, {'form': form})

    def post(self,request, pk):
        form = self.form_class(request.POST, project=self.column.project)
        if form.is_valid():
            task = form.save(commit=False)
            task.column = self.column
            task.save()
            ActivityLog.objects.create(
                user=request.user,
                project=task.column.project,
                activity_type="create-task",
                description=f"{request.user} created {task.title} task",
            )
            return redirect('projects:detail-project',pk=self.column.project.pk )

        return render(request, self.template_name, {'form': form})


class UpdateTaskView(LoginRequiredMixin, views.View):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task,pk=self.kwargs['pk'])
        if not permissions.is_project_member(request.user, task.column.project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


    def get(self, request,pk):
        form = self.form_class(instance=Task.objects.get(pk=pk))
        return render(request, self.template_name, {'form': form})

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        form = self.form_class(request.POST,instance=task)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user,
                project=task.column.project,
                activity_type="edit-task",
                description=f"{request.user} edited {task.title} task",
            )
            return redirect('projects:detail-project',pk=task.column.project.pk)

        return render(request, self.template_name, {'form': form})


class DeleteTaskView(LoginRequiredMixin, views.View):
    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task,pk=self.kwargs['pk'])
        if not permissions.is_project_owner(request.user, task.column.project):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,pk):
        task = get_object_or_404(Task,pk=pk)
        name = task.title
        task.delete()
        ActivityLog.objects.create(
            user=request.user,
            project=task.column.project,
            activity_type="delete-task",
            description=f"{request.user} deleted {name} task",
        )
        return redirect('projects:detail-project',pk=task.column.project.pk)


class MoveTaskView(LoginRequiredMixin, views.View):
    def post(self,request):
        data = json.loads(request.body)

        task_id = data['task_id']
        column_id = data['column_id']

        column = get_object_or_404(Column,pk=column_id)
        task = get_object_or_404(Task,pk=task_id, column__project=column.project)

        if not permissions.is_project_member(request.user, task.column.project):
            raise PermissionDenied

        task.column = column
        task.save()

        ActivityLog.objects.create(
            user=request.user,
            project=task.column.project,
            activity_type="move-task",
            description=f"{request.user} moved {task.title} task",
        )

        return JsonResponse({
            "success": True,
            "task_id": task.id,
            "column_id": column.id,
        })
