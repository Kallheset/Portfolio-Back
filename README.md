# Portfolio Personal - Argenis Manzanares

Portfolio web desarrollado con Django para mostrar habilidades, proyectos y experiencia profesional como desarrollador backend en Python.

## 🚀 Características

- **Responsive Design**: Adaptado para dispositivos móviles y desktop
- **Tema Oscuro/Claro**: Toggle entre modos con persistencia en localStorage
- **Gestión de Contenido**: Admin de Django para administrar proyectos y habilidades
- **API REST**: Endpoints para obtener datos de habilidades y proyectos
- **Formulario de Contacto**: Sistema de mensajes con almacenamiento en base de datos
- **Animaciones**: Efectos suaves con AOS (Animate On Scroll)

## 🛠️ Tecnologías

- **Backend**: Django 5.2.5
- **Frontend**: TailwindCSS (via CDN), HTML5, JavaScript ES6
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Iconos**: DevIcons CDN
- **Animaciones**: AOS Library
- **Código**: Optimizado siguiendo estándares SOLID y DRY

## 📋 Requisitos

- Python 3.8+
- Django 5.2+
- Navegador web moderno

## ⚡ Instalación y Uso

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Kallheset/Portfolio-Back.git
   cd Portfolio-Back
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala Django**
   ```bash
   pip install django
   ```

4. **Aplica las migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Populate con datos iniciales**
   ```bash
   python manage.py populate_portfolio
   ```

6. **Crea un superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecuta el servidor**
   ```bash
   python manage.py runserver
   ```

8. **Visita http://localhost:8000**

## 📁 Estructura del Proyecto

```
Portfolio-Back/
├── config/                 # Configuración de Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # WSGI config
├── core/                  # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y API endpoints
│   ├── admin.py          # Configuración del admin
│   └── management/       # Comandos personalizados
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   └── portfolio.html    # Contenido principal
├── static/               # Archivos estáticos
└── db.sqlite3           # Base de datos
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
- `GET /api/skills/` - Lista de habilidades
- `GET /api/projects/` - Lista de proyectos
- `POST /contact/` - Envío de mensajes de contacto

### Comandos Personalizados
```bash
# Poblar con datos de ejemplo
python manage.py populate_portfolio

# Actualizar datos existentes
python manage.py populate_portfolio --force
```

## 🎨 Personalización

1. **Datos personales**: Modifica `core/management/commands/populate_portfolio.py`
2. **Estilos**: Ajusta las clases de TailwindCSS en los templates
3. **CV**: Coloca tu CV en `static/cv/Argenis_Manzanares_CV.pdf`
4. **Configuración**: Actualiza `config/settings.py` para producción

## 📱 Características Responsive

- Navegación móvil con menú hamburguesa
- Grid adaptativo para proyectos
- Formularios optimizados para móvil
- Toggle de tema accesible en todos los dispositivos

## 🚢 Despliegue

Para producción, recuerda:

1. Configurar `STATIC_ROOT` en settings.py
2. Cambiar `SECRET_KEY` y `DEBUG = False`
3. Configurar base de datos de producción
4. Configurar servidor web para archivos estáticos

## 📄 Licencia

Este proyecto es de uso personal y educativo.

## 📧 Contacto

- **Email**: argenis010@gmail.com
- **GitHub**: [@Kallheset](https://github.com/Kallheset)
- **LinkedIn**: [Argenis Manzanares](https://www.linkedin.com/in/argenis-manzanares-108b4a349/)