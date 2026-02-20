from django.contrib import admin
from django.urls import path, include
from users.views import home  # We might replace 'home' with our product list view later
from products.views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),
    
    # Use product list as the home page for now, or keep separate 'home' view but update it
    path('', product_list, name='home'), 
    
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
