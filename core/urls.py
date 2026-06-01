from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('mandala/', views.mandala_list, name='mandala'),
    path('portrait/', views.portrait_list, name='portrait'),
    path('shading/', views.shading_list, name='shading'),
    path('category/<slug:slug>/', views.category_page, name='category_page'),
    path('gallery/', views.gallery, name='gallery'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('painting/<slug:slug>/', views.painting_detail, name='painting_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:painting_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:cart_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
]
