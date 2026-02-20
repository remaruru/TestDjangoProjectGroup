from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('action/<int:order_id>/<str:action>/', views.order_action, name='order_action'),
]
