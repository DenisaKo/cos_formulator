"""
URL configuration for cos_formulator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from formulations.views import home, sign_up, create_formulation_view, profile_view, edit_formulation_view, delete_formulation_view, create_ingredient_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', sign_up, name='register'),
    path('formulations/create/', create_formulation_view, name='create_formulation'),
    path('profile/', profile_view, name='profile'),
    path('formulations/<int:pk>/edit/', edit_formulation_view, name='edit_formulation'),
    path('formulations/<int:pk>/delete/', delete_formulation_view, name='delete_formulation'),
    path('ingredient/create/', create_ingredient_view, name='create_ingredient')
]
