from django.contrib.auth import get_user_model

User = get_user_model()

def project_members(project):
    return User.objects.filter(
        projectmember__project=project
    )