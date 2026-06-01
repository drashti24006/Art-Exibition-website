"""
Admin Panel - Completely SEPARATE from client.
Only superuser can access. Client login does NOT work here.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Sum, Count
from django.views.decorators.http import require_POST
from django.utils.text import slugify

from core.models import User, Painting, Category, Order, ContactSubmission, SiteSettings
from core.forms import LoginForm, PaintingForm

from .auth import get_admin_user, admin_required, ADMIN_SESSION_KEY
from .forms import AdminProfileForm, AdminPasswordChangeForm


def login_redirect(request):
    if get_admin_user(request):
        return redirect('admin_panel:dashboard')
    return redirect('admin_panel:login')


def admin_login(request):
    """Admin login - ONLY superuser. Client credentials will NOT work."""
    if get_admin_user(request):
        return redirect('admin_panel:dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user and user.is_superuser:
                request.session[ADMIN_SESSION_KEY] = user.id
                request.session.modified = True
                return redirect('admin_panel:dashboard')
            if user and not user.is_superuser:
                messages.error(request, 'Client credentials yaha work nathi kare. Sirf admin. Client login /login/ par karo.')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'admin_panel/login.html', {'form': form})


def admin_logout(request):
    request.session.pop(ADMIN_SESSION_KEY, None)
    request.session.modified = True
    messages.info(request, 'Logged out from admin.')
    return redirect('admin_panel:login')


@admin_required
def dashboard(request):
    from django.db.models.functions import TruncDate
    from datetime import timedelta
    from django.utils import timezone
    
    total_paintings = Painting.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(
        status__in=['confirmed', 'shipped', 'delivered']
    ).aggregate(s=Sum('total_amount'))['s'] or 0
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    top_paintings = Painting.objects.order_by('-sold_count')[:5]
    
    # Order status distribution for pie chart
    order_status_data = Order.objects.values('status').annotate(count=Count('id')).order_by('status')
    
    # Category-wise painting count for bar chart
    category_data = Category.objects.annotate(painting_count=Count('paintings')).order_by('-painting_count')[:5]
    
    # Last 7 days revenue for line chart
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_revenue = Order.objects.filter(
        created_at__gte=seven_days_ago,
        status__in=['confirmed', 'shipped', 'delivered']
    ).annotate(date=TruncDate('created_at')).values('date').annotate(
        revenue=Sum('total_amount')
    ).order_by('date')
    
    return render(request, 'admin_panel/dashboard.html', {
        'total_paintings': total_paintings,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'top_paintings': top_paintings,
        'order_status_data': order_status_data,
        'category_data': category_data,
        'daily_revenue': daily_revenue,
    })


@admin_required
def painting_list(request):
    paintings = Painting.objects.select_related('category').order_by('-created_at')
    return render(request, 'admin_panel/painting_list.html', {'paintings': paintings})


@admin_required
def painting_add(request):
    if request.method == 'POST':
        form = PaintingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Painting added.')
            return redirect('admin_panel:painting_list')
    else:
        form = PaintingForm()
    return render(request, 'admin_panel/painting_form.html', {'form': form, 'title': 'Add Painting'})


@admin_required
def painting_edit(request, pk):
    painting = get_object_or_404(Painting, pk=pk)
    if request.method == 'POST':
        form = PaintingForm(request.POST, request.FILES, instance=painting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Painting updated.')
            return redirect('admin_panel:painting_list')
    else:
        form = PaintingForm(instance=painting)
    return render(request, 'admin_panel/painting_form.html', {
        'form': form, 'title': 'Edit Painting', 'painting': painting
    })


@admin_required
@require_POST
def painting_delete(request, pk):
    """Delete a painting from admin panel."""
    painting = Painting.objects.filter(pk=pk).first()
    if not painting:
        messages.error(request, 'Painting not found.')
    else:
        title = painting.title
        painting.delete()
        messages.success(request, f'Painting "{title}" deleted.')
    return redirect('admin_panel:painting_list')


@admin_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'admin_panel/order_list.html', {
        'orders': orders, 'order_status_choices': Order.STATUS_CHOICES
    })


@admin_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'admin_panel/order_detail.html', {
        'order': order, 'order_status_choices': Order.STATUS_CHOICES
    })


@admin_required
@require_POST
def order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        old_status = order.status
        order.status = new_status
        order.save()
        if new_status == 'confirmed' and old_status != 'confirmed':
            for item in order.items.select_related('painting').all():
                p = item.painting
                p.sold_count += item.quantity
                if p.stock is not None:
                    p.stock = max(0, (p.stock or 0) - item.quantity)
                    if p.stock <= 0:
                        p.is_available = False
                p.save(update_fields=['sold_count', 'stock', 'is_available'])
        messages.success(request, f'Order status updated to {new_status}.')
    return redirect('admin_panel:order_detail', pk=pk)


@admin_required
def category_list(request):
    categories = Category.objects.annotate(
        painting_count=Count('paintings')
    ).order_by('name')
    return render(request, 'admin_panel/category_list.html', {'categories': categories})


@admin_required
@require_POST
def category_add(request):
    """Quick add for new category from admin list."""
    name = (request.POST.get('name') or '').strip()
    desc = (request.POST.get('description') or '').strip()
    if not name:
        messages.error(request, 'Category name is required.')
        return redirect('admin_panel:category_list')
    slug = slugify(name)
    cat, created = Category.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'description': desc},
    )
    if created:
        messages.success(request, f'Category "{name}" added.')
    else:
        messages.info(request, f'Category "{name}" already exists.')
    return redirect('admin_panel:category_list')


@admin_required
@require_POST
def category_delete(request, pk):
    """Delete a category (only from admin panel)."""
    cat = Category.objects.filter(pk=pk).first()
    if not cat:
        messages.error(request, 'Category not found.')
    else:
        name = cat.name
        cat.delete()
        messages.success(request, f'Category "{name}" deleted.')
    return redirect('admin_panel:category_list')


@admin_required
def user_list(request):
    users = User.objects.filter(user_type='client').exclude(is_superuser=True).order_by('-date_joined')
    return render(request, 'admin_panel/user_list.html', {'users': users})


@admin_required
def contact_list(request):
    contacts = ContactSubmission.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/contact_list.html', {'contacts': contacts})


@admin_required
@require_POST
def contact_delete(request, pk):
    """Delete a contact submission from admin."""
    obj = ContactSubmission.objects.filter(pk=pk).first()
    if not obj:
        messages.error(request, 'Contact not found.')
    else:
        obj.delete()
        messages.success(request, 'Contact deleted.')
    return redirect('admin_panel:contact_list')


@admin_required
def admin_profile(request):
    """Admin profile: username, email, profile picture, change password."""
    admin_user = request.admin_user
    profile_form = AdminProfileForm(instance=admin_user)
    password_form = AdminPasswordChangeForm(user=admin_user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'profile':
            profile_form = AdminProfileForm(request.POST, request.FILES, instance=admin_user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated (username, email, picture).')
                return redirect('admin_panel:profile')
        elif action == 'password':
            password_form = AdminPasswordChangeForm(admin_user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password changed. Next time login with new password.')
                return redirect('admin_panel:profile')
        else:
            profile_form = AdminProfileForm(request.POST, request.FILES, instance=admin_user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated.')
                return redirect('admin_panel:profile')

    return render(request, 'admin_panel/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'admin_user': admin_user,
    })


@admin_required
def settings_view(request):
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        settings_obj = SiteSettings.objects.create()
    if request.method == 'POST':
        settings_obj.site_name = request.POST.get('site_name', settings_obj.site_name)
        settings_obj.about_us_title = request.POST.get('about_us_title', settings_obj.about_us_title)
        settings_obj.about_us_content = request.POST.get('about_us_content', settings_obj.about_us_content)
        settings_obj.contact_email = request.POST.get('contact_email', settings_obj.contact_email)
        settings_obj.contact_phone = request.POST.get('contact_phone', settings_obj.contact_phone)
        settings_obj.contact_address = request.POST.get('contact_address', settings_obj.contact_address)
        settings_obj.hero_title = request.POST.get('hero_title', settings_obj.hero_title)
        settings_obj.hero_subtitle = request.POST.get('hero_subtitle', settings_obj.hero_subtitle)
        settings_obj.hero_background_url = request.POST.get('hero_background_url', '') or None
        if request.FILES.get('hero_background'):
            settings_obj.hero_background = request.FILES['hero_background']
        settings_obj.save()
        messages.success(request, 'Settings saved.')
        return redirect('admin_panel:settings')
    return render(request, 'admin_panel/settings.html', {'site_config': settings_obj})
