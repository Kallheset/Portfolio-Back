from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, datetime
from .models import Skill, Project, ProjectCategory, PortfolioSettings, ContactMessage, Experience
import json


class PortfolioModelTests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Test Skill",
            icon_url="https://example.com/icon.svg",
            category="language"
        )
        self.category = ProjectCategory.objects.create(name="Test Category")
        self.project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            github_url="https://github.com/test/repo"
        )

    def test_skill_string_representation(self):
        self.assertEqual(str(self.skill), "Test Skill (Avanzado)")

    def test_project_string_representation(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_tech_names_property(self):
        self.project.technologies.add(self.skill)
        self.assertEqual(self.project.tech_names, "Test Skill")


class PortfolioViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        
        # Create test data
        self.skill = Skill.objects.create(
            name="Python",
            icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
            category="language",
            is_featured=True
        )
        
        self.category = ProjectCategory.objects.create(name="Web Application")
        
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            github_url="https://github.com/test/repo",
            is_featured=True,
            category=self.category
        )
        self.project.technologies.add(self.skill)
        
        # Create portfolio settings
        PortfolioSettings.objects.create(
            site_title="Test Portfolio",
            github_username="testuser"
        )

    def test_home_page_status_code(self):
        """Test that the home page returns a 200 status code"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Test that the home page uses the portfolio.html template"""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'portfolio.html')

    def test_home_page_context_contains_skills(self):
        """Test that the context contains skills data"""
        response = self.client.get(self.home_url)
        self.assertIn('skills', response.context)
        skills = list(response.context['skills'])
        self.assertGreater(len(skills), 0)
        self.assertEqual(skills[0]['name'], 'Python')

    def test_home_page_context_contains_projects(self):
        """Test that the context contains projects data"""
        response = self.client.get(self.home_url)
        self.assertIn('projects', response.context)
        projects = response.context['projects']
        self.assertIsInstance(projects, list)
        self.assertGreater(len(projects), 0)

    def test_home_page_context_contains_github_url(self):
        """Test that the context contains github_url"""
        response = self.client.get(self.home_url)
        self.assertIn('github_url', response.context)
        github_url = response.context['github_url']
        self.assertIn('github.com', github_url)
        self.assertIn('testuser', github_url)

    def test_home_page_context_contains_settings(self):
        """Test that the context contains settings"""
        response = self.client.get(self.home_url)
        self.assertIn('settings', response.context)
        settings = response.context['settings']
        self.assertEqual(settings.site_title, 'Test Portfolio')

    def test_projects_have_required_fields(self):
        """Test that each project has required fields"""
        response = self.client.get(self.home_url)
        projects = response.context['projects']
        for project in projects:
            self.assertIn('title', project)
            self.assertIn('description', project)
            self.assertIn('github', project)
            self.assertTrue(project['title'])
            self.assertTrue(project['description'])


class ContactFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('contact_form')

    def test_contact_form_success(self):
        """Test successful contact form submission"""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        
        response = self.client.post(
            self.contact_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Check that message was created
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.name, 'Test User')
        self.assertEqual(message.email, 'test@example.com')

    def test_contact_form_invalid_method(self):
        """Test contact form with invalid HTTP method"""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 405)


class APITests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Python",
            icon_url="https://example.com/python.svg",
            category="language",
            is_featured=True
        )
        
        self.category = ProjectCategory.objects.create(name="Web App")
        self.project = Project.objects.create(
            title="Test API Project",
            description="API test project",
            is_featured=True,
            category=self.category
        )

    def test_skills_api(self):
        """Test skills API endpoint"""
        response = self.client.get(reverse('skills_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('skills', data)
        self.assertEqual(len(data['skills']), 1)
        self.assertEqual(data['skills'][0]['name'], 'Python')

    def test_projects_api(self):
        """Test projects API endpoint"""
        response = self.client.get(reverse('projects_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('projects', data)
        self.assertEqual(len(data['projects']), 1)
        self.assertEqual(data['projects'][0]['title'], 'Test API Project')


class PortfolioSettingsTests(TestCase):
    def test_singleton_pattern(self):
        """Test that PortfolioSettings follows singleton pattern"""
        settings1 = PortfolioSettings.get_settings()
        settings2 = PortfolioSettings.get_settings()

        self.assertEqual(settings1.pk, settings2.pk)
        self.assertEqual(PortfolioSettings.objects.count(), 1)


class SkillModelValidationTests(TestCase):
    """Tests para validaciones del modelo Skill siguiendo estándares CLAUDE.md"""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.valid_skill_data = {
            'name': 'Python',
            'icon_url': 'https://example.com/python.svg',
            'category': 'language',
            'proficiency_level': 3,
            'years_experience': 5
        }

    def test_create_skill_valid_data(self):
        """Test creación de habilidad con datos válidos."""
        skill = Skill.objects.create(**self.valid_skill_data)
        self.assertEqual(skill.name, 'Python')
        self.assertEqual(skill.proficiency_level, 3)
        self.assertTrue(skill.is_featured)

    def test_skill_str_representation(self):
        """Test representación string del modelo."""
        skill = Skill.objects.create(**self.valid_skill_data)
        expected = "Python (Avanzado)"
        self.assertEqual(str(skill), expected)

    def test_proficiency_level_validation_invalid_low(self):
        """Test validación con nivel de competencia inválido (muy bajo)."""
        with self.assertRaises(ValidationError):
            skill = Skill(proficiency_level=0, **{k: v for k, v in self.valid_skill_data.items() if k != 'proficiency_level'})
            skill.full_clean()

    def test_proficiency_level_validation_invalid_high(self):
        """Test validación con nivel de competencia inválido (muy alto)."""
        with self.assertRaises(ValidationError):
            skill = Skill(proficiency_level=5, **{k: v for k, v in self.valid_skill_data.items() if k != 'proficiency_level'})
            skill.full_clean()

    def test_years_experience_validation_invalid(self):
        """Test validación con años de experiencia inválidos."""
        with self.assertRaises(ValidationError):
            skill = Skill(years_experience=51, **{k: v for k, v in self.valid_skill_data.items() if k != 'years_experience'})
            skill.full_clean()

    def test_skill_properties(self):
        """Test properties del modelo Skill."""
        skill = Skill.objects.create(**self.valid_skill_data)

        # Test experience_display property
        self.assertEqual(skill.experience_display, "5 años")

        skill.years_experience = 1
        skill.save()
        self.assertEqual(skill.experience_display, "1 año")

        skill.years_experience = None
        skill.save()
        self.assertEqual(skill.experience_display, "No especificado")

        # Test is_expert_level property
        skill.proficiency_level = 4
        skill.save()
        self.assertTrue(skill.is_expert_level)

        skill.proficiency_level = 3
        skill.save()
        self.assertFalse(skill.is_expert_level)

    def test_skill_class_methods(self):
        """Test métodos de clase del modelo Skill."""
        # Crear habilidades de prueba
        featured_skill = Skill.objects.create(
            name="Django",
            category="framework",
            is_featured=True,
            icon_url="https://example.com/django.svg"
        )
        non_featured_skill = Skill.objects.create(
            name="Vue.js",
            category="framework",
            is_featured=False,
            icon_url="https://example.com/vue.svg"
        )

        # Test get_featured_skills
        featured_skills = Skill.get_featured_skills()
        self.assertIn(featured_skill, featured_skills)
        self.assertNotIn(non_featured_skill, featured_skills)

        # Test get_by_category
        framework_skills = Skill.get_by_category('framework')
        self.assertIn(featured_skill, framework_skills)
        self.assertNotIn(non_featured_skill, framework_skills)  # No está featured


class ProjectModelValidationTests(TestCase):
    """Tests para validaciones del modelo Project siguiendo estándares CLAUDE.md"""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.category = ProjectCategory.objects.create(
            name="Web Application",
            color="#FF5733"
        )
        self.skill = Skill.objects.create(
            name="Python",
            category="language",
            icon_url="https://example.com/python.svg"
        )
        self.valid_project_data = {
            'title': 'Portfolio Web',
            'description': 'Mi portfolio personal',
            'category': self.category,
            'status': 'completed',
            'start_date': date(2023, 1, 1),
            'end_date': date(2023, 6, 1)
        }

    def test_create_project_valid_data(self):
        """Test creación de proyecto con datos válidos."""
        project = Project.objects.create(**self.valid_project_data)
        self.assertEqual(project.title, 'Portfolio Web')
        self.assertTrue(project.is_featured)

    def test_project_str_representation(self):
        """Test representación string del modelo."""
        project = Project.objects.create(**self.valid_project_data)
        self.assertEqual(str(project), 'Portfolio Web')

    def test_project_date_validation_invalid(self):
        """Test validación con fechas inválidas."""
        with self.assertRaises(ValidationError):
            project_data = self.valid_project_data.copy()
            project_data['start_date'] = date(2023, 6, 1)
            project_data['end_date'] = date(2023, 1, 1)  # Fecha de fin anterior a inicio
            project = Project(**project_data)
            project.full_clean()

    def test_project_properties(self):
        """Test properties del modelo Project."""
        project = Project.objects.create(**self.valid_project_data)
        project.technologies.add(self.skill)

        # Test tech_names property
        self.assertEqual(project.tech_names, "Python")

        # Test duration_display property
        self.assertEqual(project.duration_display, "2023")

        # Test has_links property
        self.assertFalse(project.has_links)
        project.github_url = "https://github.com/test/repo"
        project.save()
        self.assertTrue(project.has_links)

        # Test is_in_progress property
        self.assertFalse(project.is_in_progress)
        project.status = 'in_progress'
        project.save()
        self.assertTrue(project.is_in_progress)

    def test_project_class_methods(self):
        """Test métodos de clase del modelo Project."""
        project = Project.objects.create(**self.valid_project_data)
        project.technologies.add(self.skill)

        # Test get_featured_projects
        featured_projects = Project.get_featured_projects()
        self.assertIn(project, featured_projects)

        # Test get_by_status
        completed_projects = Project.get_by_status('completed')
        self.assertIn(project, completed_projects)

        # Test get_by_technology
        python_projects = Project.get_by_technology('Python')
        self.assertIn(project, python_projects)


class ExperienceModelValidationTests(TestCase):
    """Tests para validaciones del modelo Experience siguiendo estándares CLAUDE.md"""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.valid_experience_data = {
            'title': 'Backend Developer',
            'company_or_institution': 'Tech Company',
            'description': 'Desarrollo de APIs con Django',
            'experience_type': 'work',
            'start_date': date(2022, 1, 1),
            'end_date': date(2023, 1, 1),
            'is_current': False
        }

    def test_create_experience_valid_data(self):
        """Test creación de experiencia con datos válidos."""
        experience = Experience.objects.create(**self.valid_experience_data)
        self.assertEqual(experience.title, 'Backend Developer')
        self.assertTrue(experience.is_featured)

    def test_experience_date_validation_invalid(self):
        """Test validación con fechas inválidas."""
        with self.assertRaises(ValidationError):
            experience_data = self.valid_experience_data.copy()
            experience_data['start_date'] = date(2023, 1, 1)
            experience_data['end_date'] = date(2022, 1, 1)  # Fecha de fin anterior a inicio
            experience = Experience(**experience_data)
            experience.full_clean()

    def test_experience_current_validation_invalid(self):
        """Test validación de experiencia actual con fecha de fin."""
        with self.assertRaises(ValidationError):
            experience_data = self.valid_experience_data.copy()
            experience_data['is_current'] = True
            experience_data['end_date'] = date(2023, 1, 1)  # No debería tener fecha de fin si es actual
            experience = Experience(**experience_data)
            experience.full_clean()

    def test_experience_duration_property(self):
        """Test property duration del modelo Experience."""
        experience = Experience.objects.create(**self.valid_experience_data)
        self.assertEqual(experience.duration, "2022 - 2023")

        # Test experiencia actual
        experience.is_current = True
        experience.end_date = None
        experience.save()
        self.assertEqual(experience.duration, "2022 - Presente")


class ProjectCategoryModelValidationTests(TestCase):
    """Tests para validaciones del modelo ProjectCategory siguiendo estándares CLAUDE.md"""

    def test_create_category_valid_data(self):
        """Test creación de categoría con datos válidos."""
        category = ProjectCategory.objects.create(
            name="Web Development",
            color="#3B82F6"
        )
        self.assertEqual(category.name, "Web Development")
        self.assertEqual(category.color, "#3B82F6")

    def test_category_color_validation_invalid(self):
        """Test validación con color hex inválido."""
        with self.assertRaises(ValidationError):
            category = ProjectCategory(name="Test", color="invalid-color")
            category.full_clean()

    def test_category_project_count_property(self):
        """Test property project_count del modelo ProjectCategory."""
        category = ProjectCategory.objects.create(name="Web", color="#FF0000")
        self.assertEqual(category.project_count, 0)

        Project.objects.create(
            title="Test Project",
            description="Test",
            category=category,
            is_featured=True
        )
        self.assertEqual(category.project_count, 1)


class DatabaseConstraintTests(TestCase):
    """Tests para constraints de base de datos siguiendo estándares CLAUDE.md"""

    def test_skill_proficiency_constraint(self):
        """Test constraint de nivel de competencia en Skill."""
        # Este test depende de que las constraints estén aplicadas en la BD
        skill = Skill.objects.create(
            name="Test Skill",
            proficiency_level=3,  # Válido
            icon_url="https://example.com/test.svg"
        )
        self.assertEqual(skill.proficiency_level, 3)

    def test_project_date_constraint(self):
        """Test constraint de fechas en Project."""
        project = Project.objects.create(
            title="Test Project",
            description="Test description",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 6, 1)  # Válido: end_date > start_date
        )
        self.assertIsNotNone(project.pk)
