-- ============================================
-- Art Exhibition - MySQL Database Setup
-- Run this file in MySQL to create database and all tables
-- ============================================

CREATE DATABASE IF NOT EXISTS art_exhibition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE art_exhibition_db;

SET FOREIGN_KEY_CHECKS = 0;

-- Django contenttypes
CREATE TABLE IF NOT EXISTS django_content_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Django migrations
CREATE TABLE IF NOT EXISTS django_migrations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Auth permission
CREATE TABLE IF NOT EXISTS auth_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_type_id INT NOT NULL,
    codename VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id),
    UNIQUE KEY auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id, codename)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Auth group
CREATE TABLE IF NOT EXISTS auth_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Auth group permissions
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id, permission_id),
    FOREIGN KEY (group_id) REFERENCES auth_group(id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core User (extends auth)
CREATE TABLE IF NOT EXISTS core_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6) NULL,
    is_superuser TINYINT(1) NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    is_staff TINYINT(1) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    date_joined DATETIME(6) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    user_type VARCHAR(10) NOT NULL DEFAULT 'client',
    phone VARCHAR(15) NOT NULL DEFAULT '',
    address LONGTEXT NOT NULL DEFAULT '',
    profile_pic VARCHAR(100) NULL,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core user groups
CREATE TABLE IF NOT EXISTS core_user_groups (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    group_id INT NOT NULL,
    UNIQUE KEY core_user_groups_user_id_group_id_c82fcad1_uniq (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core user permissions
CREATE TABLE IF NOT EXISTS core_user_user_permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    permission_id INT NOT NULL,
    UNIQUE KEY core_user_user_permissions_user_id_permission_id_73ea0daa_uniq (user_id, permission_id),
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core Category
CREATE TABLE IF NOT EXISTS core_category (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description LONGTEXT NOT NULL DEFAULT '',
    created_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core Painting
CREATE TABLE IF NOT EXISTS core_painting (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description LONGTEXT NOT NULL DEFAULT '',
    image VARCHAR(100) NULL,
    image_url VARCHAR(200) NULL,
    price DECIMAL(10,2) NOT NULL DEFAULT 0,
    dimension VARCHAR(100) NOT NULL DEFAULT '',
    medium VARCHAR(100) NOT NULL DEFAULT '',
    is_available TINYINT(1) NOT NULL DEFAULT 1,
    stock INT UNSIGNED NULL,
    sold_count INT UNSIGNED NOT NULL DEFAULT 0,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    category_id BIGINT NULL,
    FOREIGN KEY (category_id) REFERENCES core_category(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core Order
CREATE TABLE IF NOT EXISTS core_order (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    shipping_address LONGTEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(20) NOT NULL DEFAULT 'cod',
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    notes LONGTEXT NOT NULL DEFAULT '',
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    user_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core OrderItem
CREATE TABLE IF NOT EXISTS core_orderitem (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    quantity INT UNSIGNED NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    order_id BIGINT NOT NULL,
    painting_id BIGINT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES core_order(id) ON DELETE CASCADE,
    FOREIGN KEY (painting_id) REFERENCES core_painting(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core Cart
CREATE TABLE IF NOT EXISTS core_cart (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    quantity INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL,
    user_id BIGINT NOT NULL,
    painting_id BIGINT NOT NULL,
    UNIQUE KEY core_cart_user_id_painting_id_e3151e8b_uniq (user_id, painting_id),
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE,
    FOREIGN KEY (painting_id) REFERENCES core_painting(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core ContactSubmission
CREATE TABLE IF NOT EXISTS core_contactsubmission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(15) NOT NULL DEFAULT '',
    message LONGTEXT NOT NULL,
    created_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Core SiteSettings
CREATE TABLE IF NOT EXISTS core_sitesettings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(100) NOT NULL DEFAULT 'Art Exhibition',
    about_us_title VARCHAR(200) NOT NULL DEFAULT 'About Art Exhibition',
    about_us_content LONGTEXT NOT NULL DEFAULT 'We showcase beautiful artworks.',
    contact_email VARCHAR(254) NOT NULL DEFAULT 'contact@artexhibition.com',
    contact_phone VARCHAR(20) NOT NULL DEFAULT '+91 98765 43210',
    contact_address LONGTEXT NOT NULL DEFAULT '123 Art Gallery Street',
    hero_title VARCHAR(200) NOT NULL DEFAULT 'Discover Beautiful Art',
    hero_subtitle VARCHAR(300) NOT NULL DEFAULT 'Mandala, Portrait & Shading Art',
    hero_background VARCHAR(100) NULL,
    hero_background_url VARCHAR(200) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Django Session
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data LONGTEXT NOT NULL,
    expire_date DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Django Admin LogEntry
CREATE TABLE IF NOT EXISTS django_admin_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action_time DATETIME(6) NOT NULL,
    object_id LONGTEXT NULL,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT UNSIGNED NOT NULL,
    change_message LONGTEXT NOT NULL,
    content_type_id INT NULL,
    user_id BIGINT NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES core_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- Insert 1 Sample Record in Each Table
-- ============================================

-- Content types (required for Django)
INSERT IGNORE INTO django_content_type (app_label, model) VALUES
('contenttypes', 'contenttype'),
('auth', 'permission'),
('auth', 'group'),
('core', 'user'),
('core', 'category'),
('core', 'painting'),
('core', 'order'),
('core', 'orderitem'),
('core', 'cart'),
('core', 'contactsubmission'),
('core', 'sitesettings');

-- Categories (3 records)
INSERT IGNORE INTO core_category (name, slug, description, created_at) VALUES
('Mandala', 'mandala', 'Beautiful mandala art', NOW()),
('Portrait', 'portrait', 'Portrait paintings', NOW()),
('Shading', 'shading', 'Shading artworks', NOW());

-- Painting (1 sample record)
INSERT IGNORE INTO core_painting (title, slug, description, category_id, image_url, price, is_available, sold_count, created_at, updated_at) VALUES
('Sample Mandala Art', 'sample-mandala-art-1', 'Beautiful mandala design', 1, 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=400&fit=crop', 1500.00, 1, 0, NOW(), NOW());

-- Site Settings (1 record)
INSERT INTO core_sitesettings (site_name, about_us_title, about_us_content, contact_email, contact_phone, contact_address, hero_title, hero_subtitle, hero_background_url) 
SELECT 'Art Exhibition', 'About Art Exhibition', 'We showcase beautiful artworks including mandala, portrait, and shading art.', 'contact@artexhibition.com', '+91 98765 43210', '123 Art Gallery Street, Mumbai, India', 'Discover Beautiful Art', 'Mandala, Portrait & Shading Art Exhibition', 'https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=1920&h=1080&fit=crop'
WHERE NOT EXISTS (SELECT 1 FROM core_sitesettings);

-- Contact (1 record)
INSERT INTO core_contactsubmission (name, email, phone, message, created_at)
SELECT 'Sample Visitor', 'sample@example.com', '+91 1234567890', 'Sample contact message.', NOW()
WHERE NOT EXISTS (SELECT 1 FROM core_contactsubmission);

-- Note: For full 25 paintings + admin user, run: python manage.py seed_data
-- Note: For admin user, run: python manage.py createsuperuser
