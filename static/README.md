# Directorio de Archivos Estáticos

Este directorio contiene todos los archivos estáticos del portfolio:

## Estructura recomendada:
```
static/
├── css/          # Archivos CSS personalizados
├── js/           # JavaScript personalizado  
├── images/       # Imágenes del portfolio
├── cv/           # Curriculum Vitae
└── icons/        # Iconos y logos
```

## CV (Curriculum Vitae)
- **Ubicación requerida:** `static/cv/Argenis_Manzanares_CV.pdf`
- El botón de descarga en `templates/base.html` apunta a esta ruta
- Si cambias el nombre del archivo, actualiza la configuración en el modelo `PortfolioSettings`

## Notas importantes:
- Los archivos aquí son servidos directamente por Django en desarrollo
- En producción, usa un servidor web (nginx/apache) para servir archivos estáticos
- Configura `STATIC_ROOT` en settings.py para producción

