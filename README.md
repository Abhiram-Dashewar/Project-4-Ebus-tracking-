# 🚍 E-Bus Tracking & Management — Project 4

**E-Bus Tracking & Management** is a full-stack web application that provides real-time bus tracking, route and schedule management, driver assignment, and a user-facing booking/lookup interface.  
The project is built with Flask (backend), Jinja2 templates (server-side UI), standard web frontend (HTML/CSS/JavaScript), and a relational database (SQLite / MySQL). It includes GPS-based tracking integration (simulated GPS for development), an admin dashboard, and user booking/search features.

---

## 🔑 Key Features

### Real-time tracking
- Track buses' current positions on a map (GPS integration or simulated GPS feed).
- Display live bus location, speed, and last-updated timestamp.

### Admin / Dispatcher
- CRUD for buses, drivers, routes, and stops.
- Assign drivers to buses and create schedules.
- View active buses and their real-time route progress.
- Search and filter by route, bus, driver, or time.

### User-facing
- Browse routes and schedules.
- Search for buses between start and destination stops.
- Book seats (optional simple booking flow).
- View booking history.

### Driver interface (lightweight)
- Driver login to update status (on-duty / off-duty).
- Periodic location updates (for real GPS devices or simulated updates).

### Extras
- Notifications (email/SMS hooks — integration optional).
- Simple analytics: trips per day, active buses, occupancy rates.
- Export reports (CSV).

---

## 🧩 Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript (vanilla or Bootstrap)
- Templates: Jinja2
- Database: SQLite (development) / MySQL or PostgreSQL (production)
- Maps: Leaflet / Google Maps (configurable)
- Optional: Celery + Redis for background tasks (notifications, location processing)

---

## 🔧 Installation — Quick Start (local)

1. **Clone**
```bash
git clone https://github.com/your-username/ebus-tracking-management.git
cd ebus-tracking-management
