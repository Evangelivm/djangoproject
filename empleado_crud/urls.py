from django.urls import path
from .views import EmployeeCreateView, EmployeeListView, EmployeeUpdateView, EmployeeDeleteView, HoursCreateView, WeeklyReportView, PTOCreateView, PTOListView, PTOUpdateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API de Gestion de Empleados",
        default_version='v1',
        description="Se encarga tanto del registro y modificacion de empleados, el numero de horas trabajadas, como tambien de la ceracion y aprobacion de PTOs.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="devysalomon@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/update/<int:id_empleado>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/delete/<int:id_empleado>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('hours/create/', HoursCreateView.as_view(), name='hours-create'),
    path('report/', WeeklyReportView.as_view(), name='employee-report'),
    path('pto/', PTOListView.as_view(), name='pto-list'),
    path('pto/create/', PTOCreateView.as_view(), name='pto-create'),
    path('pto/update/<int:id>/', PTOUpdateView.as_view(), name='pto-aprobated'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
