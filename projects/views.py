from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ProjectMember, Project
from .forms import ProjectForm


class CreateProjectView(View):
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

            ProjectMember.objects.create(project=project,user=request.user,is_staff=True)
            messages.success(request,"Project created successfully",'success')
            return redirect("projects:detail-project")

        messages.error(request,"Project didn't create",'danger')
        return render(request, self.template_name,{"form":form})


class DeleteProjectView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        messages.success(request,"Project deleted successfully",'success')
        return redirect("projects:project-dashboard")


class DetailProjectView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request,'projects/project_detail.html',{'project':project})


class DashboardProjectView(View):
    def get(self, request):
        projects = Project.objects.filter(owner=request.user)
        return render(request,'projects/project_dashboard.html',{'projects':projects})


class UpdateProjectView(View):
    form_class = ProjectForm
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = self.form_class(instance=project)
        return render(request,'projects/project_update.html',{'form':form})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = self.form_class(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,"Project updated successfully",'success')
            return redirect("projects:detail-project",pk=project.pk)