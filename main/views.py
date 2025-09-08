# cast/views.py

from django.http import JsonResponse
from django.db import connections
import redis
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt
def custom_image_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        upload_name = default_storage.save(upload.name, ContentFile(upload.read()))
        upload_url = default_storage.url(upload_name)
        return JsonResponse({'url': upload_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def health_check(request):
    # Check Database Connection
    try:
        connections['default'].cursor()
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': 'Database connection failed', 'details': str(e)}, status=500)
    
    # Check Redis Connection
    try:
        redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
        redis_port = os.environ.get('REDIS_PORT', '6379')
        r = redis.Redis(host=redis_host, port=redis_port, db=0)
        r.ping()
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': 'Redis connection failed', 'details': str(e)}, status=500)
    
    # Additional checks (e.g., RabbitMQ) can be added here
    
    return JsonResponse({'status': 'healthy'})
