
## Technical Interconnection: Frontend, Backend, Database for AI Code Agent

**Core Principle:** Both Manufacturer and Retailer dashboards are distinct **clients** of a **single, unified backend API**, which in turn interacts with a **single, shared relational database**. The distinction between dashboards lies in the **presentation layer (Frontend UI)** and the **authorization layer (Backend API)** that filters data and actions based on user roles.

---

### 1. The Database (DB) - The Persistent Data Layer

* **Role:** The immutable, centralized data store for all IMS entities. It guarantees data consistency and ACID properties.
* **Technologies:** Typically a Relational Database Management System (RDBMS) like PostgreSQL, MySQL, or SQLite for development.
* **Schema (Shared Models):**
    * `Product` table: Stores `product_id (PK)`, `name`, `sku`, `category`, `mrp`, `current_stock_quantity`, `unit_of_measure`, `is_active`.
    * `RawMaterial` table: Stores `material_id (PK)`, `name`, `current_stock_quantity`, `unit_of_measure`, `reorder_point`, `supplier_id (FK)`.
    * `ProductionBatch` table: Stores `batch_id (PK)`, `product_id (FK)`, `production_date`, `quantity_produced`, `status` (`planned`, `in_progress`, `completed`, `qc_failed`), `cost_per_unit`.
    * `Order` table: Stores `order_id (PK)`, `customer_id (FK)`, `order_date`, `total_amount`, `status` (`pending`, `processing`, `shipped`, `delivered`, `canceled`).
    * `OrderItem` table: Stores `order_item_id (PK)`, `order_id (FK)`, `product_id (FK)`, `quantity`, `unit_price`.
    * `User` table: Stores `user_id (PK)`, `username`, `hashed_password`, `role` (`manufacturer`, `retailer`, `admin`).
* **Interaction Method:** SQL queries (via an ORM or direct SQL).

---

### 2. The Backend - The Application Logic & API Layer

* **Role:** Acts as the intermediary between the Frontend and the Database. It enforces business rules, handles authentication/authorization, processes requests, and prepares data.
* **Technologies:** Python (e.g., Flask, FastAPI), paired with an ORM (e.g., SQLAlchemy) for database interaction.
* **Key Components & Their Interplay:**
    * **Application Instance (`supply_chain_system/main.py`):** Initializes the FastAPI application, configures middleware, and registers routers.
    * **Database Module (`supply_chain_system/database/`):** Manages the SQLite engine, session creation and exposes SQLAlchemy models.
    * **Models (`supply_chain_system/database/models.py`):** ORM tables for products, inventory, orders and more.
    * **Router Modules:** Each feature (inventory, orders, production, etc.) has a router under `supply_chain_system/` that interacts with the database models directly.
    * **API Endpoints:**
        * **HTTP Interface:** Defines RESTful endpoints that Frontend clients send requests to.
        * **Authentication:** Verifies user identity (e.g., token validation).
        * **Authorization (Role-Based Access Control - RBAC):** Crucial for differentiating dashboard access.
            * Decorators or middleware associated with specific endpoints check the authenticated user's `role` from the `User` model.
            * Example:
                * `/production` (POST, PUT, GET): Only accessible to `manufacturer` and `admin` roles.
                * `/orders` (POST, GET): Accessible to `retailer` and `admin` roles.
                * `/products/{id}/stock` (GET): Accessible to both `manufacturer` and `retailer` roles (the manufacturer may see additional data).
        * **Request Handling:** Parses incoming JSON payloads, performs DB actions and returns JSON responses.

---

### 3. The Frontend - The User Interface Layer

* **Role:** Provides the visual and interactive interface for users (Manufacturer or Retailer) to interact with the IMS.
* **Technologies:** HTML (for structure), CSS (for styling), JavaScript (for dynamic behavior and API calls).
* **Key Components & Their Interplay:**
    * **HTML Files (`frontend/*.html`):**
        * `manufacturer_dashboard.html`: Contains specific structural elements for production schedules, raw material displays, QC logs.
        * `retailer_dashboard.html`: Contains specific structural elements for sales charts, order lists, finished goods stock.
        * `base.html`: Common layout for navigation, header, footer.
        * The FastAPI backend serves these pages directly.
    * **JavaScript (`frontend/api.js`):**
        * **Asynchronous API Calls (AJAX/Fetch API):**
            * **Manufacturer Dashboard JS:**
                * `GET /production` lists batches.
                * `GET /inventory` fetches raw material inventory levels.
                * `POST /production` creates or updates batches.
            * **Retailer Dashboard JS:**
                * `GET /dashboard/retailer/{id}` fetches metrics.
                * `GET /orders` lists orders.
                * `PUT /orders/{id}/status` updates an order.
                * `GET /products/{id}/stock` returns finished product stock.
            * These requests typically include the user's authentication token in the headers.
        * **DOM Manipulation:** Updates the HTML elements dynamically based on JSON data received from the backend APIs (e.g., populating tables, rendering charts using libraries like Chart.js or D3.js).
        * **Event Listeners:** Reacts to user interactions (button clicks, form submissions) to trigger API calls.
        * **Conditional Rendering:** Basic UI elements might be hidden/shown based on user role detected on the frontend (e.g., a "Start Production" button only visible for manufacturers), but *true security relies on backend authorization*.

---

### The Data Flow - How They Connect Technically:

1.  **User Logs In:**
    * Frontend (login.html + JS) sends `POST /auth/login` with `username` and `password`.
    * Backend (api/auth.py) authenticates against `User` table in DB. If successful, returns an **authentication token** and the user's `role`.
    * Frontend stores the token (e.g., in `localStorage`).

2.  **Dashboard Load/Interaction:**
    * **Manufacturer:**
        * Frontend loads `manufacturer_dashboard.html`.
        * JS makes `GET` requests to backend endpoints like `/production` and `/inventory`, including the auth token.
        * Backend's API layer:
            * Validates token.
            * Checks user's role (e.g., `is_manufacturer()`).
            * The router functions query `ProductionBatchModel` and `RawMaterialModel` tables.
            * Backend sends JSON data.
        * Frontend JS receives JSON, parses it, and renders charts/tables.
        * If the manufacturer updates progress, the frontend sends `POST /production` or `PATCH /production/{id}/progress`.
        * Backend updates `ProductionBatchModel` and related product stock.
    * **Retailer:**
        * Frontend loads `retailer_dashboard.html`.
        * JS makes `GET` requests to backend endpoints like `/dashboard/retailer/{id}` and `/products/{id}/stock`.
        * Backend's API layer:
            * Validates token.
            * Checks user's role (e.g., `is_retailer()`).
            * Router functions aggregate data from `OrderModel`, `OrderItemModel` and `ProductModel` tables.
            * Backend sends JSON data.
        * Frontend JS receives JSON, parses it, and renders charts/tables.
        * If the retailer clicks "Mark Order Shipped," the frontend sends `PUT /orders/{id}/status`.
        * Backend updates `OrderModel.status` in the database.

This architecture ensures that both dashboards, though visually distinct and role-segregated, operate on the same canonical data, managed and secured by a robust backend service layer.
