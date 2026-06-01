from .models import Cart, SiteSettings, Category


def cart_count(request):
    try:
        if request.user.is_authenticated:
            return {'cart_count': Cart.objects.filter(user=request.user).count()}
    except Exception:
        pass
    return {'cart_count': 0}


def site_settings(request):
    try:
        s = SiteSettings.objects.first()
        return {'site_settings': s if s else SiteSettings()}
    except Exception:
        return {'site_settings': SiteSettings()}


def nav_categories(request):
    """Categories for client navbar dropdown – dynamic from admin."""
    try:
        cats = Category.objects.order_by('name')
        return {'nav_categories': cats}
    except Exception:
        return {'nav_categories': []}
