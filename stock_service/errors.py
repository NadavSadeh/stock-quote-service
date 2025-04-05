from django.http import JsonResponse


def custom_404(request, exception):
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found on this server.'
    }, status=404, content_type="application/json")

def custom_500(request):
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.'
    }, status=500, content_type="application/json")
