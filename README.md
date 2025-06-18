# Arivu Supply Chain Management System

## Overview
A modular FastAPI-based B2B supply chain management system for Arivu Foods, supporting:
- Inventory, Orders, Customers, Billing, Analytics, Notifications, Audit
- Admin and Retailer user roles
- JWT authentication and SQLite persistent storage
- Real PDF invoice generation and email notifications (demo)

Okay, focusing on concise, key features for manufacturing and retail roles for Arivu Foods:

Core Product Identification & Details:

Product Name: (e.g., "Low-Carb Multi Seeds Atta", "Groundnut Oil") - This is the primary display name of the product.
SKU (Stock Keeping Unit): A unique alphanumeric code for each specific product variant (e.g., AF-LCA-1KG, AF-GNO-1L). This is crucial for tracking.
Product Description: A more detailed explanation of the product, its key features, and benefits (e.g., "Whole Ground Flax, Sunflower, Melon, Pumpkin Seeds; Rich in Fibre, Protein, Calcium.").
Category: (e.g., "Flour", "Oil", "Snacks") - For logical grouping and reporting.
Unit of Measure (UOM): How the product is sold or tracked (e.g., "kg", "Liter", "gram").
Quantity/Volume per Unit: The specific amount in the UOM (e.g., "1" kg, "1" L, "500" g).
MRP (Maximum Retail Price): The selling price to the customer (e.g., ₹480)

## Dashboard Features & Functions: Arivu Foods

---

### I. Manufacturer User Dashboard

**Purpose:** To monitor and manage production, raw materials, and quality control.

**Key Features & Sections:**

1.  **Production Overview:**
    * **"What's Next" Schedule:** Displays upcoming production batches (e.g., "Khapli Wheat Flour - Batch 005 - Start tomorrow").
    * **Current Production Status:** Real-time progress of ongoing batches (e.g., "Multi Seeds Atta - 70% Complete").
    * **Alerts:** "Low Capacity Detected," "Production Delay Alert."
    * **Functions:**
        * View detailed production orders.
        * Update batch progress (e.g., "Started," "Completed").

2.  **Raw Material Inventory:**
    * **"Top 5 Critical Materials":** Visual of essential raw material stock levels (e.g., Sunflower Seeds - 80kg Left).
    * **Low Stock Warnings:** Highlights materials below reorder point (e.g., "Coconut Powder - LOW STOCK!").
    * **Functions:**
        * Quickly access full raw material list.
        * Initiate a purchase request for a specific material.

3.  **Quality Control (QC) & Batch Traceability:**
    * **"QC Check Results (Last 24 Hrs)":** Summary of recent QC passes/fails.
    * **"Batch Status":** Overview of recently produced batches and their QC approval.
    * **Functions:**
        * Search by batch number to view full production and QC history.
        * Log new QC results for incoming raw materials or finished goods.

---

### II. Retailer User Dashboard

**Purpose:** To monitor sales, manage finished goods inventory, and track customer orders.

**Key Features & Sections:**

1.  **Sales Performance:**
    * **"Today's Sales":** Total revenue and number of orders for the current day.
    * **"Top 3 Best Sellers (Last 7 Days)":** Shows products generating most revenue/quantity (e.g., "Low-Carb Multi Seeds Atta," "Groundnut Oil").
    * **Sales Trend:** Simple graph showing daily sales over the last week.
    * **Functions:**
        * View detailed sales reports by product or period.
        * Compare current sales to previous periods.

2.  **Finished Goods Inventory:**
    * **"Quick Stock Status":** At-a-glance view of essential finished product stock levels (e.g., "Coconut Mixture - 150 units left").
    * **"Products Nearing Out of Stock":** Highlights items with critically low stock (e.g., "Multi Seed Chakli - 20 units left!").
    * **Functions:**
        * Browse full product inventory.
        * Request stock transfer from manufacturing/warehouse.

3.  **Order Fulfillment:**
    * **"Pending Orders":** Number of orders awaiting processing/shipping.
    * **"Recent Shipped Orders":** List of most recently dispatched orders.
    * **"Returns Pending":** Count of return requests to be processed.
    * **Functions:**
        * Click to view full order details.
        * Change order status (e.g., "Mark as Shipped").
        * Print shipping labels for selected orders.

## Features
- Inventory CRUD, logs, and low stock alerts
- Product catalog management with SKU, description, and pricing stored in `arivu.db`
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
Only admins can create retailer accounts. Open `/register.html` while logged in as
an admin to add new users. When creating a retailer the frontend sends a special
`admin_token` so that self-registration is blocked.

### 6. Features
 - Admin dashboard: `/admin_dashboard.html` (auto-redirect after admin login)
- Retailer dashboard: `/retailer_dashboard.html` (auto-redirect after retailer login)
- Inventory, customer, and invoice management via UI
- Download invoice PDFs and send emails (demo)

### 7. Sample Data
Sample users, products, inventory, customers, orders, and invoices are auto-populated on first run.

### 8. Notes
- Email notifications require a local SMTP server (for demo: `python -m smtpd -c DebuggingServer -n localhost:1025`)
- All data is stored in `arivu.db` (SQLite) using SQLAlchemy models
- All API endpoints require JWT authentication

---


---

## License
MIT
