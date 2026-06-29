from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from conf import permissions
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Project
from tasks.models import ActivityLog
from .forms import ProjectForm


class CreateProjectView(LoginRequiredMixin, View):
    form_class = ProjectForm
    template_name = "projects/create_project.html"
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name,{"form": form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.create_default_columns()
            project.add_owner_as_member()
            messages.success(request,"Project created successfully",'success')
            return redirect("projects:detail-project",pk=project.pk)

        messages.error(request,"Project didn't create",'danger')
        return render(request, self.template_name,{"form":form})


class DeleteProjectView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        if not permissions.is_project_owner(request.user, project):
            return HttpResponseForbidden("You are not allowed to delete this project")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user != project.owner:
            return HttpResponseForbidden()
        project.delete()
        messages.success(request,"Project deleted successfully",'success')
        return redirect("projects:project-dashboard")


class DetailProjectView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not permissions.is_project_member(request.user, self.project):
            return HttpResponseForbidden("You are not allowed to view this project")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        columns = self.project.columns.order_by('order')

        return render(
            request,
            'projects/project_detail.html',
            {
                'project': self.project,
                'columns': columns,
            }
        )


class DashboardProjectView(LoginRequiredMixin, View):
    def get(self, request):
        projects = Project.objects.filter(projectmember__user=request.user)
        return render(request,'projects/project_dashboard.html',{'projects':projects})


class UpdateProjectView(LoginRequiredMixin, View):
    form_class = ProjectForm
    def setup(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not permissions.is_project_owner(request.user, self.project):
            return HttpResponseForbidden("You are not allowed to update this project")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        form = self.form_class(instance=self.project)
        return render(request,'projects/project_update.html',{'form':form})

    def post(self, request, pk):
        form = self.form_class(request.POST, instance=self.project)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user,
                project=self.project,
                activity_type="edit-project",
                description=f"{request.user} edited {self.project.name}",
            )
            messages.success(request,"Project updated successfully",'success')
            return redirect("projects:detail-project",pk=self.project.pk)

        return render(
            request,
            'projects/project_update.html',
            {'form': form}
        )