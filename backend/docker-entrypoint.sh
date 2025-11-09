#!/bin/bash
set -e

echo "⏳ Waiting 25 seconds for network and PostgreSQL..."
sleep 25

echo "✅ Network ready, testing database..."

echo "🔄 Running migrations..."
python manage.py migrate --noinput || {
    echo "❌ Migration failed, retrying in 10s..."
    sleep 10
    python manage.py migrate --noinput
}

echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('ℹ️  Superuser already exists')
" 2>/dev/null || echo "⚠️  Superuser creation skipped"

echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000