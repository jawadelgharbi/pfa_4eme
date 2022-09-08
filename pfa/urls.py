"""pfa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from AiMark import views
from auth import views as views2
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('admins', views.index),
    path('admins/marks/add', views.ajouter),
    path('admins/marks/edit/<int:id>', views.modifier),
    path('admins/marks/delete', views.supprimer),
    # path('search', views.search),

    path('admins/marks/points/add/<int:id>', views.ajouterpoint),
    path('admins/marks/points/delete/<int:id>', views.supprimerpoint),

    path('admins/login', views2.loginauth),
    path('admins/loginclick', views2.loginclick),
    path('admins/logoutclick', views2.logoutclick)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
