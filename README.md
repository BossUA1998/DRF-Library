# Library Service API

A comprehensive RESTful API service designed to automate online library operations. The system facilitates the management of book catalogs, users, borrowing cycles, and return processes, while also automating payments and fine calculations for overdue items.

The project is built using **Django REST Framework** and adheres to clean architecture principles.

## 🛠 Tech Stack

* **Python 3 / Django 6**
* **Django REST Framework** (DRF)
* **PostgreSQL** — Primary relational database
* **Stripe** — Payment gateway for processing rentals and fines
* **DjangoQ + Redis** — Asynchronous task processing (background payments, notifications)
* **Telegram Bot API** — User notifications and account synchronization
* **JWT** — Secure JSON Web Token authentication
* **Swagger / Redoc** — Automatic API documentation

## 🚀 Key Features

### 📚 Library Management
* **Catalog Control:** Manage book details including titles, authors, cover types, and daily fees.
* **Inventory Tracking:** Automatic inventory validation and updates when books are borrowed or returned.
* **Permissions:** Granular access control distinguishing between Administrators (full access) and authenticated Users (read-only catalog access).

### 🔄 Borrowing System
* **Loan Processing:** Create borrowing records with automatic inventory checks.
* **Tracking:** Records borrow dates and expected return dates.
* **Filtering:** Filter borrowings by User ID or active status (returned vs. non-returned).
* **Validation:** Prevents borrowing if the book inventory is empty.

### 💸 Payments & Fines
* **Stripe Integration:** Seamless payment processing via Stripe Checkout Sessions.
* **Rental Calculation:** Dynamic cost calculation based on the book's daily fee and borrowing duration.
* **Fine System:** Automated calculation of additional fees using a fine multiplier if a book is returned after the expected date.
* **Status Management:** Tracks payment lifecycles (`PENDING`, `PAID`).

### 👤 Users & Notifications
* **Authentication:** Registration and login system powered by JWT.
* **Telegram Sync:** Users can link their Telegram accounts to receive real-time notifications about new borrowings and successful payments.
* **Profile Management:** Dedicated `/me/` endpoint for managing personal data.

---

## 🏁 Getting Started
* **Configure the .env-sample file into a new .env file**
* **Run the docker and docker-compose file**
```bash
docker-compose up --build
```