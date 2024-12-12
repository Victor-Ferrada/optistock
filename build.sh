#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p staticfiles
mkdir -p media

# Copiar la base de datos SQLite si existe en el directorio de construcción
if [ -f db.sqlite3 ]; then
    cp db.sqlite3 $RENDER_RUNTIME_DIR/
fi

# Recolectar archivos estáticos
python manage.py collectstatic --no-input --clear

# Ejecutar migraciones
python manage.py migrate 