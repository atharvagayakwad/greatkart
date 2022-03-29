from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_to_cart/<slug:product_id>/', views.add_to_cart, name="add-to-cart"),
    path('remove_from_cart/<slug:product_id>/<slug:cart_item_id>/', views.remove_from_cart, name="remove-from-cart"),
    path('delete_from_cart/<slug:product_id>/<slug:cart_item_id>/', views.delete_from_cart, name="delete-from-cart"),
    path('checkout/', views.checkout, name="checkout"),

]