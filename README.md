# Arivu Supply Chain Management System

## Overview
A modular FastAPI-based B2B supply chain management system for Arivu Foods, supporting:
- Inventory, Orders, Customers, Billing, Analytics, Notifications, Audit
- Admin and Retailer user roles
- JWT authentication and SQLite persistent storage
- Real PDF invoice generation and email notifications (demo)

## Features
- Inventory CRUD, logs, and low stock alerts
- Order management with status tracking
- Customer management (basic CRM)
- Billing and invoice management (PDF export)
- Analytics dashboards for admin and retailer
- Email notifications (requires local SMTP server)
- Audit logging for sensitive actions
- All endpoints protected by JWT authentication

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the backend server
```bash
uvicorn supply_chain_system.main:app --reload
```

### 3. Access the frontend
Open your browser to:
```
http://localhost:8000/
```

### 4. Login credentials
- **Admin:**
  - Username: `admin`
  - Password: `adminpass`
- **Retailer:**
  - Username: `retailer1`
  - Password: `retailpass`

### 5. Registering new users
Use `/register.html` to create additional accounts. The registration endpoint
requires a `role` parameter with either `admin` or `retailer`.

### 6. Features
- Admin dashboard: `/dashboard.html` (auto-redirect after admin login)
- Retailer dashboard: `/retailer_dashboard.html` (auto-redirect after retailer login)
- Inventory, customer, and invoice management via UI
- Download invoice PDFs and send emails (demo)

### 7. Sample Data
Sample users, inventory, customers, orders, and invoices are auto-populated on first run.

### 8. Notes
- Email notifications require a local SMTP server (for demo: `python -m smtpd -c DebuggingServer -n localhost:1025`)
- All data is stored in `arivu.db` (SQLite)
- All API endpoints require JWT authentication

---

## Project Structure
```
supply_chain_system/
├── main.py
├── auth/ (JWT, login, register)
├── users/
├── inventory/
├── orders/
├── customers/
├── billing/
├── analytics/
├── reports/
├── notifications/
├── audit/
├── database/ (models, session, core)
├── utils/
frontend/
  ├── index.html, dashboard.html, inventory.html, register.html, retailer_dashboard.html
```

---

## License
MIT
