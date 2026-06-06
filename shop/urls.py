from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produit/<int:id>/', views.detail_produit, name='detail_produit'),
    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:produit_id>/', views.cart_add, name='cart_add'),
    path('panier/supprimer/<int:produit_id>/', views.cart_remove, name='cart_remove'),
    path('panier/modifier/<int:produit_id>/', views.cart_update, name='cart_update'), # Nouvelle ligne
    path('panier/vider/', views.cart_clear, name='cart_clear'),                       # Nouvelle ligne
]