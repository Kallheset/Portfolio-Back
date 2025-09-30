# 🎯 Portfolio Personal - Argenis Manzanares

Portfolio web profesional desarrollado con Django para mostrar habilidades, proyectos y experiencia profesional como desarrollador backend en Python.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Características

### Funcionalidades Core
- **🎨 Responsive Design**: Adaptado para dispositivos móviles y desktop
- **🌓 Tema Oscuro/Claro**: Toggle entre modos con persistencia en localStorage
- **⚙️ Gestión de Contenido**: Admin de Django para administrar proyectos y habilidades
- **🔌 API REST**: Endpoints con paginación y filtros para habilidades y proyectos
- **📧 Formulario de Contacto**: Sistema de mensajes con validación y almacenamiento en BD
- **✨ Animaciones**: Efectos suaves con AOS (Animate On Scroll)

### Optimizaciones y Seguridad
- **⚡ Performance**:
  - Cache integrado (LocMem/Redis)
  - Queries optimizadas con select_related/prefetch_related
  - Paginación en APIs
  - Static files comprimidos (WhiteNoise)

- **🔒 Seguridad**:
  - CSRF protection habilitado
  - Validaciones robustas en modelos y vistas
  - Middleware personalizado para manejo de errores
  - Configuración por ambiente (dev/prod)
  - Headers de seguridad configurados

- **📊 Logging**: Sistema estructurado de logs con rotación automática

- **✅ Testing**: Suite completa de tests unitarios y de integración

- **🎯 Code Quality**: Pre-commit hooks (Black, isort, flake8)

## 🛠️ Stack Tecnológico

### Backend
- **Django 5.2.5**: Framework web principal
- **Django REST Framework**: APIs RESTful
- **django-environ**: Gestión de variables de entorno
- **Gunicorn**: WSGI server para producción
- **WhiteNoise**: Servir archivos estáticos

### Frontend
- **TailwindCSS**: Framework CSS (via CDN)
- **HTML5 & JavaScript ES6**: Validaciones y interactividad
- **AOS Library**: Animaciones on-scroll
- **DevIcons CDN**: Iconos de tecnologías

### Base de Datos
- **SQLite**: Desarrollo local
- **PostgreSQL**: Recomendado para producción

### Testing & Quality
- **pytest & pytest-django**: Testing framework
- **Black**: Code formatter
- **isort**: Import sorting
- **flake8**: Linting

## 📋 Requisitos

- Python 3.11+
- Django 5.2+
- pip y virtualenv
- PostgreSQL 15+ (opcional, para producción)
- Redis (opcional, para cache en producción)

## ⚡ Instalación Rápida

### Desarrollo Local

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Kallheset/Portfolio-Back.git
   cd Portfolio-Back
   ```

2. **Crea y activa entorno virtual**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura variables de entorno**
   ```bash
   # Copia el archivo de ejemplo
   cp .env.example .env

   # Edita .env con tus valores (opcional para desarrollo local)
   ```

5. **Crea directorios necesarios**
   ```bash
   mkdir -p logs static/cv media
   ```

6. **Aplica migraciones**
   ```bash
   python manage.py migrate
   ```

7. **Carga datos iniciales**
   ```bash
   python manage.py populate_portfolio
   ```

8. **Crea un superusuario**
   ```bash
   python manage.py createsuperuser
   ```

9. **Recolecta archivos estáticos**
   ```bash
   python manage.py collectstatic --noinput
   ```

10. **Ejecuta el servidor de desarrollo**
    ```bash
    python manage.py runserver
    ```

11. **Abre en el navegador**
    - Portfolio: http://localhost:8000
    - Admin: http://localhost:8000/admin

### Instalación con Pre-commit Hooks (Recomendado)

```bash
# Instalar pre-commit hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 📁 Estructura del Proyecto

```
proyecto-portafolio/
├── config/                      # Configuración Django
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             # Settings base
│   │   ├── development.py      # Settings desarrollo
│   │   └── production.py       # Settings producción
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
├── core/                        # Aplicación principal
│   ├── models.py               # Modelos de datos
│   ├── views.py                # Vistas y API endpoints
│   ├── admin.py                # Configuración del admin
│   ├── tests.py                # Tests unitarios
│   ├── middleware/             # Middleware personalizado
│   │   ├── __init__.py
│   │   └── error_handler.py
│   └── management/
│       └── commands/
│           └── populate_portfolio.py
├── templates/                   # Templates HTML
│   ├── base.html               # Template base
│   ├── portfolio.html          # Contenido principal
│   ├── 404.html                # Error 404
│   └── 500.html                # Error 500
├── static/                      # Archivos estáticos
│   └── cv/                     # CVs en PDF
├── staticfiles/                 # Archivos estáticos recolectados
├── media/                       # Archivos subidos por usuarios
├── logs/                        # Logs de la aplicación
├── docs/                        # Documentación
│   └── DEPLOYMENT.md           # Guía de deployment
├── .env.example                 # Ejemplo de variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── .pre-commit-config.yaml      # Configuración pre-commit hooks
├── requirements.txt             # Dependencias Python
├── pyproject.toml              # Configuración Black/isort
├── setup.cfg                    # Configuración flake8/pytest
├── manage.py                    # CLI de Django
└── db.sqlite3                  # Base de datos (desarrollo)
```

## 🎯 Funcionalidades Principales

### Modelos de Datos (Optimizados)
- **Skill**: Habilidades técnicas con categorías, niveles y años de experiencia
- **Project**: Proyectos con tecnologías, enlaces, fechas e imágenes destacadas
- **ProjectCategory**: Categorías de proyectos con colores personalizados
- **Experience**: Experiencia laboral, educación y certificaciones
- **ContactMessage**: Mensajes con notas de administrador y seguimiento
- **PortfolioSettings**: Configuración general del sitio (patrón Singleton)

#### Características Avanzadas de los Modelos
- **Validaciones robustas** con `clean()` methods y database constraints
- **Índices optimizados** para consultas frecuentes
- **Properties y class methods** para consultas reutilizables
- **Docstrings completos** siguiendo estándares de documentación
- **Estructura SOLID** con separación clara de responsabilidades

### API Endpoints

#### Skills API
```bash
GET /api/skills/                    # Lista todas las habilidades
GET /api/skills/?page=2             # Paginación
GET /api/skills/?category=language  # Filtrar por categoría
GET /api/skills/?page_size=20       # Tamaño de página personalizado
```

**Respuesta:**
```json
{
  "success": true,
  "skills": [
    {
      "id": 1,
      "name": "Python",
      "icon_url": "https://...",
      "category": "language",
      "proficiency_level": 4,
      "years_experience": 5
    }
  ],
  "pagination": {
    "page": 1,
    "total_pages": 2,
    "total_items": 15,
    "has_next": true,
    "has_previous": false
  }
}
```

#### Projects API
```bash
GET /api/projects/                      # Lista todos los proyectos
GET /api/projects/?page=1               # Paginación
GET /api/projects/?category=web         # Filtrar por categoría
GET /api/projects/?status=completed     # Filtrar por estado
```

#### Contact Form
```bash
POST /contact/
Content-Type: application/json

{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "subject": "Consulta",
  "message": "Hola, me gustaría contactarte..."
}
```

### Comandos Personalizados

```bash
# Poblar con datos de ejemplo
python manage.py populate_portfolio

# Actualizar datos existentes (forzar)
python manage.py populate_portfolio --force

# Ejecutar tests
pytest

# Ejecutar tests con coverage
pytest --cov=core --cov-report=html

# Formatear código con Black
black .

# Ordenar imports
isort .

# Linting con flake8
flake8 .
```

## 🎨 Personalización

### Configuración Básica

1. **Variables de entorno** (`.env`):
   ```env
   SECRET_KEY=tu-secret-key-aqui
   DEBUG=False
   ALLOWED_HOSTS=tudominio.com,www.tudominio.com
   EMAIL_HOST_PASSWORD=tu-app-password
   ```

2. **Datos personales**: Edita `core/management/commands/populate_portfolio.py`

3. **Estilos**: Modifica clases TailwindCSS en `templates/base.html` y `templates/portfolio.html`

4. **CV**: Coloca tu CV en `static/cv/Tu_Nombre_CV.pdf`

### Configuración Avanzada

5. **Settings por ambiente**: Edita archivos en `config/settings/`
   - `base.py`: Configuración compartida
   - `development.py`: Desarrollo local
   - `production.py`: Producción

6. **Middleware**: Agrega middleware personalizado en `core/middleware/`

7. **Cache**: Configura Redis en producción (ver `config/settings/production.py`)

## 📱 Características Responsive

- ✅ Navegación móvil con menú hamburguesa animado
- ✅ Grid adaptativo para proyectos (1-3 columnas según dispositivo)
- ✅ Formularios optimizados para móvil
- ✅ Toggle de tema accesible en todos los dispositivos
- ✅ Imágenes responsive y optimizadas
- ✅ Tipografía fluida y legible en pantallas pequeñas

## 🚢 Deployment

### Guía Rápida

Ver documentación completa en [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)

**Pasos básicos para producción:**

1. **Configura variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env con valores de producción
   ```

2. **Genera SECRET_KEY nueva**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Configura base de datos PostgreSQL**
   ```env
   DB_NAME=portfolio_db
   DB_USER=portfolio_user
   DB_PASSWORD=secure_password
   ```

4. **Aplica migraciones y recolecta estáticos**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. **Ejecuta con Gunicorn**
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```

### Plataformas Recomendadas

- **Railway**: Deployment automático desde GitHub
- **Render**: Free tier con PostgreSQL incluido
- **Heroku**: Fácil configuración con Procfile
- **VPS (DigitalOcean, AWS)**: Control total

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=core --cov-report=html

# Tests específicos
pytest core/tests.py::SkillModelValidationTests

# Ver reporte de coverage
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```

**Coverage actual**: Tests cubren modelos, vistas, APIs y validaciones

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Asegúrate de que los tests pasen (`pytest`)
4. Formatea el código (`black . && isort .`)
5. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
6. Push a la rama (`git push origin feature/AmazingFeature`)
7. Abre un Pull Request

## 📝 Changelog

### v2.0.0 (2025-01-30)
- ✨ Implementado sistema de configuración por ambientes
- ✨ Agregado sistema de cache con soporte Redis
- ✨ APIs con paginación y filtros
- ✨ Middleware personalizado para manejo de errores
- ✨ Sistema de logging estructurado
- ✨ Pre-commit hooks (Black, isort, flake8)
- ✨ Templates de error 404 y 500
- ✨ Documentación completa de deployment
- 🔒 Mejorada seguridad del formulario de contacto (CSRF)
- ⚡ Queries optimizadas (N+1 solucionado)
- 🧪 Suite completa de tests unitarios
- 📚 README ampliado con documentación detallada

### v1.0.0 (2024-12-15)
- 🎉 Release inicial
- Modelos de datos optimizados
- Admin interface personalizada
- API REST básica
- Sistema de temas claro/oscuro

## 📄 Licencia

Este proyecto es de uso personal y educativo.

## 📧 Contacto

**Argenis Manzanares**
- 📧 Email: [argenis010@gmail.com](mailto:argenis010@gmail.com)
- 💼 LinkedIn: [Argenis Manzanares](https://www.linkedin.com/in/argenis-manzanares-108b4a349/)
- 🐙 GitHub: [@Kallheset](https://github.com/Kallheset)
- 🌐 Portfolio: [Ver demo](https://tudominio.com)

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Desarrollado con ❤️ y ☕ por Argenis Manzanares

</div>
