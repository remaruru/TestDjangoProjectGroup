from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem, Notification
from decimal import Decimal

def get_common_context(request):
    return {}

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item_data['quantity']
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
        except Product.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
        **get_common_context(request)
    }
    return render(request, 'orders/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # LOGIC FIX: Prevent ordering own items
    if request.user.is_authenticated and product.seller == request.user:
        messages.error(request, "You cannot add your own product to the cart.")
        return redirect('products:detail', pk=product_id)
        
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {'quantity': quantity, 'price': str(product.price)}
    
    request.session['cart'] = cart
    messages.success(request, f"{product.title} added to cart.")
    return redirect('orders:cart_detail')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('orders:cart_detail')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('products:list')
    
    # Group by seller
    seller_items = {}
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        
        # Double check self-ordering at checkout
        if product.seller == request.user:
            messages.error(request, f"You cannot order your own product: {product.title}")
            return redirect('orders:cart_detail')
            
        seller = product.seller
        if seller not in seller_items:
            seller_items[seller] = []
        seller_items[seller].append({
            'product': product,
            'quantity': item_data['quantity'],
            'price': product.price
        })
    
    for seller, items in seller_items.items():
        # Create Order (Offer)
        order = Order.objects.create(
            customer=request.user,
            seller=seller,
            status='PENDING'
        )
        order_total = Decimal('0.00')
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_order=item['price']
            )
            order_total += item['price'] * item['quantity']
        
        order.total_price = order_total
        order.save()
        
        # Create Notification for seller
        Notification.objects.create(
            user=seller,
            message=f"New offer from @{request.user.username}: ${order_total}",
            link="/dashboard/"
        )
    
    # Clear cart
    request.session['cart'] = {}
    messages.success(request, "Your offers have been sent!")
    return redirect('users:dashboard')

@login_required
def order_action(request, order_id, action):
    order = get_object_or_404(Order, id=order_id, seller=request.user)
    
    if action == 'confirm':
        order.status = 'CONFIRMED'
        messages.success(request, f"Order #{order.id} confirmed!")
        Notification.objects.create(
            user=order.customer,
            message=f"Seller @{request.user.username} confirmed order #{order.id}!",
            link="/dashboard/"
        )
    elif action == 'reject':
        order.status = 'REJECTED'
        messages.warning(request, f"Order #{order.id} rejected.")
        Notification.objects.create(
            user=order.customer,
            message=f"Seller @{request.user.username} rejected order #{order.id}.",
            link="/dashboard/"
        )
    
    order.save()
    return redirect('users:dashboard')
