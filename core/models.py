from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError


class Skill(models.Model):
    """
    Modelo para representar habilidades técnicas del portfolio.

    Incluye información sobre tecnologías, frameworks y herramientas
    con niveles de competencia y experiencia en años.
    """

    # Choices constants
    CATEGORY_CHOICES = [
        ('language', 'Lenguaje de Programación'),
        ('framework', 'Framework'),
        ('database', 'Base de Datos'),
        ('tool', 'Herramienta'),
        ('cloud', 'Cloud/DevOps'),
    ]

    PROFICIENCY_CHOICES = [
        (1, 'Básico'),
        (2, 'Intermedio'),
        (3, 'Avanzado'),
        (4, 'Experto'),
    ]

    # 1. Campos de datos principales
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    icon_url = models.URLField(help_text="URL del icono (ej: devicon CDN)")
    years_experience = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Años de experiencia con esta tecnología"
    )

    # 2. Campos de categorización
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='tool',
        verbose_name="Categoría"
    )
    proficiency_level = models.IntegerField(
        default=3,
        choices=PROFICIENCY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Nivel de competencia"
    )

    # 3. Campos de metadata
    is_featured = models.BooleanField(default=True, help_text="Mostrar en el portfolio")
    display_order = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['is_featured']),
            models.Index(fields=['category']),
            models.Index(fields=['display_order']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(proficiency_level__gte=1) & models.Q(proficiency_level__lte=4),
                name='valid_proficiency_level'
            ),
            models.CheckConstraint(
                check=models.Q(years_experience__isnull=True) | models.Q(years_experience__gte=0),
                name='valid_years_experience'
            ),
        ]

    def __str__(self):
        """Representación string del modelo."""
        return f"{self.name} ({self.get_proficiency_level_display()})"

    def clean(self):
        """Validaciones personalizadas del modelo."""
        super().clean()
        if self.years_experience and self.years_experience > 50:
            raise ValidationError('Los años de experiencia no pueden ser mayor a 50')

    def save(self, *args, **kwargs):
        """Override save para validar antes de guardar."""
        self.full_clean()
        super().save(*args, **kwargs)

    # Properties
    @property
    def experience_display(self):
        """Devuelve la experiencia en formato legible."""
        if not self.years_experience:
            return "No especificado"
        if self.years_experience == 1:
            return "1 año"
        return f"{self.years_experience} años"

    @property
    def is_expert_level(self):
        """Indica si la habilidad es de nivel experto."""
        return self.proficiency_level == 4

    # Class methods
    @classmethod
    def get_featured_skills(cls):
        """Devuelve las habilidades destacadas ordenadas."""
        return cls.objects.filter(is_featured=True).order_by('display_order', 'name')

    @classmethod
    def get_by_category(cls, category):
        """Devuelve habilidades filtradas por categoría."""
        return cls.objects.filter(category=category, is_featured=True)


class ProjectCategory(models.Model):
    """
    Categorías para organizar proyectos del portfolio.

    Permite agrupar proyectos por tipo (web, móvil, API, etc.)
    con colores distintivos para la interfaz.
    """

    # 1. Campos de datos principales
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")

    # 2. Campos de presentación
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text="Color hex para la categoría",
        validators=[RegexValidator(
            regex=r'^#[0-9A-Fa-f]{6}$',
            message='Debe ser un color hex válido (ej: #3B82F6)'
        )],
        verbose_name="Color"
    )
    
    class Meta:
        verbose_name = "Categoría de Proyecto"
        verbose_name_plural = "Categorías de Proyecto"
        ordering = ['name']

    def __str__(self):
        """Representación string del modelo."""
        return self.name

    def clean(self):
        """Validaciones personalizadas del modelo."""
        super().clean()
        # Validar que el color sea un hex válido (ya validado por RegexValidator)
        pass

    def save(self, *args, **kwargs):
        """Override save para validar antes de guardar."""
        self.full_clean()
        super().save(*args, **kwargs)

    # Properties
    @property
    def project_count(self):
        """Devuelve el número de proyectos en esta categoría."""
        return self.project_set.filter(is_featured=True).count()

    # Class methods
    @classmethod
    def get_with_projects(cls):
        """Devuelve categorías que tienen al menos un proyecto."""
        return cls.objects.filter(project__is_featured=True).distinct()


class Project(models.Model):
    """
    Modelo para representar proyectos del portfolio.

    Incluye información completa sobre proyectos desarrollados,
    tecnologías utilizadas, enlaces y estado del proyecto.
    """

    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('archived', 'Archivado'),
        ('in_progress', 'En Desarrollo'),
    ]

    # 1. Campos de datos principales
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    detailed_description = models.TextField(
        blank=True,
        help_text="Descripción detallada opcional",
        verbose_name="Descripción detallada"
    )

    # 2. Campos de enlaces
    github_url = models.URLField(blank=True, null=True, verbose_name="URL de GitHub")
    demo_url = models.URLField(blank=True, null=True, verbose_name="URL de Demo")
    featured_image = models.URLField(
        blank=True,
        null=True,
        help_text="URL de imagen destacada del proyecto",
        verbose_name="Imagen destacada"
    )

    # 3. Campos de relación
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría"
    )
    technologies = models.ManyToManyField(
        Skill,
        blank=True,
        help_text="Tecnologías utilizadas",
        verbose_name="Tecnologías"
    )

    # 4. Campos de metadata
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
        verbose_name="Estado"
    )
    is_featured = models.BooleanField(default=True, help_text="Mostrar en el portfolio")
    display_order = models.PositiveIntegerField(default=0, help_text="Orden de visualización")

    # 5. Timestamps
    start_date = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de fin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['is_featured']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['display_order']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__isnull=True) | models.Q(end_date__isnull=True) | models.Q(end_date__gte=models.F('start_date')),
                name='valid_project_dates'
            ),
        ]

    def __str__(self):
        """Representación string del modelo."""
        return self.title

    def clean(self):
        """Validaciones personalizadas del modelo."""
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')

    def save(self, *args, **kwargs):
        """Override save para validar antes de guardar."""
        self.full_clean()
        super().save(*args, **kwargs)

    # Properties
    @property
    def tech_names(self):
        """Devuelve los nombres de tecnologías separados por comas."""
        return ", ".join([tech.name for tech in self.technologies.all()])

    @property
    def duration_display(self):
        """Devuelve la duración del proyecto en formato legible."""
        if not self.start_date:
            return "Fecha no especificada"
        if not self.end_date:
            return f"Desde {self.start_date.strftime('%Y')}"
        if self.start_date.year == self.end_date.year:
            return str(self.start_date.year)
        return f"{self.start_date.strftime('%Y')} - {self.end_date.strftime('%Y')}"

    @property
    def has_links(self):
        """Indica si el proyecto tiene enlaces disponibles."""
        return bool(self.github_url or self.demo_url)

    @property
    def is_in_progress(self):
        """Indica si el proyecto está en desarrollo."""
        return self.status == 'in_progress'

    # Class methods
    @classmethod
    def get_featured_projects(cls):
        """Devuelve proyectos destacados ordenados."""
        return cls.objects.select_related('category').prefetch_related('technologies').filter(
            is_featured=True
        ).order_by('display_order', '-created_at')

    @classmethod
    def get_by_status(cls, status):
        """Devuelve proyectos filtrados por estado."""
        return cls.objects.filter(status=status, is_featured=True)

    @classmethod
    def get_by_technology(cls, technology_name):
        """Devuelve proyectos que usan una tecnología específica."""
        return cls.objects.filter(
            technologies__name__icontains=technology_name,
            is_featured=True
        ).distinct()


class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ('work', 'Experiencia Laboral'),
        ('education', 'Educación'),
        ('certification', 'Certificación'),
        ('volunteer', 'Voluntariado'),
    ]

    title = models.CharField(max_length=200)
    company_or_institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES, default='work')
    
    # Fechas
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Dejar vacío si es actual")
    is_current = models.BooleanField(default=False, help_text="¿Es el trabajo/estudio actual?")
    
    # Tecnologías relacionadas
    technologies = models.ManyToManyField(Skill, blank=True)
    
    # Configuración
    is_featured = models.BooleanField(default=True, help_text="Mostrar en el portfolio")
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"
        ordering = ['display_order', '-start_date']
        indexes = [
            models.Index(fields=['is_featured']),
            models.Index(fields=['experience_type']),
            models.Index(fields=['is_current']),
        ]

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
        if self.is_current and self.end_date:
            raise ValidationError('Una experiencia actual no puede tener fecha de fin')

    def __str__(self):
        return f"{self.title} - {self.company_or_institution}"

    @property
    def duration(self):
        if self.is_current:
            return f"{self.start_date.strftime('%Y')} - Presente"
        elif self.end_date:
            return f"{self.start_date.strftime('%Y')} - {self.end_date.strftime('%Y')}"
        else:
            return self.start_date.strftime('%Y')


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True, help_text="Fecha en que se respondió")
    admin_notes = models.TextField(blank=True, help_text="Notas internas del administrador")

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class PortfolioSettings(models.Model):
    site_title = models.CharField(max_length=200, default="Argenis Manzanares")
    tagline = models.CharField(max_length=300, default="Desarrollador Backend en Python")
    about_me = models.TextField(
        default="Soy programador web backend con experiencia en Python, Django, FastAPI, Flask, SQL y Docker. Estoy enfocado en crear APIs y sistemas escalables."
    )
    email = models.EmailField(default="argenis010@gmail.com")
    github_username = models.CharField(max_length=100, default="Kallheset")
    linkedin_url = models.URLField(default="https://www.linkedin.com/in/argenis-manzanares-108b4a349/")
    cv_file_path = models.CharField(
        max_length=200, 
        default="cv/Argenis_Manzanares_CV.pdf",
        help_text="Ruta relativa desde static/"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio Settings"
        verbose_name_plural = "Portfolio Settings"

    def __str__(self):
        return "Portfolio Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
        return self

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
