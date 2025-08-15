# Arivu Supply Chain Management System with CRM

## Overview
A comprehensive FastAPI-based B2B supply chain management system with integrated CRM for Arivu Foods. Features a unified backend and responsive frontend for managing FMCG operations, inventory, and customer relationships.

## 🚀 Main Features:
- **CRM & Lead Management**: Full-featured lead pipeline management with conversion tracking
- **Inventory Management**: Real-time stock tracking with automated alerts
- **Multi-User Dashboards**: Specialized interfaces for CEO, Sales Manager, and Retail Partners
- **Order Management**: End-to-end order processing and fulfillment
- **Production Planning**: Quality Control and Finished Goods tracking
- **Authentication**: JWT-based secure authentication with role-based access
- **Analytics**: Comprehensive reporting and performance metrics

## 👥 User Roles & Access:
- **CEO/Manufacturer**: Complete oversight, lead management, business analytics
- **Sales Manager**: Lead pipeline management, conversion tracking, partner communications
- **Retail Partners**: Inventory management, stock requests, order placement
- **Standard Retailer**: Product browsing, order placement, account management

## 🆕 CRM Features Added:
- **Lead Management**: Create, track, and convert potential retail partners
- **Pipeline Tracking**: Visual sales funnel with conversion metrics
- **Lead Conversion**: Seamlessly convert qualified leads to active retailers
- **Performance Analytics**: Conversion rates, pipeline statistics, and KPIs
- **Communication Center**: Integrated messaging and contact management

## 📱 Dashboard Features:

### CEO Dashboard (`/ceo_dashboard.html`)
- **Executive Overview**: Total leads, active retailers, revenue metrics
- **Lead Pipeline Management**: Visual pipeline with lead status tracking
- **Lead Conversion**: Direct lead-to-retailer conversion functionality
- **Business Intelligence**: Inventory overview, recent orders, KPIs
- **Quick Actions**: Add new leads, manage pipeline, monitor performance

### Sales Manager Dashboard (`/sales_manager_dashboard.html`)
- **Lead Management**: Comprehensive lead tracking and management
- **Pipeline Analytics**: Detailed funnel visualization and metrics
- **Task Management**: Daily tasks, follow-ups, and activity feed
- **Performance Tracking**: Conversion rates, targets, and achievements
- **Quick Tools**: Bulk import, scheduling, reporting features

### Enhanced Retail Partner Dashboard (`/enhanced_retailer_dashboard.html`)
- **Inventory Management**: Real-time stock monitoring with status alerts
- **Stock Request System**: Automated replenishment requests with urgency levels
- **Performance Metrics**: Inventory turnover, accuracy, fulfillment rates
- **Communication Hub**: Direct supplier communication and notifications
- **Order Management**: Recent orders, status tracking, easy reordering

## 🛠 API Endpoints:

### CRM & Leads (`/leads/`)
- `GET /leads/` - List all leads with filtering options
- `POST /leads/` - Create new lead
- `GET /leads/{id}` - Get specific lead details
- `PUT /leads/{id}` - Update lead information
- `DELETE /leads/{id}` - Remove lead
- `POST /leads/{id}/convert` - Convert lead to retailer
- `GET /leads/stats/pipeline` - Get pipeline statistics

### Authentication (`/auth/`)
- `POST /auth/login` - User authentication (supports manufacturer, sales_manager, retailer roles)

### Products & Inventory (`/products/`, `/inventory/`)
- Complete CRUD operations for product management
- Real-time inventory tracking and updates

### Orders & Customers (`/orders/`, `/customers/`)
- Order processing and fulfillment tracking
- Customer/retailer management

## 🔐 User Credentials (Demo):
- **CEO/Manufacturer**: `manufacturer` / `password`
- **Sales Manager**: `sales_manager` / `password`  
- **Retailer**: `retailer1@example.com` / `password`

## 🚀 Quick Start:

### Installation & Setup:
```bash
# Clone the repository
git clone https://github.com/yashas-13/arivu.git
cd arivu

# Create virtual environment
python -m venv arivu-venv
source arivu-venv/bin/activate  # Linux/Mac
# arivu-venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn supply_chain_system.main:app --reload --port 8000
```

### Access Dashboards:
- **CEO Dashboard**: http://localhost:8000/ceo_dashboard.html
- **Sales Manager**: http://localhost:8000/sales_manager_dashboard.html
- **Retail Partner**: http://localhost:8000/enhanced_retailer_dashboard.html
- **API Documentation**: http://localhost:8000/docs

### Sample Data Included:
- 3 demonstration leads in various pipeline stages
- 2 sample products with inventory
- 1 converted retailer from lead conversion
- Sample orders and performance metrics

## Core Product Features:

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
- Analytics dashboards for manufacturer and retailer
- Email notifications (requires local SMTP server)
- Audit logging for sensitive actions
- Production batches with progress tracking
- Quality control checks
- Finished goods inventory
- Simple reporting endpoints
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
- **Manufacturer (Admin):**
  - Username: `manufacturer`
  - Password: `manufacturerpass`
- **Retailer:**
  - Username: `retailer1`
  - Password: `retailpass`

### 5. Registering new users
Manufacturers can self-register using `/manufacturer_register.html`.
Existing manufacturers may also create retailer accounts by opening `/register.html` while logged in.
When creating a retailer the frontend sends a special `admin_token` so that self-registration for retailers is blocked.

### 6. Features
 - Manufacturer dashboard: `/manufacturer_dashboard.html` (auto-redirect after manufacturer login)
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
