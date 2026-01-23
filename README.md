# 📚 Library Service API

A REST API service for automating city library operations.\
The system allows managing the book inventory, tracking borrowings, processing payments, and notifying administrators.

## 🛠 Technologies

- **Core:** Python 3, Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Async & Tasks:** Redis, Django-Q
- **External APIs:** Stripe (payments), Telegram API (notifications)
- **Containerization:** Docker, Docker Compose

## ✨ Features

### User Management
- Registration
- JWT authentication
- Permissions (Admin/User)

### Books
- CRUD operations
- Automatic inventory tracking (available book count)

### Borrowings
- Borrowing creation
- Inventory validation
- Book returns

### Payments
- Stripe integration for borrowing payments and overdue fines.

### Notifications
- Asynchronous Telegram notifications for new borrowings and daily overdue reports.
