"""
Admin authentication - SEPARATE from client.
Only superuser can access. Uses _admin_user_id session.
Client login has NO effect here.
"""
from core.models import User

ADMIN_SESSION_KEY = '_admin_user_id'


def get_admin_user(request):
    """Returns admin user if logged in via admin panel. None otherwise."""
    user_id = request.session.get(ADMIN_SESSION_KEY)
    if user_id:
        try:
            return User.objects.get(pk=user_id, is_superuser=True)
        except User.DoesNotExist:
            request.session.pop(ADMIN_SESSION_KEY, None)
    return None


def admin_required(view_func):
    """Decorator: only superuser logged in at /admin-panel/login/ can access."""
    def wrap(request, *args, **kwargs):
        admin_user = get_admin_user(request)
        if not admin_user:
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.error(request, 'Admin login required.')
            return redirect('admin_panel:login')
        request.admin_user = admin_user
        return view_func(request, *args, **kwargs)
    return wrap
