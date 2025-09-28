from django.urls import path
from . import views

urlpatterns = [
    path('cargar-fichero/', views.cargar_fichero, name='cargar_fichero'),
]