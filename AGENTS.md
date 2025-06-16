# `agents.md`

**Arivu Foods – Supply Chain Management System (SCMS)**
**Architecture: Modular Agent-Based | Tech Stack: Python + FastAPI**

---

## 🧩 Overview

This SCMS is designed to automate and streamline Arivu Foods’ B2B operations between **FMCG Admins** and **Local Retail Stores**, supporting:

* Inventory Tracking & Reorder Logic
* Order Lifecycle Management
* Retailer CRM & Terms
* Auto Invoice & Billing System
* Sales, Stock & Performance Analytics
* Dashboards with KPIs
* Email/SMS Notifications
* Audit Logs and Role-Based Access

---

## 👤 User Roles

### 1. FMCG Admin

* Full access to product, order, inventory, analytics, billing
* Configure stock thresholds, credit limits, product pricing
* Approve, monitor, or auto-process orders

### 2. Local Retail Store

* Place & track orders
* View invoices & product catalog
* Analyze order trends via dashboard
* Limited to their own data

---

## 🧠 Modular Agents Specification

### 📦 Inventory Management Agent

* Tracks product stock levels per SKU
* Auto restock alerts when below threshold
* Stock reservation during order placement
* Optional expiry date and batch tracking
* Logs inventory change history

**Endpoints:**

* `GET /inventory`
* `POST /inventory/update`
* `GET /inventory/logs`

---

### 📬 Order Management Agent

* Validates & processes incoming retailer orders
* Checks stock availability via inventory agent
* Handles approval logic (manual/auto)
* Triggers fulfillment workflow
* Emits events for notification, billing

**Endpoints:**

* `POST /orders`
* `GET /orders/{id}`
* `PATCH /orders/{id}/status`

---

### 👥 Customer Management Agent

* Manages retailer profiles, addresses, credit terms
* Links all orders/invoices per customer
* Tracks communication notes (optional)
* Works with Auth system for login/access

**Endpoints:**

* `GET /customers`
* `POST /customers`
* `GET /customers/{id}`

---

### 🧾 Billing & Invoice Agent

* Auto-generates invoice after order confirmation
* Tracks payment status (paid/unpaid/overdue)
* Exports invoices as PDF
* Handles credit notes/adjustments
* Future-ready for online payment integration

**Endpoints:**

* `GET /invoices`
* `GET /invoices/{id}/pdf`
* `PATCH /invoices/{id}/mark-paid`

---

### 📊 Analytics & Dashboard Agent

* Aggregates KPIs: revenue, top products, low stock, etc.
* User-based dashboards: Admin sees all, Retailer sees own data
* Visualizations: bar, pie, time-series charts
* Provides downloadable sales/inventory reports

**Endpoints:**

* `GET /dashboard/admin`
* `GET /dashboard/retailer`
* `GET /reports/sales?range=monthly`

---

### 📢 Notification Agent (Optional Enhancer)

* Sends order, invoice, stock alerts via Email/SMS
* Triggered via hooks/events in order or billing agents

**Endpoints:**

* `POST /notify/email`
* `POST /notify/sms`

---

### 🛡️ Audit & Logging Agent

* Captures actions: order edits, inventory changes, logins
* Supports audit trails for enterprise compliance

**Endpoints:**

* `GET /audit/logs`
* `POST /audit/record`

---

## ⚙️ Automation vs Manual Triggers

| Agent         | Manual Control       | Automation Available?       |
| ------------- | -------------------- | --------------------------- |
| Inventory     | Manual stock update  | Auto reorder alerts         |
| Orders        | Admin approval       | Auto-approval mode          |
| Billing       | Manual payment entry | Auto invoice gen            |
| Dashboards    | User-driven          | Real-time update via events |
| Notifications | Optional triggers    | Auto on event hook          |

---

## 🧱 Backend Architecture & Stack

| Layer          | Tech/Structure                 |
| -------------- | ------------------------------ |
| Framework      | Python + FastAPI               |
| DB             | PostgreSQL / MySQL             |
| ORM            | SQLAlchemy                     |
| Auth           | JWT + RBAC                     |
| Modularization | Agent-based DDD                |
| Export Formats | PDF (invoices), XLSX (reports) |
| Notifications  | SMTP (email), optional SMS API |
| Hosting Ready  | Docker, Gunicorn/Uvicorn       |

---

## 🗂️ Suggested Project Structure

```
supply_chain_system/
├── main.py
├── config/
│   └── settings.py
├── auth/                 # JWT + RBAC
├── users/                # Admin/Retailer profiles
├── inventory/            # Inventory Agent
├── orders/               # Order Agent
├── customers/            # Customer CRM Agent
├── billing/              # Invoice Agent + PDF
├── analytics/            # Dashboard KPIs
├── reports/              # CSV/XLSX exporters
├── notifications/        # Email/SMS triggers
├── audit/                # Log & monitor actions
├── database/             # DB engine, migrations
├── utils/                # Shared helpers, logger
└── tests/                # Unit/integration tests
```

---

## ✅ Summary

This `agents.md` defines a scalable, modular FastAPI-based architecture for Arivu Foods’ B2B SCM system. It enables automation, real-time data sync, analytics, billing, and multi-role operations with enterprise security, extensibility, and performance.
