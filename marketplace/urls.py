from django.urls import path
from . import views

urlpatterns = [

    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    #Add To Cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    #Decrese cart
    path('remove_from_cart/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    #delecte cart item
    path('delete_cart/<int:cart_id>', views.delete_cart, name="delete_cart")
 
]