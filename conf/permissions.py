from projects.models import Project, ProjectMember


def is_project_member(user, project):
    return ProjectMember.objects.filter(user=user, project=project).exists()

def is_project_owner(user, project):
    return ProjectMember.objects.filter(user=user, project=project, role='owner').exists()
