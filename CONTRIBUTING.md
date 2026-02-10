# Contributing to Bus Tracker

First off, thank you for considering contributing to the Bus Tracker project! It's people like you who make this a great tool for the community.

## 🚦 Our "Golden Rule"
**All 17 existing unit tests must pass** before a Pull Request can be considered. We take stability seriously!

---

## 🛠 How to Get Started:

1. **Fork the Repository**: Create your own copy of the project.
2. **Create a Branch**: 
   ```bash
   git checkout -b feature/your-awesome-feature
   ```
3. **Set Up the Environment**: 

   Ensure you have all dependencies installed from the requirements.txt.

---

## 📂 Understanding the Project Structure:

To keep the project clean, please place your code in the appropriate directory:

- api/: General API endpoints and GTFS import logic.

- bus_backend/apps/: Modular logic (Routes, Users, Real-time data).

- frontend/: Kivy UI components and .kv styles.

- tests/: Any new features must include corresponding tests here.

---

## 🧪 Testing Requirements
We use pytest. Before submitting any changes, run the full suite:

```Bash
pytest
```

If you add a new feature, please add a new test file in tests/ to ensure your feature stays working in the future.

---

## 📝 Commit Messages
- We prefer clear, descriptive commit messages:

- feat: add real-time arrival predictions

- fix: resolve crash on map screen window resize

- docs: update installation instructions

---

## 🚀 Submitting a Pull Request

- Push your branch to your fork.

- Open a Pull Request against the main branch.

- Describe your changes in detail: What was the problem? How did you fix it?

- Await review! We try to look at all PRs within 72 hours.

---

## ⚖️ Code of Conduct
Be respectful, patient, and helpful to other contributors. We're all here to build something cool!