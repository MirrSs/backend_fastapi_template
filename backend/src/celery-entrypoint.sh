echo "Celery staring"

exec celery -A services.celery_service worker --loglevel=INFO