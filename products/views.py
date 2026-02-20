from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Category
from .forms import ProductForm
from orders.models import Notification

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()
    
    # Simple filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(title__icontains=search_query)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


class SellerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller


class ProductCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        new_cat_name = form.cleaned_data.get('new_category')
        if new_cat_name:
            category, created = Category.objects.get_or_create(
                name=new_cat_name,
                defaults={'slug': slugify(new_cat_name)}
            )
            form.instance.category = category
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        new_cat_name = form.cleaned_data.get('new_category')
        if new_cat_name:
            category, created = Category.objects.get_or_create(
                name=new_cat_name,
                defaults={'slug': slugify(new_cat_name)}
            )
            form.instance.category = category
        return super().form_valid(form)

    def get_queryset(self):
        # Ensure that only the seller who owns the product can edit it
        return super().get_queryset().filter(seller=self.request.user)


class ProductDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('users:dashboard')

    def get_queryset(self):
        # Ensure that only the seller who owns the product can delete it
        return super().get_queryset().filter(seller=self.request.user)

