from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.login_redirect),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paintings/', views.painting_list, name='painting_list'),
    path('paintings/add/', views.painting_add, name='painting_add'),
    path('paintings/<int:pk>/edit/', views.painting_edit, name='painting_edit'),
    path('paintings/<int:pk>/delete/', views.painting_delete, name='painting_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/status/', views.order_status, name='order_status'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('users/', views.user_list, name='user_list'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('profile/', views.admin_profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
]
