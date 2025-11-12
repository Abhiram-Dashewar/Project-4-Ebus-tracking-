# 🚍 E-Bus Tracking & Management — Project 4

**E-Bus Tracking & Management** is a full-stack web application that provides real-time bus tracking, route and schedule management, driver assignment, and a user-facing booking/lookup interface.  
The project is built with Flask (backend), Jinja2 templates (server-side UI), standard web frontend (HTML/CSS/JavaScript), and a relational database (SQLite / MySQL).
---

## 🔑 Key Features

### Admin 
- CRUD for buses, drivers, routes, and stops.
- Assign drivers to buses and create schedules.
- View active buses and their real-time route progress.
- Search and filter by route, bus, driver, or time.

### User-facing
- Browse routes and schedules.
- Search for buses between start and destination stops.

---

## 🧩 Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript (vanilla or Bootstrap)
- Templates: Jinja2
- Database: SQLite (development) / MySQL or PostgreSQL (production)
- Optional: Celery + Redis for background tasks (notifications, location processing)

---

## 🔧 Installation — Quick Start (local)

1. **Clone**
```bash
git clone https://github.com/your-username/ebus-tracking-management.git
cd ebus-tracking-management
