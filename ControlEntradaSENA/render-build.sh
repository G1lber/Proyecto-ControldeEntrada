
# Render build script

echo "Aplicando migraciones..."
python manage.py migrate

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput
    