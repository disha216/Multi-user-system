"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Login view
    path('signup/', views.signup_view, name='signup'),  # Signup view
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor dashboard view
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),  # Client dashboard view
    path('logout/', views.user_logout, name='logout'),  # Logout view
    path('edit-details/', views.edit_details, name='edit_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)