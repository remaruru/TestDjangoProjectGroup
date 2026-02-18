# Online Marketplace

## Project Overview
This project is an online marketplace platform with user authentication, custom user roles (Standard Customer, Seller), and social login integration.

## Getting Started

### 1. Setup Environment
Make sure you have Python installed.

```bash
# Clone the repository (if applicable)

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

*(Note: Create a requirements.txt file if needed: `pip freeze > requirements.txt`)*

### 2. Configure Social Auth (Important)
To enable Google Sign-In, you need to create OAuth 2.0 Credentials in the Google Developer Console.

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable "Google People API" (or just standard login scope).
4. Create Credentials -> OAuth Client ID -> Web application.
5. Add Authorized Redirect URIs: `http://localhost:8000/social/complete/google-oauth2/`
6. Copy the **Client ID** and **Client Secret**.
7. Update `marketplace/settings.py`:
   - `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-client-id'`
   - `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-client-secret'`

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Open your browser at `http://localhost:8000/`.

## Features
- **Sign Up:** Register as a Customer or Seller.
- **Log In:** Standard username/password or Google Login.
- **Dashboard:** View your role (Customer/Seller/Admin) on the home page.
