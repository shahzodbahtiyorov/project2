from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from v1.services.bill import generate_pdf
from v1.views import jsonrpc, meaning, backend
from django.conf import settings
from django.conf.urls.static import static

from v1.services.auth import CreateStaff, UserLogin, PasswordChangeView, AdminPasswordChangeView, CreateDashboardStaff
from v1.services.dashboard import AccountView, ChartView, GetOrCreateBankClient, GetClient, \
    GetClientAccounts, GetExistingAcc, GetMfo, GetAccountHistory, ClientAccounts, GetTransactions
from v1.services.notifications import SendToDeviceView, SendTopicView, NewsView
from v1.services.permissions import CreatePermission, CreateRoleView, PermissionToRoleView, UserRoleView

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Description of your API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url='https://unired-business-test.cloudgate.uz/',
)

urlpatterns = [
          path('jsonrpc', jsonrpc),
          path('backend', backend),
          path('withoutmeaning', meaning),
          path('bill', generate_pdf),
          path('staff/management', CreateStaff.as_view()),
          path('staff/management/<int:pk>/', CreateStaff.as_view()),
          path('user/login/', UserLogin.as_view()),
          path('change/password/', PasswordChangeView.as_view()),
          path('change/admin-password/', AdminPasswordChangeView.as_view()),

          path('get-account-history/<int:pk>', GetAccountHistory.as_view()),
          path('get-account-history/<int:pk>/<int:tr_id>/', GetAccountHistory.as_view()),
          path('get-account-history/<int:pk>/<str:begin>/', GetAccountHistory.as_view()),
          path('get-account-history/<int:pk>/<str:begin>/<str:end>/', GetAccountHistory.as_view()),

          path('company/account/', AccountView.as_view()),
          path('company/account/<int:pk>', AccountView.as_view()),

          path('get-filials/', GetMfo.as_view()),

          path('get-transaction/<int:pk>', GetTransactions.as_view()),

          path('device/notification/', SendToDeviceView.as_view()),
          path('topic/notification/', SendTopicView.as_view()),

          path('news/', NewsView.as_view()),
          path('news/<int:pk>', NewsView.as_view()),

          path('permissions/', CreatePermission.as_view()),
          path('permissions/<int:pk>', CreatePermission.as_view()),

          path('user-role/', CreateRoleView.as_view()),
          path('user-role/<int:pk>', CreateRoleView.as_view()),

          path('role-permission/', PermissionToRoleView.as_view()),
          path('role-permission/<int:pk>', PermissionToRoleView.as_view()),

          path('role-to-user/', UserRoleView.as_view()),

          path('chart-graph/', ChartView.as_view()),

          path('client-register/', GetOrCreateBankClient.as_view()),
          path('client-register/<int:pk>', GetOrCreateBankClient.as_view()),

          path('get-client/', GetClient.as_view()),
          path('get-client/<int:pk>', GetClient.as_view()),

          path('get-client-account/<int:pk>', GetClientAccounts.as_view()),
          path('get-client-account/', GetClientAccounts.as_view()),

          path('get-existing-account/<int:pk>', GetExistingAcc.as_view()),

          path('get-accounts/', ClientAccounts.as_view()),

          path('dashboard-staff/', CreateDashboardStaff.as_view()),
          path('dashboard-staff/<int:pk>', CreateDashboardStaff.as_view()),

          re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                  name='schema-json'),
          re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
          re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
