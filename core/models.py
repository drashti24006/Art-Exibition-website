from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def painting_upload_path(instance, filename):
    if instance.category:
        folder = instance.category.slug
    else:
        folder = 'other'
    return f'paintings/{folder}/{filename}'


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_admin_user(self):
        return self.user_type == 'admin' or self.is_staff

    def get_display_name(self):
        """Returns capital first letter of username for avatar."""
        if self.username:
            return self.username[0].upper()
        if self.email:
            return self.email[0].upper()
        return 'U'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Painting(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='paintings')
    image = models.ImageField(upload_to=painting_upload_path, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text='External image URL if no file uploaded')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dimension = models.CharField(max_length=100, blank=True)
    medium = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    sold_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=400&fit=crop'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'painting']

    def __str__(self):
        return f"{self.painting.title} x {self.quantity}"

    @property
    def subtotal(self):
        return self.painting.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery (COD)'),
        ('online', 'Online Payment'),
    )
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            self.order_number = f"ART{timezone.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.painting.title} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity


class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Art Exhibition')
    about_us_title = models.CharField(max_length=200, default='About Art Exhibition')
    about_us_content = models.TextField(default='We showcase beautiful artworks including mandala, portrait, and shading art.')
    contact_email = models.EmailField(default='contact@artexhibition.com')
    contact_phone = models.CharField(max_length=20, default='+91 98765 43210')
    contact_address = models.TextField(default='123 Art Gallery Street, Mumbai, India')
    hero_title = models.CharField(max_length=200, default='Discover Beautiful Art')
    hero_subtitle = models.CharField(max_length=300, default='Mandala, Portrait & Shading Art Exhibition')
    hero_background = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_background_url = models.URLField(blank=True, null=True)

    def get_hero_bg(self):
        if self.hero_background:
            return self.hero_background.url
        if self.hero_background_url:
            return self.hero_background_url
        return 'https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=1920&h=1080&fit=crop'
