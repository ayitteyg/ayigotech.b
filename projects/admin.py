from django.contrib import admin
from .models import Project, ProjectScreenshot

class ProjectScreenshotInline(admin.TabularInline):  # or StackedInline if you prefer
    model = ProjectScreenshot
    extra = 1  # how many empty slots to show for adding new screenshots
    fields = ("image", "order")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_mobile_app", "created_at", "github_link", "demo_link")
    list_filter = ("is_mobile_app", "created_at")
    search_fields = ("title", "description", "problem", "solution", "outcome")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    inlines = [ProjectScreenshotInline]
