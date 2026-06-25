from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ProjectMember, Project
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
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user != project.owner:
            return HttpResponseForbidden()
        project.delete()
        messages.success(request,"Project deleted successfully",'success')
        return redirect("projects:project-dashboard")


class DetailProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        is_member = ProjectMember.objects.filter(
            project=project,
            user=request.user
        ).exists()

        if not is_member:
            return HttpResponseForbidden()

        return render(
            request,
            'projects/project_detail.html',
            {'project': project}
        )


class DashboardProjectView(LoginRequiredMixin, View):
    def get(self, request):
        projects = Project.objects.filter(projectmember__user=request.user)
        return render(request,'projects/project_dashboard.html',{'projects':projects})


class UpdateProjectView(LoginRequiredMixin, View):
    form_class = ProjectForm
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        is_member = ProjectMember.objects.filter(project=project, user=request.user).exists()
        if not is_member:
            return HttpResponseForbidden()
        form = self.form_class(instance=project)
        return render(request,'projects/project_update.html',{'form':form})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        is_member = ProjectMember.objects.filter(project=project, user=request.user).exists()
        if not is_member:
            return HttpResponseForbidden()
        form = self.form_class(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,"Project updated successfully",'success')
            return redirect("projects:detail-project",pk=project.pk)

        return render(
            request,
            'projects/project_update.html',
            {'form': form}
        )