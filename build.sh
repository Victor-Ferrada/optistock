#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p staticfiles
mkdir -p media

# Recolectar archivos estáticos
python manage.py collectstatic --no-input --clear

# Crear base de datos si no existe
if [ ! -f db.sqlite3 ]; then
    python manage.py migrate
fi 