# Student Management System

A secure student management web application with end-to-end encryption built using Django.

## Features

- End-to-end encryption for sensitive data
- User authentication (register/login)
- Student profile management
- Course enrollment and tracking
- Grade management
- Secure communication

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```
6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
8. Run the development server:
   ```
   python manage.py runserver
   ```

## Security Features

- End-to-end encryption for sensitive data
- Secure authentication
- CSRF protection
- XSS prevention
- Secure password storage 