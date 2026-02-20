# Project Progress Report

**Project Title:** NovaMarket - Online Marketplace System

**Team Members:** (To be filled by group)

## Development Progress

### 1. System Setup
- Initialized Django project structure.
- Created `users` app for handling authentication and user role management.
- Configured PostgreSQL/SQLite database (currently using SQLite for development).

### 2. User Authentication System
- **Custom User Model:** Implemented a custom user model extending `AbstractUser` to support multiple user roles:
  - **Customer:** Standard user who can browse and buy products.
  - **Seller:** User who can list and manage products.
  - **Admin:** Superuser with full system access.
- **Registration:** Created separate registration flows for Customers and Sellers.
- **Login/Logout:** Implemented standard Django authentication views.

### 3. Social Authentication
- Integrated `social-auth-app-django` library.
- Configured Google OAuth2 backend (requires API keys).
- Added "Sign in with Google" button to login page.

### 4. User Interface (New Design System Implemented)
- **Branding:** Updated project name to "NovaMarket". Applied new design system with Inter font, rounded corners (12px), and pill-shaped elements.
- **Color Palette:** Implemented "Modern SaaS" palette with Primary (#4F46E5), Secondary (#F9FAFB), and Accent (#F97316).
- **Layout:**
  - **Sticky Header:** Includes Logo, Search Bar, Category Dropdown, and Action Icons (Cart, Notifications).
  - **Hero Section:** Added dynamic hero banner with call-to-action buttons.
  - **Sidebar Filters:** Implemented sidebar for filtering products by Price, Category, and Rating.
  - **Product Grid:** Responsive grid layout for showcasing products.
- **Components:** styled buttons, inputs, and cards to match the design specification.

### 5. Next Steps
- Implement Product models and dynamic listing functionality (currently static placeholders).
- Develop the Shopping Cart and Checkout system.
- Build the Seller Dashboard for managing inventory.
