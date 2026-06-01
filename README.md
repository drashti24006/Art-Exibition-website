# Art Exhibition

Beautiful Django website for Art Exhibition - Mandala, Portrait & Shading artworks.

## Features

**Client Side:**
- Nav: Home, Mandala, Portrait, Shading, Gallery, About Us, Contact Us
- Register & Login buttons (username capital letter in circle when logged in)
- Hero section with background image and title
- 25 artwork images with Add to Cart, quantity +/- in cart
- Login required to purchase - bill with name, address, email, mobile, price, quantity
- About Us & Contact Us with admin-editable content
- Responsive design

**Admin Side:**
- Dashboard, Paintings, Orders, Categories, Users, Contacts, Settings
- Add/edit 25 paintings, manage orders, update hero image & site content

## Setup (SQLite - Default, No MySQL needed)

1. **Install:** `pip install -r requirements.txt`
2. **Migrate:** `python manage.py migrate`
3. **Seed data:** `python manage.py seed_data`  (25 paintings + categories)
4. **Admin user:** `python manage.py createsuperuser`
5. **Run:** Double-click `run.bat` (runs on port 8001, opens Art Exhibition in browser)
   OR: `python manage.py runserver 8001`

## Setup (MySQL)

1. Run `sql/art_exhibition_db.sql` in MySQL (creates database + all tables + sample records)
2. In `config/settings.py` - uncomment MySQL config, comment SQLite
3. Run `python manage.py seed_data` and `python manage.py createsuperuser`

## Hero Background Image

Add your custom dashboard/hero image: Login as admin > Admin Panel > Settings > Hero Background URL (paste image URL) or upload Hero Background image.
