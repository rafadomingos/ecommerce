from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('fecharpedido/', views.FecharPedido.as_view(), name='fecharpedido'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('detalhe/', views.Detalhe.as_view(), name='detalhe'),
]
