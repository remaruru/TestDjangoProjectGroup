from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomerSignUpForm, SellerSignUpForm
from .models import User
from products.models import Product, Category
from orders.models import Order, Notification

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

def social_role_select(request):
    """View to show role selection when registering via Google / Social"""
    # Simply rendering the signup choice template
    return render(request, 'registration/signup.html', {
        'is_social_auth': True,
        'social_title': 'Complete Your Registration'
    })

def set_role_customer(request):
    user_id = request.session.get('partial_pipeline_user_id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
        user.is_customer = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        del request.session['partial_pipeline_user_id']
        messages.success(request, "Account created! Welcome to NovaMarket.")
        return redirect('home')
    return redirect('users:signup')

def set_role_seller(request):
    user_id = request.session.get('partial_pipeline_user_id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
        user.is_seller = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        del request.session['partial_pipeline_user_id']
        messages.success(request, "Seller account created! Welcome to your Dashboard.")
        return redirect('users:dashboard')
    return redirect('users:signup')


@login_required
def dashboard(request):
    
    if request.user.is_seller:
        # Seller Dashboard Logic
        my_products = Product.objects.filter(seller=request.user)
        # Pending Offers for the seller
        pending_offers = Order.objects.filter(seller=request.user, status='PENDING')
        recent_sales = Order.objects.filter(seller=request.user).exclude(status='PENDING')[:10]
        
        # Calculate revenue (simple sum of confirmed/shipped/completed orders)
        revenue = sum(o.total_price for o in Order.objects.filter(seller=request.user, status__in=['CONFIRMED', 'SHIPPED', 'COMPLETED']))
        
        context = {
            'my_products': my_products,
            'pending_offers': pending_offers,
            'recent_sales': recent_sales,
            'total_sales': recent_sales.count(),
            'revenue': revenue,
        }
        return render(request, 'users/seller_dashboard.html', context)
    else:
        # Customer Dashboard Logic
        my_orders = Order.objects.filter(customer=request.user)
        
        context = {
            'my_orders': my_orders,
        }
        return render(request, 'users/customer_dashboard.html', context)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user
