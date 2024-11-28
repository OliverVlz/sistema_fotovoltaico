from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_electrodomesticos, name='lista_electrodomesticos'),
    path('agregar/', views.agregar_electrodomestico, name='agregar_electrodomestico'),
    path('editar/<int:pk>/', views.EditarElectrodomestico.as_view(), name='editar_electrodomestico'),
    path('eliminar/<int:pk>/', views.eliminar_electrodomestico, name='eliminar_electrodomestico'),
    path('editar_configuracion/', views.editar_configuracion, name='editar_configuracion'),
    path('resultados/', views.resultados, name='resultados'),
]
