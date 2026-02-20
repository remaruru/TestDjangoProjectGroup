from django.shortcuts import render, get_object_or_404
from .models import Product, Category

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
        'selected_category': category_slug
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/product_detail.html', context)
