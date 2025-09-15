from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Skill, Project, PortfolioSettings, ContactMessage
import json


def home(request):
    # Get portfolio settings
    settings = PortfolioSettings.get_settings()
    
    # Get featured skills
    skills_queryset = Skill.objects.filter(is_featured=True)
    skills = []
    for skill in skills_queryset:
        skills.append({
            'name': skill.name,
            'icon_url': skill.icon_url,
            'proficiency_level': skill.proficiency_level,
            'proficiency_display': skill.get_proficiency_level_display()
        })
    
    # Get featured projects
    projects = Project.objects.filter(is_featured=True).select_related('category')
    
    # Format projects for template
    formatted_projects = []
    for project in projects:
        formatted_projects.append({
            "title": project.title,
            "description": project.description,
            "github": project.github_url,
            "demo": project.demo_url,
            "category": project.category.name if project.category else None,
            "status": project.get_status_display(),
            "technologies": [tech.name for tech in project.technologies.all()]
        })
    
    # GitHub URL from settings
    github_url = f"https://github.com/{settings.github_username}"
    
    context = {
        "skills": skills,
        "projects": formatted_projects,
        "github_url": github_url,
        "settings": settings,
    }
    
    return render(request, "portfolio.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_form(request):
    """Handle contact form submissions"""
    try:
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Create contact message in database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification
        try:
            email_subject = f"Nuevo mensaje del portfolio: {subject}"
            email_message = f"""
Nuevo mensaje recibido desde el portfolio:

Nombre: {name}
Email: {email}
Asunto: {subject}

Mensaje:
{message}

---
Este mensaje fue enviado desde tu portfolio web.
            """.strip()
            
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
        except Exception as email_error:
            # Email failed but message was saved to database
            print(f"Error enviando email: {email_error}")
        
        return JsonResponse({
            'success': True,
            'message': '¡Mensaje enviado correctamente! Te contactaré pronto.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error al enviar el mensaje. Inténtalo de nuevo.'
        }, status=400)


def skills_api(request):
    """API endpoint for skills data"""
    skills = Skill.objects.filter(is_featured=True).values(
        'id', 'name', 'icon_url', 'category', 'proficiency_level'
    )
    return JsonResponse({'skills': list(skills)})


def projects_api(request):
    """API endpoint for projects data"""
    projects = Project.objects.filter(is_featured=True).select_related('category').prefetch_related('technologies')
    
    projects_data = []
    for project in projects:
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'detailed_description': project.detailed_description,
            'github_url': project.github_url,
            'demo_url': project.demo_url,
            'category': project.category.name if project.category else None,
            'status': project.status,
            'technologies': [{'name': tech.name, 'icon_url': tech.icon_url} for tech in project.technologies.all()],
            'start_date': project.start_date,
            'end_date': project.end_date,
        })
    
    return JsonResponse({'projects': projects_data})
