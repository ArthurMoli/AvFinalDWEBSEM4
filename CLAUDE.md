# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based real estate management system (Sistema de Gerenciamento Imobiliário) with TailwindCSS for frontend styling. The application manages properties, user registrations, property interests, work tasks, and reporting features.

## Commands

### Development Setup
```bash
# If using system Python (no venv), add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install Django dependencies
pip3 install --break-system-packages -r requirements.txt

# Install frontend dependencies
npm install

# Run database migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Build
```bash
# Build TailwindCSS (manual - no npm scripts defined)
npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
```

### Django Management
```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files for production
python manage.py collectstatic

# Django shell for debugging
python manage.py shell

# Run tests (when implemented)
python manage.py test
```

## Architecture

### Django Apps Structure
The project follows Django's app-based architecture with clear separation of concerns:

- **config/** - Main Django project configuration
  - URL routing aggregates all app URLs
  - Settings configured for development (DEBUG=True)
  - Uses SQLite database

- **properties/** - Core real estate functionality
  - `Imovel` model: Property listings (apartments/houses) with image URLs
  - `Interesse` model: Tracks client interest in properties
  - Permission system for property publication

- **users/** - User management and authentication
  - Custom user model implementation
  - Registration and profile management

- **works/** - Work/task management system
  - Separate namespace in URL configuration

- **reports/** - Reporting and analytics features
  - Dashboard functionality

- **core/** - Shared functionality
  - Context processors for global template data
  - Notification system (NotificacoesView)
  - Home page view

### Frontend Architecture
- **Templates**: Django template inheritance with app-specific organization
- **Styling**: TailwindCSS with dark theme variables defined
- **Static files**: 
  - `input.css` contains Tailwind directives and custom CSS variables
  - `output.css` is the compiled CSS file
  - Dark theme color scheme using slate/emerald palette

### Key Design Patterns
1. **URL Organization**: Main urls.py includes app-specific URL configurations
2. **Model Relationships**: ForeignKey relationships between User, Imovel, and Interesse
3. **Permission System**: Custom permissions for property publication
4. **View Architecture**: Mix of class-based views (HomeView, NotificacoesView) and function-based views

### Database Schema
- SQLite database (db.sqlite3)
- Key models:
  - User (custom user model in users app)
  - Imovel (properties with type, price, rooms, description)
  - Interesse (many-to-many relationship between users and properties)
  - Work-related models in works app
  - Notification system in core app