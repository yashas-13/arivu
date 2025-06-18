
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
    * **Application Instance (`inventory_app/__init__.py`):** Initializes the web framework application, configures middleware (e.g., CORS, authentication), and registers blueprints/routers.
    * **Database Module (`inventory_app/database.py`):** Manages database connection pooling, session creation, and ORM setup. Provides session objects for service/API layers.
    * **Models (`inventory_app/models/`):** ORM representations of the database schema. Used by the Service layer to interact with the DB.
    * **Services (`inventory_app/services/`):**
        * **Business Logic Encapsulation:** Contains methods for all core business operations, independent of HTTP specifics.
        * Example:
            * `inventory_service.update_product_stock(product_id, quantity_change, operation_type)`
            * `production_service.create_production_batch(product_id, planned_quantity)`
            * `sales_service.process_customer_order(order_payload)`
        * **Transaction Management:** Ensures atomicity of complex operations (e.g., deducting raw materials while incrementing finished goods in a production completion).
    * **API Endpoints (`inventory_app/api/`):**
        * **HTTP Interface:** Defines RESTful endpoints that Frontend clients send requests to.
        * **Authentication:** Verifies user identity (e.g., token validation).
        * **Authorization (Role-Based Access Control - RBAC):** Crucial for differentiating dashboard access.
            * Decorators or middleware associated with specific endpoints check the authenticated user's `role` from the `User` model.
            * Example:
                * `/api/production/batches` (POST, PUT, GET): Only accessible to `manufacturer` and `admin` roles.
                * `/api/orders` (POST, GET): Accessible to `retailer` and `admin` roles.
                * `/api/products/stock` (GET): Accessible to both `manufacturer` and `retailer` roles (but `manufacturer` might see more granular production-related details).
        * **Request Handling:** Parses incoming JSON payloads, calls appropriate methods in the `services` layer, and constructs JSON responses.

---

### 3. The Frontend - The User Interface Layer

* **Role:** Provides the visual and interactive interface for users (Manufacturer or Retailer) to interact with the IMS.
* **Technologies:** HTML (for structure), CSS (for styling), JavaScript (for dynamic behavior and API calls).
* **Key Components & Their Interplay:**
    * **HTML Templates (`inventory_app/templates/`):**
        * `manufacturer_dashboard.html`: Contains specific structural elements for production schedules, raw material displays, QC logs.
        * `retailer_dashboard.html`: Contains specific structural elements for sales charts, order lists, finished goods stock.
        * `base.html`: Common layout for navigation, header, footer.
        * The backend's web framework (e.g., Flask) renders the appropriate template based on the user's role and route.
    * **JavaScript (`inventory_app/static/js/`):**
        * **Asynchronous API Calls (AJAX/Fetch API):**
            * **Manufacturer Dashboard JS:**
                * `GET /api/production/batches`: Fetches current and planned production orders.
                * `GET /api/raw_materials/stock`: Fetches real-time raw material inventory levels.
                * `POST /api/production/batches/{id}/complete`: Sends a request to mark a batch as completed.
            * **Retailer Dashboard JS:**
                * `GET /api/sales/daily`: Fetches daily sales figures.
                * `GET /api/orders?status=pending`: Fetches pending customer orders.
                * `PUT /api/orders/{id}/status`: Updates an order's status (e.g., to 'shipped').
                * `GET /api/products/stock?type=finished_goods`: Fetches available finished product stock.
            * These requests typically include the user's authentication token in the headers.
        * **DOM Manipulation:** Updates the HTML elements dynamically based on JSON data received from the backend APIs (e.g., populating tables, rendering charts using libraries like Chart.js or D3.js).
        * **Event Listeners:** Reacts to user interactions (button clicks, form submissions) to trigger API calls.
        * **Conditional Rendering:** Basic UI elements might be hidden/shown based on user role detected on the frontend (e.g., a "Start Production" button only visible for manufacturers), but *true security relies on backend authorization*.

---

### The Data Flow - How They Connect Technically:

1.  **User Logs In:**
    * Frontend (login.html + JS) sends `POST /api/auth/login` with `username` and `password`.
    * Backend (api/auth.py) authenticates against `User` table in DB. If successful, returns an **authentication token** and the user's `role`.
    * Frontend stores the token (e.g., in `localStorage`).

2.  **Dashboard Load/Interaction:**
    * **Manufacturer:**
        * Frontend loads `manufacturer_dashboard.html`.
        * JS makes `GET` requests to backend endpoints like `/api/production/batches` and `/api/raw_materials/stock`, including the auth token.
        * Backend's API layer:
            * Validates token.
            * Checks user's role (e.g., `is_manufacturer()`).
            * Calls `production_service.get_batches()` and `inventory_service.get_raw_material_stock()`.
            * Services query the DB (`ProductionBatch`, `RawMaterial` tables).
            * Backend sends JSON data.
        * Frontend JS receives JSON, parses it, and renders charts/tables.
        * If the manufacturer clicks "Complete Batch," Frontend sends `PUT /api/production/batches/{id}/complete`.
        * Backend updates `ProductionBatch` status and `Product.current_stock_quantity` in DB via `services`.
    * **Retailer:**
        * Frontend loads `retailer_dashboard.html`.
        * JS makes `GET` requests to backend endpoints like `/api/sales/daily` and `/api/products/stock`.
        * Backend's API layer:
            * Validates token.
            * Checks user's role (e.g., `is_retailer()`).
            * Calls `sales_service.get_daily_sales()` and `inventory_service.get_finished_goods_stock()`.
            * Services query the DB (`Order`, `OrderItem`, `Product` tables).
            * Backend sends JSON data.
        * Frontend JS receives JSON, parses it, and renders charts/tables.
        * If the retailer clicks "Mark Order Shipped," Frontend sends `PUT /api/orders/{id}/status`.
        * Backend updates `Order.status` in DB via `services`.

This architecture ensures that both dashboards, though visually distinct and role-segregated, operate on the same canonical data, managed and secured by a robust backend service layer.
