# 🚍 Bus App

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Repo Size](https://img.shields.io/github/repo-size/reory/bus_app)
![Last Commit](https://img.shields.io/github/last-commit/reory/bus_app)
![Tests](https://img.shields.io/badge/tests-26%20passing-brightgreen)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Kivy](https://img.shields.io/badge/Kivy-3776AB?style=for-the-badge&logo=kivy&logoColor=white)


A full-stack transit app featuring a  Django REST framework and a Multi-threaded Kivy mobile interface.

A Reliable transit apps require robust front-end logic. I built this UK Bus Tracker (v1) as a Proof of Concept to demonstrate a mobile-ready UI (Kivy) capable of processing transit data. To ensure a consistent demo experience without API rate-limiting, v1 utilizes a mocked data engine that simulates real-world bus arrivals.

---

<details>
  <summary>📱 App Gallery</summary>

<p align="center">
  <img src="screenshots/alerts_screen.png" width="250" alt="Alert Screen">
  <img src="screenshots/login_screen.png" width="250" alt="Login Screen">
  <img src="screenshots/maps_screen.png" width="250" alt="Maps Screen">
  <img src="screenshots/prediction_screen.png" width="250" alt="Prediction Screen">
  <img src="screenshots/select_route_screen.png" width="250" alt="Routes Screen">
  <img src="screenshots/stops_screen.png" width="250" alt="Stops Screen">
</p>

</details>
---

## 🚀 Features

* **26/26 Passing Unit Tests**✅ 
* **Mocked Time** - (Proof of concept)
* **Multi-threaded Kivy UI**
* **Django REST Framework Backend** (Scalable app structure)

---

## 📦 Installation

1. **Clone the repository and install:**
```bash
git clone https://github.com/reory/bus_app.git
cd bus_app
pip install -r requirements.txt
python manage.py migrate
```

---

## Usage

This project requires both the backend and frontend to be running simultaneously.

1. **Start the backend:** 
   ```bash
    python manage.py runserver 
    ```

2. **Start the frontend:**
   ```bash
   python main.py
   ```

---

## Project Structure

```text
bus_app/
├── api/                  # Main API Gateway & GTFS Imports
├── bus_backend/          # Project Core
│   ├── apps/             # Modular Business Logic
│   │   ├── notifications/# User alerts & notifications
│   │   ├── realtime/     # Live bus tracking data
│   │   ├── routes/       # GTFS route & stop management
│   │   └── users/        # Custom user models & auth
│   └── settings.py       # Global configuration
├── frontend/             # Kivy Mobile Application
├── tests/                # 26 Unit tests (Backend & Frontend)
├── manage.py             # Django management script
└── main.py               # Kivy entry point
```

---

## Testing🚦

The project includes a comprehensive suite of 17 tests covering models, serializers, and the Kivy UI logic.

To run the tests:
```bash
pytest
```

---

## Technologies Used

- Python 3.x
- Django (REST framework)
- Kivy (UI Framework)
- Pytest (Testing)
- Celery (Task scheduling)

---

## 🛣️ Roadmap Features

- [ ] Live GTFS-Realtime Ingestion
The Goal: Swap mock data for live transit feeds.
The Tech: Deploy a Django background worker to pull and decode Protocol Buffer (.pb) vehicle streams every 30 seconds.

- [ ] Synthetic GTFS Generator (Faker)
The Goal: Build a localized data factory to simulate a bustling city transit network.
The Tech: Use `faker`.providers.address to generate realistic street name bus stops (e.g., "Main St & 4th Ave") and clamp random lat/long coordinates within a tight boundary to simulate a dense downtown core.

- [ ] Rust-Powered Schedule Matrix Compiler
The Goal: Generate millions of realistic, connected schedule times without melting your CPU.
The Tech: Pass your synthetic `faker` stop lists into a `Rust` + `PyO3` extension. Let `Rust` handle the heavy loop calculations to instantly generate sequential arrival and departure times (StopTime rows) for thousands of simulated trips.

- [ ] Multi-Stop Journey Planner
The Goal: Give the app actual point-A to point-B routing capabilities.
The Tech: Implement pathfinding algorithms (like Dijkstra’s or Connection Scan) on the backend to calculate the fastest multi-stop trips.

- [ ] Offline Spatial Caching
The Goal: Keep the app functional when cellular data drops out.
The Tech: Embed a lightweight `SQLite` cache on the `Kivy` client to store and render route shapes and stop layouts completely offline.

- [ ] WebSocket Push Alerts
The Goal: Notify riders of sudden route delays instantly.
The Tech: Use `Django` Channels to maintain live WebSocket connections, pushing urgent service disruptions directly to the `Kivy` UI.

- [ ] Personalized Dashboards
The Goal: Let users see their daily commute countdown immediately.
The Tech: Build a "Favorites" schema allowing users to pin specific stop IDs directly to the launch screen, skipping the route menus entirely.

---

## Notes
- Version 1.0 Initial release. 
- 17 passing unit tests. 
- Ensure the Django backend is running before starting the Kivy frontend.

**Built By Roy Peters** [Click here for contact details 😁](https://www.linkedin.com/in/roy-p-74980b382/)