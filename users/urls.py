from django.urls import path, include
from .views import (SignUpView, CustomerSignUpView, SellerSignUpView, 
                    home)

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/seller/', SellerSignUpView.as_view(), name='seller_signup'),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
