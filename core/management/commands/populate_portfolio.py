"""Django management command to populate portfolio database with initial data."""
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import PortfolioSettings, Project, ProjectCategory, Skill


class Command(BaseCommand):
    """Management command to populate the database with initial portfolio data."""

    help = "Populate the database with initial portfolio data"

    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update even if data already exists",
        )

    def handle(self, *args, **options):
        """Execute the command to populate portfolio data."""
        with transaction.atomic():
            self.populate_skills(options["force"])
            self.populate_project_categories()
            self.populate_projects(options["force"])
            self.populate_settings(options["force"])

        self.stdout.write(self.style.SUCCESS("Successfully populated portfolio data!"))

    def populate_skills(self, force=False):
        """Populate skills data in the database."""
        skills_data = [
            {
                "name": "Python",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
                    "python/python-original.svg"
                ),
                "category": "language",
                "proficiency_level": 4,
                "display_order": 1,
            },
            {
                "name": "Django",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "django/django-plain.svg"
                ),
                "category": "framework",
                "proficiency_level": 4,
                "display_order": 2,
            },
            {
                "name": "FastAPI",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
                    "fastapi/fastapi-original.svg"
                ),
                "category": "framework",
                "proficiency_level": 3,
                "display_order": 3,
            },
            {
                "name": "Flask",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "flask/flask-original.svg"
                ),
                "category": "framework",
                "proficiency_level": 3,
                "display_order": 4,
            },
            {
                "name": "SQL",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "mysql/mysql-original.svg"
                ),
                "category": "database",
                "proficiency_level": 3,
                "display_order": 5,
            },
            {
                "name": "PostgreSQL",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
                    "postgresql/postgresql-original.svg"
                ),
                "category": "database",
                "proficiency_level": 3,
                "display_order": 6,
            },
            {
                "name": "Git",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "git/git-original.svg"
                ),
                "category": "tool",
                "proficiency_level": 3,
                "display_order": 7,
            },
            {
                "name": "Docker",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
                    "docker/docker-original.svg"
                ),
                "category": "cloud",
                "proficiency_level": 3,
                "display_order": 8,
            },
            {
                "name": "NGINX",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "nginx/nginx-original.svg"
                ),
                "category": "tool",
                "proficiency_level": 2,
                "display_order": 9,
            },
            {
                "name": "HTML",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "html5/html5-original.svg"
                ),
                "category": "language",
                "proficiency_level": 3,
                "display_order": 10,
            },
            {
                "name": "CSS",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/" "css3/css3-original.svg"
                ),
                "category": "language",
                "proficiency_level": 3,
                "display_order": 11,
            },
            {
                "name": "JavaScript",
                "icon_url": (
                    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
                    "javascript/javascript-original.svg"
                ),
                "category": "language",
                "proficiency_level": 2,
                "display_order": 12,
            },
        ]

        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data["name"], defaults=skill_data
            )
            if force and not created:
                for key, value in skill_data.items():
                    setattr(skill, key, value)
                skill.save()
                self.stdout.write(f"Updated skill: {skill.name}")
            elif created:
                self.stdout.write(f"Created skill: {skill.name}")

    def populate_project_categories(self):
        """Populate project categories in the database."""
        categories_data = [
            {"name": "Web Application", "color": "#3B82F6"},
            {"name": "API", "color": "#10B981"},
            {"name": "Library", "color": "#8B5CF6"},
            {"name": "Tool", "color": "#F59E0B"},
        ]

        for cat_data in categories_data:
            category, created = ProjectCategory.objects.get_or_create(
                name=cat_data["name"], defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

    def populate_projects(self, force=False):
        """Populate projects data in the database."""
        web_category = ProjectCategory.objects.get(name="Web Application")

        projects_data = [
            {
                "title": "Biblioteca Digital",
                "description": "Una plataforma para gestionar y acceder a libros digitales.",
                "detailed_description": (
                    "Sistema completo de gestión de biblioteca digital con autenticación "
                    "de usuarios, sistema de búsqueda avanzado, gestión de préstamos y "
                    "devoluciones. Desarrollado con Django y Django REST Framework."
                ),
                "github_url": "https://github.com/Kallheset/Biblioteca-django-drf",
                "category": web_category,
                "status": "completed",
                "display_order": 1,
            },
            {
                "title": "Gestor de Tareas",
                "description": "Aplicación para organizar y gestionar tareas diarias.",
                "detailed_description": (
                    "Aplicación web para gestión de tareas con funcionalidades de crear, "
                    "editar, eliminar y marcar como completadas. Incluye categorización y "
                    "filtros avanzados."
                ),
                "github_url": "https://github.com/Kallheset/gestor-de-tareas",
                "category": web_category,
                "status": "completed",
                "display_order": 2,
            },
            {
                "title": "To-Do App",
                "description": "Una simple aplicación para llevar un control de tareas.",
                "detailed_description": (
                    "Aplicación minimalista de to-do list con interfaz limpia y "
                    "funcionalidades básicas de gestión de tareas."
                ),
                "github_url": "https://github.com/Kallheset/todo-app",
                "category": web_category,
                "status": "completed",
                "display_order": 3,
            },
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=project_data["title"], defaults=project_data
            )
            if force and not created:
                for key, value in project_data.items():
                    if key != "title":  # Don't update the unique field
                        setattr(project, key, value)
                project.save()
                self.stdout.write(f"Updated project: {project.title}")
            elif created:
                self.stdout.write(f"Created project: {project.title}")

        # Add technologies to projects after creation
        self.link_project_technologies()

    def link_project_technologies(self):
        """Link technologies (skills) to projects via many-to-many relationships."""
        # Get skills
        python = Skill.objects.get(name="Python")
        django = Skill.objects.get(name="Django")
        html = Skill.objects.get(name="HTML")
        css = Skill.objects.get(name="CSS")
        js = Skill.objects.get(name="JavaScript")

        # Link technologies to projects
        biblioteca = Project.objects.get(title="Biblioteca Digital")
        biblioteca.technologies.set([python, django, html, css])

        gestor = Project.objects.get(title="Gestor de Tareas")
        gestor.technologies.set([python, django, html, css, js])

        todo = Project.objects.get(title="To-Do App")
        todo.technologies.set([python, django, html, css])

        self.stdout.write("Linked technologies to projects")

    def populate_settings(self, force=False):
        """Populate portfolio settings (singleton) in the database."""
        settings_data = {
            "site_title": "Argenis Manzanares",
            "tagline": "Desarrollador Backend en Python",
            "about_me": (
                "Desarrollador Backend especializado en Python con más de 2 años de "
                "experiencia creando aplicaciones web robustas y escalables. Experto en "
                "Django y FastAPI para el desarrollo de APIs RESTful, con sólidos "
                "conocimientos en bases de datos SQL/PostgreSQL y optimización de queries.\n\n"
                "Mi enfoque se centra en código limpio y buenas prácticas, aplicando "
                "principios SOLID, patrones de diseño y estándares de desarrollo que "
                "garantizan mantenibilidad y escalabilidad. Experiencia práctica en Docker "
                "para containerización y GitHub para control de versiones y colaboración "
                "en equipos.\n\n"
                "Me especializo en:\n\n"
                "• Optimización de base de datos: Implementación de índices estratégicos, "
                "select_related/prefetch_related\n"
                "• Validaciones robustas: Constraints a nivel de modelo y base de datos\n"
                "• Testing: Desarrollo dirigido por pruebas con tests unitarios e integración\n"
                "• Arquitectura de software: Aplicación de principios SOLID y DRY\n\n"
                "Siempre en constante aprendizaje, actualmente explorando arquitecturas de "
                "microservicios y herramientas de DevOps. Me apasiona resolver problemas "
                "complejos del backend, optimizar rendimiento y crear soluciones técnicas "
                "innovadoras que impacten positivamente en la experiencia del usuario.\n\n"
                "Enfoque actual: Perfeccionando habilidades en optimización de queries, "
                "patrones de diseño avanzados y mejores prácticas de testing para crear "
                "aplicaciones backend de alta calidad."
            ),
            "email": "argenis010@gmail.com",
            "github_username": "Kallheset",
            "linkedin_url": "https://www.linkedin.com/in/argenis-manzanares-108b4a349/",
            "cv_file_path": "cv/Argenis_Manzanares_CV.pdf",
        }

        settings, created = PortfolioSettings.objects.get_or_create(pk=1, defaults=settings_data)

        if force and not created:
            for key, value in settings_data.items():
                setattr(settings, key, value)
            settings.save()
            self.stdout.write("Updated portfolio settings")
        elif created:
            self.stdout.write("Created portfolio settings")
