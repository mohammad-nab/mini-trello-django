from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='projects_owner'
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.updated_at}'

    def create_default_columns(self):
        from tasks.models import Column

        if self.columns.exists():
            return

        defaults = [
            "Todo",
            "In Progress",
            "Done",
        ]

        for index, name in enumerate(defaults, start=1):
            Column.objects.create(
                project=self,
                title=name,
                order=index,
            )

    def add_owner_as_member(self):

        ProjectMember.objects.get_or_create(
            project=self,
            user=self.owner
        )


class ProjectMember(models.Model):
    class Roles(models.TextChoices):
        OWNER = 'owner', 'Owner'
        MEMBER = 'member', 'Member'
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.MEMBER,
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project.name} - {self.user.username}'


