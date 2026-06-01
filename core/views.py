from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import (
    User, Painting, Category, Cart, Order, OrderItem,
    ContactSubmission, SiteSettings
)
from .forms import UserRegistrationForm, LoginForm, CheckoutForm, ContactForm


def home(request):
    paintings = Painting.objects.filter(is_available=True).order_by('-created_at')[:25]
    return render(request, 'core/home.html', {'paintings': paintings})


def _category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    paintings = Painting.objects.filter(category=category, is_available=True).order_by('-created_at')
    return render(request, 'core/category_list.html', {'paintings': paintings, 'category': category})


def mandala_list(request):
    return _category_view(request, 'mandala')


def portrait_list(request):
    return _category_view(request, 'portrait')


def shading_list(request):
    return _category_view(request, 'shading')


def category_page(request, slug):
    """Generic category page – supports any category added from admin."""
    return _category_view(request, slug)

def gallery(request):
    paintings = Painting.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'core/gallery.html', {'paintings': paintings})


def painting_detail(request, slug):
    painting = get_object_or_404(Painting, slug=slug, is_available=True)
    related = Painting.objects.filter(
        category=painting.category, is_available=True
    ).exclude(id=painting.id)[:4]
    return render(request, 'core/painting_detail.html', {'painting': painting, 'related': related})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('core:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """Client login ONLY - sirf client/game users. Admin credentials work NAHI kare."""
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                if user.is_superuser:
                    messages.error(request, 'Admin login client side par nathi. Admin panel ma login karo: /admin-panel/')
                    return render(request, 'core/login.html', {'form': form})
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and next_url.startswith('/') and not next_url.startswith('/admin-panel'):
                    return redirect(next_url)
                return redirect('core:home')
            messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:home')


@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user).select_related('painting')
    total = sum(c.subtotal for c in items)
    return render(request, 'core/cart.html', {'cart_items': items, 'cart_total': total})


@require_POST
@login_required
def cart_add(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id, is_available=True)
    qty = int(request.POST.get('quantity', 1))
    if qty < 1:
        qty = 1
    cart, created = Cart.objects.get_or_create(
        user=request.user, painting=painting, defaults={'quantity': qty}
    )
    if not created:
        cart.quantity += qty
        cart.save()
    messages.success(request, f'"{painting.title}" added to cart.')
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url if next_url else 'core:gallery')


@require_POST
@login_required
def cart_remove(request, cart_id):
    cart = Cart.objects.filter(id=cart_id, user=request.user).first()
    if cart:
        cart.delete()
        messages.success(request, 'Item removed from cart.')
    return redirect('core:cart')


@require_POST
@login_required
def cart_update(request, cart_id):
    cart = Cart.objects.filter(id=cart_id, user=request.user).first()
    qty = int(request.POST.get('quantity', 1))
    if cart and qty >= 1:
        cart.quantity = qty
        cart.save()
        messages.success(request, 'Cart updated.')
    return redirect('core:cart')


@login_required
def checkout_view(request):
    items = Cart.objects.filter(user=request.user).select_related('painting')
    if not items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('core:gallery')
    total = sum(c.subtotal for c in items)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                total_amount=total,
                shipping_address=form.cleaned_data['shipping_address'],
                phone=form.cleaned_data['phone'],
                payment_method=form.cleaned_data.get('payment_method', 'cod'),
                notes=form.cleaned_data.get('notes', ''),
            )
            for cart_item in items:
                OrderItem.objects.create(
                    order=order,
                    painting=cart_item.painting,
                    quantity=cart_item.quantity,
                    price=cart_item.painting.price,
                )
            items.delete()
            messages.success(request, f'Order {order.order_number} placed successfully.')
            return redirect('core:order_detail', order_id=order.id)
    else:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone', ''),
            'shipping_address': getattr(request.user, 'address', ''),
        }
        form = CheckoutForm(initial=initial)
    return render(request, 'core/checkout.html', {
        'cart_items': items, 'cart_total': total, 'form': form
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})


def about_us(request):
    return render(request, 'core/about_us.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('core:contact_us')
    else:
        form = ContactForm()
    return render(request, 'core/contact_us.html', {'form': form})
