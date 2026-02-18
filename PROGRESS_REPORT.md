# Project Progress Report

**Project Title:** Online Marketplace System

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

### 4. User Interface
- Designed a modern, responsive UI using custom CSS variables and Flexbox.
- Implemented a base template with a consistent header/footer structure.
- Applied "Glassmorphism" inspired design elements with gradients and card layouts.

### 5. Next Steps
- Implement Product models and listing functionality.
- Develop the Shopping Cart and Checkout system.
- Build the Seller Dashboard for managing inventory.
