# Mini Trello

A real-time collaborative project management tool inspired by Trello, built with Django and Django Channels.

This project focuses on backend architecture, real-time communication, clean code practices, and scalable design rather than frontend complexity.

## Features

### Authentication

* Custom User Model
* Registration and Login
* Secure Authentication

### Organizations

* Create Organizations
* Invite Members
* Role-Based Permissions

### Project Management

* Create Projects
* Create Boards
* Create Columns
* Create Tasks

### Collaboration

* Assign Tasks
* Comment on Tasks
* Activity Tracking
* Real-Time Updates

### Real-Time Functionality

* Live Task Creation
* Live Task Updates
* Live Task Movement Between Columns
* Live Comment Updates

## Tech Stack

### Backend

* Django 5.x
* Django Channels 4.x
* PostgreSQL
* Redis

### Frontend

* Django Templates
* Vanilla JavaScript
* HTML/CSS

### Infrastructure

* Docker
* Docker Compose

### Development Tools

* Pytest
* Black
* isort
* Flake8
* GitHub Actions

## Architecture

The application follows a service-layer architecture:

Views
→ Services
→ Models
→ Database

WebSocket events are handled through Django Channels and Redis.

The codebase is structured to allow a future migration to Django REST Framework and a decoupled frontend without major refactoring.

## Project Structure

```text
apps/
├── accounts/
├── organizations/
├── projects/
├── boards/
├── tasks/
├── activities/
└── notifications/
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/mini-trello.git
cd mini-trello
```

### Create Environment Variables

```bash
cp .env.example .env
```

### Run With Docker

```bash
docker compose up --build
```

### Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

### Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

## Running Tests

```bash
pytest
```

## Future Improvements

* REST API using Django REST Framework
* Drag-and-Drop Interface
* Email Notifications
* File Attachments
* Advanced Search and Filtering

## Screenshots

Add screenshots here after implementing the UI.

## License

MIT License
