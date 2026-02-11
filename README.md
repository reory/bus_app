# Bus Tracker

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Repo Size](https://img.shields.io/github/repo-size/reory/bus_app)
![Last Commit](https://img.shields.io/github/last-commit/reory/bus_app)
![Tests](https://img.shields.io/badge/tests-17%20passing-brightgreen)

A full-stack transit app featuring a  Django REST framework and a Multi-threaded Kivy mobile interface.

---

## 📱 App Gallery

<p align="center">
  <img src="screenshots/alerts_screen.png" width="250" alt="Alert Screen">
  <img src="screenshots/login_screen.png" width="250" alt="Login Screen">
  <img src="screenshots/maps_screen.png" width="250" alt="Maps Screen">
  <img src="screenshots/prediction_screen.png" width="250" alt="Prediction Screen">
  <img src="screenshots/select_route_screen.png" width="250" alt="Routes Screen">
  <img src="screenshots/stops_screen.png" width="250" alt="Stops Screen">
</p>

---

## 🚀 Features

* **17/17 Passing Unit Tests**✅ 
* **Real-time API Integration** 
* **Multi-threaded Kivy UI**
* **Django REST Framework Backend** (Scalable app structure)

---

## 📦 Installation

1. **Clone the repository and install:**
```bash
git clone <add-later>
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
├── tests/                # 17 Unit tests (Backend & Frontend)
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

## Notes
- Version 1.0 Initial release. 
- 17 passing unit tests. 
- Ensure the Django backend is running before starting the Kivy frontend.
