from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomerSignUpForm, SellerSignUpForm
from .models import User
from products.models import Product, Category

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')

class SellerSignUpView(CreateView):
    model = User
    form_class = SellerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'seller'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('users:dashboard')

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    if request.user.is_seller:
        # Seller Dashboard Logic
        my_products = Product.objects.filter(seller=request.user)
        context = {
            'my_products': my_products,
            'total_sales': 0, # Placeholder
            'revenue': 0, # Placeholder
        }
        return render(request, 'users/seller_dashboard.html', context)
    else:
        # Customer Dashboard Logic
        # (Orders would go here)
        context = {
            'recent_orders': [], 
        }
        return render(request, 'users/customer_dashboard.html', context)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user
