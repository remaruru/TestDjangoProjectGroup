from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/seller/', views.SellerSignUpView.as_view(), name='seller_signup'),
    
    # Social Auth Role Selection
    path('role-select/', views.social_role_select, name='social_role_select'),
    path('role-select/customer/', views.set_role_customer, name='set_role_customer'),
    path('role-select/seller/', views.set_role_seller, name='set_role_seller'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
