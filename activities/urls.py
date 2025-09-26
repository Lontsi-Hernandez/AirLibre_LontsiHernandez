"""
URL configuration for AirLibre_LontsiHernandez project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
     path('signup/', views.signup, name='signup'),
    path('connexion/', views.connexion, name='connexion'),
    path("logout/", views.deconnexion, name="deconnexion"),
    path('toutes_activites/', views.toutes_activites, name='toutes_activites'),
    path('mes_activites/<int:id>/', views.mes_activites, name='mes_activites'),
    path('new/', views.ajouter_activite, name='ajouter_activite'),
    path('s_inscrire/<int:id>/<int:id_u>/', views.s_inscrire, name='s_inscrire'),
    path('se_desinscrire/<int:id>/', views.se_desinscrire, name='se_desinscrire'),
    path('mes_inscriptions/<int:id>/', views.mes_inscriptions, name='mes_inscriptions'),
    path('<str:location_city>/<int:id>/', views.activity_detail, name='activity_detail'),
    path('profil/', views.profil, name='profil'),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
