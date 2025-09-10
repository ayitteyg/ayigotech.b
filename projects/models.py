from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.JSONField(default=list, blank=True)  # works with SQLite & Postgres
    github_link = models.URLField()
    demo_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/")
    is_mobile_app = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    problem = models.TextField()
    solution = models.TextField()
    outcome = models.TextField()

    def __str__(self):
        return self.title


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="screenshots",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="projects/screenshots/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} Screenshot {self.order}"
