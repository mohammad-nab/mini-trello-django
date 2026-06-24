from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ProjectMember, Project
from .forms import CreateProjectForm


class CreateProjectView(View):
    form_class = CreateProjectForm
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
            return redirect("home:home")

        messages.error(request,"Project didn't create",'danger')
        return render(request, self.template_name,{"form":form})


class DeleteProjectView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        messages.success(request,"Project deleted successfully",'success')
        return redirect("home:home")