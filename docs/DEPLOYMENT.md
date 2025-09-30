# =€ Guía de Deployment - Portfolio Django

Esta guía describe los pasos para desplegar el portfolio en diferentes entornos.

## =Ë Tabla de Contenidos

- [Prerequisitos](#prerequisitos)
- [Configuración Inicial](#configuración-inicial)
- [Deployment Local](#deployment-local-desarrollo)
- [Deployment en Producción](#deployment-en-producción)
- [Deployment en Railway/Render](#deployment-en-railwayrender)
- [Post-Deployment](#post-deployment)
- [Troubleshooting](#troubleshooting)

---

## =' Prerequisitos

- Python 3.11+
- Git
- pip y virtualenv
- PostgreSQL (para producción)
- Redis (opcional, para cache en producción)

---

## ™ Configuración Inicial

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd proyecto-portafolio
```

### 2. Crear entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
```

**Variables importantes:**
- `SECRET_KEY`: Generar nueva clave secreta
- `DEBUG`: True para desarrollo, False para producción
- `ALLOWED_HOSTS`: Dominios permitidos
- `EMAIL_HOST_PASSWORD`: Contraseña de aplicación de Gmail

---

## =» Deployment Local (Desarrollo)

### 1. Aplicar migraciones

```bash
python manage.py migrate
```

### 2. Crear superusuario

```bash
python manage.py createsuperuser
```

### 3. Poblar datos iniciales (opcional)

```bash
python manage.py populate_portfolio
```

### 4. Recolectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 5. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a: http://localhost:8000

---

## < Deployment en Producción

### Configuración General

1. **Generar SECRET_KEY nueva:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. **Configurar .env para producción:**

```env
DEBUG=False
SECRET_KEY=<tu-secret-key-generada>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DJANGO_SETTINGS_MODULE=config.settings.production

# Base de datos PostgreSQL
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=<password-segura>
DB_HOST=localhost
DB_PORT=5432

# Email SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_PASSWORD=<tu-app-password>

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

3. **PostgreSQL Setup:**

```bash
# Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres psql
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

4. **Instalar dependencias de producción:**

```bash
pip install psycopg2-binary gunicorn whitenoise
```

5. **Aplicar migraciones:**

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

6. **Ejecutar con Gunicorn:**

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## =‚ Deployment en Railway/Render

### Railway

1. **Crear cuenta en Railway.app**

2. **Crear nuevo proyecto desde GitHub**

3. **Agregar PostgreSQL:**
   - Add Service ’ Database ’ PostgreSQL

4. **Configurar variables de entorno:**

```env
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<generar-nueva>
ALLOWED_HOSTS=*.railway.app
DATABASE_URL=<se configura automáticamente>
```

### Render

1. **Crear cuenta en Render.com**

2. **Crear Web Service desde GitHub**

3. **Configurar:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`

4. **Agregar PostgreSQL:**
   - New ’ PostgreSQL

5. **Variables de entorno:**

```env
PYTHON_VERSION=3.11
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<generar-nueva>
DATABASE_URL=<de PostgreSQL>
```

---

##  Post-Deployment

### 1. Verificar deployment

```bash
# Verificar que el sitio carga
curl https://tudominio.com

# Verificar admin
curl https://tudominio.com/admin/
```

### 2. Configurar HTTPS

**Con Let's Encrypt + Nginx:**

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

### 3. Configurar monitoreo

- Configurar logs centralizados (Sentry, LogDNA)
- Configurar alertas de errores
- Monitoreo de uptime (UptimeRobot, Pingdom)

---

## =
 Troubleshooting

### Error: "DisallowedHost"

```python
# Verificar ALLOWED_HOSTS en .env
ALLOWED_HOSTS=tudominio.com,www.tudominio.com,localhost
```

### Error: "Static files not found"

```bash
# Recolectar estáticos nuevamente
python manage.py collectstatic --noinput --clear
```

### Error: "Database connection failed"

```bash
# Verificar variables de entorno
echo $DATABASE_URL

# Verificar que PostgreSQL está corriendo
sudo service postgresql status
```

### Error: "500 Internal Server Error"

```bash
# Ver logs en logs/errors.log
# Verificar DEBUG=False en producción
```

---

## =Ú Recursos Adicionales

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

**Última actualización:** 2025-01-30
