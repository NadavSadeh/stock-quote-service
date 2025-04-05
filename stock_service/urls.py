from django.contrib import admin
from django.urls import path, include
from .errors import custom_404, custom_500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quotes.urls')),
]

handler404 = custom_404
handler500 = custom_500
