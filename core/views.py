"""Django views for portfolio application."""
import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .models import ContactMessage, PortfolioSettings, Project, Skill

logger = logging.getLogger(__name__)


@cache_page(settings.CACHE_TIMEOUT_MEDIUM)
def home(request):
    """
    Vista principal del portfolio.

    Muestra habilidades y proyectos destacados con queries optimizadas
    y caché para mejorar el rendimiento.
    """
    # Get portfolio settings (cached)
    portfolio_settings = cache.get("portfolio_settings")
    if not portfolio_settings:
        portfolio_settings = PortfolioSettings.get_settings()
        cache.set("portfolio_settings", portfolio_settings, settings.CACHE_TIMEOUT_LONG)

    # Get featured skills (optimized query)
    skills_queryset = Skill.objects.filter(is_featured=True).order_by("display_order", "name")
    skills = []
    for skill in skills_queryset:
        skills.append(
            {
                "name": skill.name,
                "icon_url": skill.icon_url,
                "proficiency_level": skill.proficiency_level,
                "proficiency_display": skill.get_proficiency_level_display(),
            }
        )

    # Get featured projects (optimized with select_related and prefetch_related)
    projects = (
        Project.objects.filter(is_featured=True)
        .select_related("category")
        .prefetch_related("technologies")
        .order_by("display_order", "-created_at")
    )

    # Format projects for template
    formatted_projects = []
    for project in projects:
        # Technologies already prefetched, no additional queries
        technologies = [tech.name for tech in project.technologies.all()]

        formatted_projects.append(
            {
                "title": project.title,
                "description": project.description,
                "github": project.github_url,
                "demo": project.demo_url,
                "category": project.category.name if project.category else None,
                "status": project.get_status_display(),
                "technologies": technologies,
            }
        )

    # GitHub URL from settings
    github_url = f"https://github.com/{portfolio_settings.github_username}"

    context = {
        "skills": skills,
        "projects": formatted_projects,
        "github_url": github_url,
        "settings": portfolio_settings,
    }

    return render(request, "portfolio.html", context)


@ensure_csrf_cookie
@require_http_methods(["POST"])
def contact_form(request):
    """
    Maneja el envío del formulario de contacto.

    Valida datos, crea registro en BD y envía notificación por email.
    Requiere CSRF token para seguridad.
    """
    try:
        data = json.loads(request.body)

        # Validate required fields
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        message_text = data.get("message", "").strip()

        if not all([name, email, subject, message_text]):
            logger.warning(f"Contact form validation failed - missing fields from {email}")
            return JsonResponse(
                {"success": False, "message": "Todos los campos son obligatorios."}, status=400
            )

        # Basic email validation
        if "@" not in email or "." not in email:
            logger.warning(f"Contact form validation failed - invalid email: {email}")
            return JsonResponse(
                {"success": False, "message": "El email proporcionado no es válido."}, status=400
            )

        # Create contact message in database
        contact_message = ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message_text
        )

        logger.info(f"Contact message created: {contact_message.id} from {email}")

        # Send email notification
        try:
            email_subject = f"Nuevo mensaje del portfolio: {subject}"
            email_message = f"""
Nuevo mensaje recibido desde el portfolio:

Nombre: {name}
Email: {email}
Asunto: {subject}

Mensaje:
{message_text}

---
Este mensaje fue enviado desde tu portfolio web.
ID del mensaje: {contact_message.id}
            """.strip()

            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            logger.info(f"Contact email sent successfully for message {contact_message.id}")

        except Exception as email_error:
            # Email failed but message was saved to database
            logger.error(
                f"Error sending contact email for message {contact_message.id}: {email_error}",
                exc_info=True,
            )

        return JsonResponse(
            {"success": True, "message": "¡Mensaje enviado correctamente! Te contactaré pronto."}
        )

    except json.JSONDecodeError:
        logger.error("Invalid JSON in contact form submission")
        return JsonResponse(
            {"success": False, "message": "Datos del formulario inválidos."}, status=400
        )

    except Exception as e:
        logger.error(f"Unexpected error in contact form: {e}", exc_info=True)
        return JsonResponse(
            {"success": False, "message": "Error al enviar el mensaje. Inténtalo de nuevo."},
            status=500,
        )


@cache_page(settings.CACHE_TIMEOUT_MEDIUM)
def skills_api(request):
    """
    Get featured skills via JSON API.

    Returns a paginated list of featured skills in JSON format
    with caching enabled for improved performance.
    """
    try:
        # Get page parameter
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", settings.PAGINATION_PAGE_SIZE)

        # Get category filter
        category = request.GET.get("category", None)

        # Base queryset
        queryset = Skill.objects.filter(is_featured=True).order_by("display_order", "name")

        # Apply filters
        if category:
            queryset = queryset.filter(category=category)

        # Pagination
        paginator = Paginator(queryset, page_size)

        try:
            skills_page = paginator.page(page)
        except PageNotAnInteger:
            skills_page = paginator.page(1)
        except EmptyPage:
            skills_page = paginator.page(paginator.num_pages)

        # Serialize data
        skills_data = []
        for skill in skills_page:
            skills_data.append(
                {
                    "id": skill.id,
                    "name": skill.name,
                    "icon_url": skill.icon_url,
                    "category": skill.category,
                    "proficiency_level": skill.proficiency_level,
                    "proficiency_display": skill.get_proficiency_level_display(),
                    "years_experience": skill.years_experience,
                }
            )

        return JsonResponse(
            {
                "success": True,
                "skills": skills_data,
                "pagination": {
                    "page": skills_page.number,
                    "total_pages": paginator.num_pages,
                    "total_items": paginator.count,
                    "has_next": skills_page.has_next(),
                    "has_previous": skills_page.has_previous(),
                },
            }
        )

    except Exception as e:
        logger.error(f"Error in skills_api: {e}", exc_info=True)
        return JsonResponse({"success": False, "error": "Error retrieving skills"}, status=500)


@cache_page(settings.CACHE_TIMEOUT_MEDIUM)
def projects_api(request):
    """
    Get featured projects via JSON API.

    Returns a paginated list of projects with filters and optimized queries
    using select_related and prefetch_related for performance.
    """
    try:
        # Get page parameter
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", settings.PAGINATION_PAGE_SIZE)

        # Get filters
        category = request.GET.get("category", None)
        status_filter = request.GET.get("status", None)

        # Base queryset with optimizations
        queryset = (
            Project.objects.filter(is_featured=True)
            .select_related("category")
            .prefetch_related("technologies")
            .order_by("display_order", "-created_at")
        )

        # Apply filters
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Pagination
        paginator = Paginator(queryset, page_size)

        try:
            projects_page = paginator.page(page)
        except PageNotAnInteger:
            projects_page = paginator.page(1)
        except EmptyPage:
            projects_page = paginator.page(paginator.num_pages)

        # Serialize data
        projects_data = []
        for project in projects_page:
            projects_data.append(
                {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "detailed_description": project.detailed_description,
                    "github_url": project.github_url,
                    "demo_url": project.demo_url,
                    "featured_image": project.featured_image,
                    "category": {"name": project.category.name, "color": project.category.color}
                    if project.category
                    else None,
                    "status": project.status,
                    "status_display": project.get_status_display(),
                    "technologies": [
                        {"name": tech.name, "icon_url": tech.icon_url}
                        for tech in project.technologies.all()
                    ],
                    "start_date": project.start_date.isoformat() if project.start_date else None,
                    "end_date": project.end_date.isoformat() if project.end_date else None,
                    "duration_display": project.duration_display,
                }
            )

        return JsonResponse(
            {
                "success": True,
                "projects": projects_data,
                "pagination": {
                    "page": projects_page.number,
                    "total_pages": paginator.num_pages,
                    "total_items": paginator.count,
                    "has_next": projects_page.has_next(),
                    "has_previous": projects_page.has_previous(),
                },
            }
        )

    except Exception as e:
        logger.error(f"Error in projects_api: {e}", exc_info=True)
        return JsonResponse({"success": False, "error": "Error retrieving projects"}, status=500)
