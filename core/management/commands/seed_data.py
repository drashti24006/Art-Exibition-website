"""
Management command to seed database with 25 artworks, categories, and sample data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Painting, User, Order, OrderItem, ContactSubmission, SiteSettings

ART_IMAGES = [
    ("https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=400&fit=crop", "Mandala Harmony", "mandala", "Intricate mandala design with balanced patterns", 2500),
    ("https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=400&fit=crop", "Floral Mandala", "mandala", "Beautiful flower-inspired mandala art", 1800),
    ("https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=400&h=400&fit=crop", "Geometric Mandala", "mandala", "Geometric precision mandala artwork", 2200),
    ("https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=400&fit=crop", "Zen Mandala", "mandala", "Peaceful zen mandala design", 1950),
    ("https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=400&h=400&fit=crop", "Sacred Circle", "mandala", "Sacred circular mandala art", 2100),
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop", "Classic Portrait", "portrait", "Elegant classical portrait painting", 3500),
    ("https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400&h=400&fit=crop", "Modern Portrait", "portrait", "Contemporary portrait with modern style", 2800),
    ("https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop", "Character Portrait", "portrait", "Expressive character portrait", 3200),
    ("https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop", "Graceful Portrait", "portrait", "Graceful and detailed portrait", 2900),
    ("https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop", "Natural Portrait", "portrait", "Natural light portrait art", 2700),
    ("https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=400&h=400&fit=crop", "Apple Shading", "shading", "Realistic apple shading study", 1200),
    ("https://images.unsplash.com/photo-1513542789411-b6d5d1f1b2c3?w=400&h=400&fit=crop", "Sphere Shading", "shading", "3D sphere shading technique", 950),
    ("https://images.unsplash.com/photo-1546883521-43d2f84edc8a?w=400&h=400&fit=crop", "Cube Shading", "shading", "Geometric cube shading art", 1100),
    ("https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=400&fit=crop", "Landscape Shading", "shading", "Atmospheric landscape shading", 1500),
    ("https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=400&fit=crop", "Still Life Shading", "shading", "Classical still life shading", 1400),
    ("https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=400&h=400&fit=crop", "Sunset Mandala", "mandala", "Warm sunset colors mandala", 2300),
    ("https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=400&h=400&fit=crop", "Ocean Mandala", "mandala", "Ocean-inspired mandala patterns", 2000),
    ("https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=400&fit=crop", "Royal Portrait", "portrait", "Regal portrait style", 4200),
    ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop", "Minimalist Portrait", "portrait", "Clean minimalist portrait", 2600),
    ("https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=400&fit=crop", "Hand Shading", "shading", "Detailed hand shading study", 1300),
    ("https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=400&fit=crop", "Bottle Shading", "shading", "Glass bottle shading art", 1150),
    ("https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=400&h=400&fit=crop", "Petals Mandala", "mandala", "Delicate petal mandala design", 2400),
    ("https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400&h=400&fit=crop", "Abstract Portrait", "portrait", "Abstract expression portrait", 3100),
    ("https://images.unsplash.com/photo-1546883521-43d2f84edc8a?w=400&h=400&fit=crop", "Architecture Shading", "shading", "Architectural shading drawing", 1600),
    ("https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=400&h=400&fit=crop", "Celestial Mandala", "mandala", "Cosmic celestial mandala art", 2700),
]


class Command(BaseCommand):
    help = 'Seeds database with 25 artworks, categories, sample user, and settings'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Categories
        cats_data = [
            ('Mandala', 'mandala', 'Beautiful mandala art designs'),
            ('Portrait', 'portrait', 'Elegant portrait paintings'),
            ('Shading', 'shading', 'Shading and sketch artworks'),
        ]
        categories = {}
        for name, slug, desc in cats_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
            categories[slug] = cat

        # 25 Paintings
        for i, (img_url, title, cat_slug, desc, price) in enumerate(ART_IMAGES, 1):
            slug = slugify(title) + f'-{i}'
            Painting.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'category': categories[cat_slug],
                    'image_url': img_url,
                    'price': price,
                    'is_available': True,
                }
            )

        # Site Settings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='Art Exhibition',
                about_us_title='About Art Exhibition',
                about_us_content='We showcase beautiful artworks including mandala, portrait, and shading art. Our exhibition features talented artists from around the world.',
                contact_email='contact@artexhibition.com',
                contact_phone='+91 98765 43210',
                contact_address='123 Art Gallery Street, Mumbai, India 400001',
                hero_title='Discover Beautiful Art',
                hero_subtitle='Mandala, Portrait & Shading Art Exhibition',
                hero_background_url='https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=1920&h=1080&fit=crop',
            )

        # Sample Contact
        if not ContactSubmission.objects.exists():
            ContactSubmission.objects.create(
                name='Sample Visitor',
                email='sample@example.com',
                phone='+91 1234567890',
                message='This is a sample contact submission.',
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 25 paintings, categories, and sample data!'))
