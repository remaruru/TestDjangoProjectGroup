from django.contrib import admin
from django.urls import path, include
from users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),
    path('', home, name='home'),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
