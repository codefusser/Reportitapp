from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static



# from RIT.views import index
from . import views

urlpatterns = [
    path('', views.WebApp.redirect_route, name='redirect_route'),
    #path('RIT/', views.WebApp.index, name='index'),
    path('RIT/login/', views.WebApp.login, name='login'),
    path('RIT/register/', views.WebApp.register, name='register'),
    path('RIT/', views.WebApp.dashboard, name='dashboard'),
    path('RIT/incidentForm/', views.WebApp.incident_form, name='incidentForm'),
    path('RIT/resolveIncident/', views.WebApp.resolve_incident, name='resolve_incident'),
    path('RIT/<str:department>/', views.WebApp.dept_dashboard, name='dept_dashboard'),
    path('RIT/incidentStatus/', views.WebApp.incident_status, name='incident_status'),
    path('RIT/updateIncident/', views.WebApp.update_incident, name='update_incident'),
    path('RIT/logout', views.WebApp.logout, name='logout')
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
