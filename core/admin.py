"""
Django admin configuration for core app models.

Provides customized admin interfaces for managing portfolio content including
skills, projects, experiences, contact messages, and site settings.
"""
from django.contrib import admin

from .models import ContactMessage, Experience, PortfolioSettings, Project, ProjectCategory, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin interface for managing skills."""

    list_display = ("name", "category", "proficiency_level", "is_featured", "display_order")
    list_filter = ("category", "proficiency_level", "is_featured")
    search_fields = ("name",)
    list_editable = ("is_featured", "display_order")
    ordering = ("display_order", "name")


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing project categories."""

    list_display = ("name", "color", "description")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for managing projects."""

    list_display = ("title", "category", "status", "is_featured", "display_order", "created_at")
    list_filter = ("status", "category", "is_featured", "created_at")
    search_fields = ("title", "description")
    list_editable = ("is_featured", "display_order")
    filter_horizontal = ("technologies",)
    date_hierarchy = "created_at"
    ordering = ("display_order", "-created_at")

    fieldsets = (
        (
            "Información Básica",
            {"fields": ("title", "description", "detailed_description", "category")},
        ),
        ("Enlaces", {"fields": ("github_url", "demo_url")}),
        ("Metadatos", {"fields": ("technologies", "status", "start_date", "end_date")}),
        ("Configuración", {"fields": ("is_featured", "display_order")}),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Admin interface for managing work experiences and education."""

    list_display = (
        "title",
        "company_or_institution",
        "experience_type",
        "duration",
        "is_current",
        "is_featured",
    )
    list_filter = ("experience_type", "is_current", "is_featured", "start_date")
    search_fields = ("title", "company_or_institution", "description")
    list_editable = ("is_featured",)
    filter_horizontal = ("technologies",)
    date_hierarchy = "start_date"
    ordering = ("display_order", "-start_date")

    fieldsets = (
        (
            "Información Básica",
            {"fields": ("title", "company_or_institution", "location", "experience_type")},
        ),
        ("Descripción", {"fields": ("description", "technologies")}),
        ("Fechas", {"fields": ("start_date", "end_date", "is_current")}),
        ("Configuración", {"fields": ("is_featured", "display_order")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for managing contact form messages."""

    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_read",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Información del Contacto", {"fields": ("name", "email", "subject")}),
        ("Mensaje", {"fields": ("message",)}),
        ("Estado", {"fields": ("is_read", "created_at")}),
    )


@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(admin.ModelAdmin):
    """Admin interface for managing portfolio site settings (singleton)."""

    list_display = ("site_title", "email", "updated_at")
    readonly_fields = ("updated_at",)

    fieldsets = (
        ("Información Personal", {"fields": ("site_title", "tagline", "about_me")}),
        ("Contacto y Redes", {"fields": ("email", "github_username", "linkedin_url")}),
        ("Archivos", {"fields": ("cv_file_path",)}),
        ("Metadatos", {"fields": ("updated_at",)}),
    )

    def has_add_permission(self, request):
        """Only allow one instance of settings (singleton pattern)."""
        return not PortfolioSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of settings."""
        return False
