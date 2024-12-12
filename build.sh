#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p staticfiles
mkdir -p media

# Limpiar archivos estáticos existentes
python manage.py collectstatic --clear --noinput

# Recolectar archivos estáticos sin procesar mapas de CSS
WHITENOISE_KEEP_ONLY_HASHED_FILES=True python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate 