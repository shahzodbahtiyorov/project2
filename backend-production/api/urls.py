from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from api.app import redirect_to_custom_scheme
from api.main_view import view_main, fallback_html, get_cloudgate_data


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', view_main),
    path('get-cloudgate/', get_cloudgate_data),
    path('secret-admin/', admin.site.urls),
    path('api/v1/', include('v1.urls')),
    path('sentry-debug/', trigger_error),
    path('dashboard/', include('ubank_auth_server.urls')),

] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
