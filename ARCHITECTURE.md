# Food Management System - Architecture Overview

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web        │  │   Mobile     │  │   Tablet     │          │
│  │   Browser    │  │   Browser    │  │   Browser    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └──────────────────┼──────────────────┘                   │
│                            │                                      │
│                   HTTPS / HTTP                                   │
└────────────────────────────┼──────────────────────────────────────┘
                             │
┌────────────────────────────▼──────────────────────────────────────┐
│                    Web Server Layer                               │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              Nginx (Reverse Proxy)                       │     │
│  │  • SSL/TLS Termination                                   │     │
│  │  • Static File Serving                                   │     │
│  │  • Load Balancing (optional)                             │     │
│  └─────────────────────┬───────────────────────────────────┘     │
│                        │                                          │
│                   Unix Socket                                     │
└────────────────────────┼──────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                Application Server Layer                           │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              uWSGI / Gunicorn                            │     │
│  │  • WSGI Interface                                        │     │
│  │  • Process Management                                    │     │
│  │  • Request Handling                                      │     │
│  └─────────────────────┬───────────────────────────────────┘     │
│                        │                                          │
│                   WSGI Protocol                                   │
└────────────────────────┼──────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                   Application Layer                               │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │           Flask Application (food_management.py)         │     │
│  │                                                           │     │
│  │  ┌─────────────────────────────────────────────────┐    │     │
│  │  │          Authentication & Session                │    │     │
│  │  │  • Login/Logout                                  │    │     │
│  │  │  • Role-Based Access Control                     │    │     │
│  │  │  • Session Management                            │    │     │
│  │  └─────────────────────────────────────────────────┘    │     │
│  │                                                           │     │
│  │  ┌─────────────────────────────────────────────────┐    │     │
│  │  │          Business Logic Layer                    │    │     │
│  │  │                                                   │    │     │
│  │  │  ┌──────────────┐  ┌──────────────┐            │    │     │
│  │  │  │Order         │  │Menu          │            │    │     │
│  │  │  │Management    │  │Management    │            │    │     │
│  │  │  └──────────────┘  └──────────────┘            │    │     │
│  │  │  ┌──────────────┐  ┌──────────────┐            │    │     │
│  │  │  │Expense       │  │Client        │            │    │     │
│  │  │  │Management    │  │Management    │            │    │     │
│  │  │  └──────────────┘  └──────────────┘            │    │     │
│  │  │  ┌──────────────┐  ┌──────────────┐            │    │     │
│  │  │  │Finance       │  │User          │            │    │     │
│  │  │  │Reports       │  │Management    │            │    │     │
│  │  │  └──────────────┘  └──────────────┘            │    │     │
│  │  │  ┌──────────────┐  ┌──────────────┐            │    │     │
│  │  │  │Refund        │  │Notification  │            │    │     │
│  │  │  │System        │  │System        │            │    │     │
│  │  │  └──────────────┘  └──────────────┘            │    │     │
│  │  └─────────────────────────────────────────────────┘    │     │
│  │                                                           │     │
│  │  ┌─────────────────────────────────────────────────┐    │     │
│  │  │          Data Access Layer                       │    │     │
│  │  │  • Database Connections                          │    │     │
│  │  │  • Query Execution                               │    │     │
│  │  │  • Transaction Management                        │    │     │
│  │  └─────────────────────────────────────────────────┘    │     │
│  │                                                           │     │
│  │  ┌─────────────────────────────────────────────────┐    │     │
│  │  │          Template Engine (Jinja2)                │    │     │
│  │  │  • HTML Rendering                                │    │     │
│  │  │  • Template Inheritance                          │    │     │
│  │  │  • Internationalization                          │    │     │
│  │  └─────────────────────────────────────────────────┘    │     │
│  └─────────────────────┬───────────────────────────────────┘     │
└────────────────────────┼──────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                   Database Layer                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │               MySQL Database Server                      │     │
│  │  • food_management database                             │     │
│  │  • 15 tables with relationships                          │     │
│  │  • utf8mb4 character set                                │     │
│  └─────────────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                   Storage Layer                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              File System Storage                         │     │
│  │  • /uploads/profile/    - Profile pictures              │     │
│  │  • /uploads/docs/       - User documents                │     │
│  │  • /uploads/expenses/   - Expense receipts              │     │
│  │  • /uploads/menu/       - Menu item images              │     │
│  └─────────────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│                   External Services                               │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              WhatsApp API Integration                    │     │
│  │  • wasenderapi.com                                       │     │
│  │  • Order notifications                                   │     │
│  │  • Customer alerts                                       │     │
│  └─────────────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Presentation Layer (Templates)

**Responsibilities**:
- Render HTML pages
- Display data to users
- Capture user input
- Client-side validation
- Internationalization (i18n)

**Technologies**:
- Jinja2 templating
- HTML5
- CSS3 (Bootstrap framework)
- JavaScript (vanilla + jQuery)
- AJAX for dynamic updates

**Key Templates**:
```
templates/
├── base.html                 # Master layout
├── login.html               # Authentication
├── dashboard.html           # Main dashboard
├── orders/
│   ├── list.html           # Order listing
│   ├── create.html         # New order form
│   ├── view.html           # Order details
│   └── receipt.html        # Printable receipt
├── menu/
│   ├── list.html           # Menu items
│   ├── add.html            # Add menu item
│   └── edit.html           # Edit menu item
├── finance/
│   └── reports.html        # Financial reports
└── ...
```

### 2. Application Layer (Flask Routes)

**Responsibilities**:
- Route HTTP requests
- Execute business logic
- Manage sessions
- Enforce authorization
- Return responses

**Route Organization**:
```python
# Authentication
/login                       POST - Login user
/logout                      GET  - Logout user
/set_language/<lang>        GET  - Change language

# Dashboard
/dashboard                   GET  - Main dashboard

# Orders
/orders                      GET  - List orders
/orders/create              GET  - Order form
/orders/create              POST - Create order
/orders/<id>                GET  - Order details
/orders/update_status       POST - Update status
/orders/receipt/<id>        GET  - Generate receipt

# Menu
/menu                        GET  - List menu items
/menu/add                   GET/POST - Add item
/menu/edit/<id>             GET/POST - Edit item
/menu/delete/<id>           POST - Delete item

# Expenses
/expenses                    GET  - List expenses
/expenses/add               GET/POST - Add expense

# Finance
/finance                     GET  - Finance dashboard
/finance/generate           POST - Generate report

# Clients
/clients                     GET  - List clients
/clients/<id>               GET  - Client details
/clients/edit/<id>          GET/POST - Edit client

# Users (Admin)
/users                       GET  - List users
/users/add                  GET/POST - Add user
/users/edit/<id>            GET/POST - Edit user
/users/delete               POST - Delete user

# Refunds
/refunds                     GET  - List refunds
/request_refund/<order_id>  GET/POST - Request refund
/approve_refund/<id>        POST - Approve refund
/process_refund/<id>        POST - Process refund

# Notifications
/notifications               GET  - List notifications
/notifications/send         GET/POST - Send notification
/notifications/mark_read    POST - Mark as read

# API Endpoints
/api/menu_items             GET  - Menu items JSON
/api/customers/search       GET  - Search customers
/api/order/<id>             GET  - Order details JSON
```

### 3. Business Logic Layer

**Responsibilities**:
- Implement business rules
- Data validation
- Calculations (totals, profit/loss)
- State transitions (order status)
- Access control enforcement

**Key Functions**:
```python
# Authentication
login_required(f)           # Decorator for auth
admin_required(f)           # Decorator for admin

# Database
get_db_connection()         # Get MySQL connection
create_database_if_not_exists()
create_tables()
seed_initial_data()
run_migrations()

# User Management
get_user_by_id(user_id)

# Utilities
allowed_file(filename)      # Check file extension
safe_join(dir, filename)    # Prevent path traversal
_(text)                     # Translation function
get_current_language()      # Get user language
```

### 4. Data Access Layer

**Responsibilities**:
- Database connections
- SQL query execution
- Transaction management
- Data mapping

**Connection Pattern**:
```python
def database_operation():
    connection = get_db_connection()
    if not connection:
        # Handle error
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT ...")
        results = cursor.fetchall()
        
        # Modify data
        cursor.execute("INSERT ...")
        connection.commit()
        
        return results
    except Error as e:
        logger.error(f"Database error: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
```

### 5. Security Layer

**Responsibilities**:
- Authentication
- Authorization
- Input sanitization
- CSRF protection (future)
- Rate limiting (future)
- Security headers

**Implementation**:
```python
# Password Security
from werkzeug.security import generate_password_hash, check_password_hash

# File Upload Security
from werkzeug.utils import secure_filename

# Security Headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    # ... more headers
```

## Data Flow Diagrams

### Order Creation Flow

```
┌─────────┐       ┌─────────┐       ┌──────────┐       ┌──────────┐
│  User   │──1──▶ │  Flask  │──2──▶ │  MySQL   │──3──▶ │ WhatsApp │
│ Browser │       │  Route  │       │ Database │       │   API    │
└─────────┘       └─────────┘       └──────────┘       └──────────┘
     │                 │                  │                  │
     │  Submit Form    │                  │                  │
     ├────────────────▶│                  │                  │
     │                 │  Validate Data   │                  │
     │                 ├─────────────────▶│                  │
     │                 │                  │                  │
     │                 │  Get/Create      │                  │
     │                 │  Client          │                  │
     │                 ├─────────────────▶│                  │
     │                 │◀─────────────────┤                  │
     │                 │                  │                  │
     │                 │  Insert Order    │                  │
     │                 ├─────────────────▶│                  │
     │                 │◀─────────────────┤                  │
     │                 │  (order_id)      │                  │
     │                 │                  │                  │
     │                 │  Insert Order    │                  │
     │                 │  Items           │                  │
     │                 ├─────────────────▶│                  │
     │                 │◀─────────────────┤                  │
     │                 │                  │                  │
     │                 │  Commit          │                  │
     │                 │  Transaction     │                  │
     │                 ├─────────────────▶│                  │
     │                 │                  │                  │
     │                 │  Send            │                  │
     │                 │  Notification    │                  │
     │                 ├──────────────────┼─────────────────▶│
     │                 │                  │                  │
     │  Redirect to    │                  │                  │
     │  Order Details  │                  │                  │
     │◀────────────────┤                  │                  │
     │                 │                  │                  │
```

### Authentication Flow

```
┌─────────┐       ┌─────────┐       ┌──────────┐
│  User   │       │  Flask  │       │  MySQL   │
│ Browser │       │  Route  │       │ Database │
└─────────┘       └─────────┘       └──────────┘
     │                 │                  │
     │  POST /login    │                  │
     ├────────────────▶│                  │
     │  username +     │                  │
     │  password       │                  │
     │                 │  Query User      │
     │                 ├─────────────────▶│
     │                 │                  │
     │                 │  User Record     │
     │                 │◀─────────────────┤
     │                 │  (with hash)     │
     │                 │                  │
     │                 │  Verify Password │
     │                 │  (bcrypt)        │
     │                 │                  │
     │                 │  Create Session  │
     │                 │  - user_id       │
     │                 │  - username      │
     │                 │  - role          │
     │                 │  - name          │
     │                 │                  │
     │  Set-Cookie:    │                  │
     │  session=...    │                  │
     │◀────────────────┤                  │
     │                 │                  │
     │  Redirect to    │                  │
     │  /dashboard     │                  │
     │◀────────────────┤                  │
     │                 │                  │
```

### Financial Report Generation Flow

```
┌─────────┐       ┌─────────┐       ┌──────────┐
│  User   │       │  Flask  │       │  MySQL   │
│ Browser │       │  Route  │       │ Database │
└─────────┘       └─────────┘       └──────────┘
     │                 │                  │
     │  POST /finance/ │                  │
     │  generate       │                  │
     ├────────────────▶│                  │
     │  report_type +  │                  │
     │  date_range     │                  │
     │                 │                  │
     │                 │  Get Starting    │
     │                 │  Balance         │
     │                 ├─────────────────▶│
     │                 │◀─────────────────┤
     │                 │                  │
     │                 │  Get Revenue     │
     │                 │  (Orders)        │
     │                 ├─────────────────▶│
     │                 │◀─────────────────┤
     │                 │                  │
     │                 │  Get Expenses    │
     │                 ├─────────────────▶│
     │                 │◀─────────────────┤
     │                 │                  │
     │                 │  Calculate       │
     │                 │  - Profit/Loss   │
     │                 │  - Percentages   │
     │                 │  - Trends        │
     │                 │                  │
     │                 │  Render Report   │
     │                 │  Template        │
     │                 │                  │
     │  Display Report │                  │
     │  with Charts    │                  │
     │◀────────────────┤                  │
     │                 │                  │
```

## Database Design Patterns

### 1. Denormalization for Performance

**Order Items Table**:
Instead of just storing `menu_item_id`, we also store:
- `menu_item_name` (English)
- `menu_item_arabic_name` (Arabic)
- `unit_price` (at time of order)

**Reason**: 
- Historical accuracy - if menu item is deleted/renamed
- Price preservation - price at time of order
- Faster queries - no joins needed for order display

### 2. Soft Deletes

**Implementation**:
Tables have `is_active` boolean field:
- `users.is_active`
- `menu_items.is_available`
- `branches.is_active`

**Benefits**:
- Preserve historical data
- Can reactivate if needed
- Audit trail

### 3. Foreign Key Relationships

```sql
orders.client_id → clients.id
orders.created_by → users.id
order_items.order_id → orders.id (CASCADE)
order_items.menu_item_id → menu_items.id
expenses.category_id → expense_categories.id
expenses.created_by → users.id
refunds.order_id → orders.id (CASCADE)
```

**Cascade Deletes**:
- Delete order → delete all order_items
- Delete order → delete all refunds

### 4. Audit Fields

Most tables include:
- `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- `updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
- `created_by INT` (foreign key to users)

### 5. Enum for Status Fields

```sql
status ENUM('pending', 'completed', 'prepared', 'delivered', 'refunded', 'partially_refunded')
refund_status ENUM('none', 'requested', 'approved', 'processed')
role ENUM('admin', 'staff')
```

**Benefits**:
- Data integrity
- Performance (stored as integers)
- Self-documenting

## Scalability Considerations

### Current Limitations

1. **Single Server**:
   - All components on one server
   - Database and app on same machine

2. **Session Storage**:
   - Server-side sessions (not distributed)
   - Won't work with multiple app servers

3. **File Uploads**:
   - Stored on local file system
   - Not suitable for multi-server setup

4. **No Caching**:
   - Every request hits database
   - Repeated queries not cached

### Scalability Path

#### Phase 1: Vertical Scaling
```
Current: 1 server (2 CPU, 4GB RAM)
↓
Upgraded: 1 server (8 CPU, 16GB RAM)
```

#### Phase 2: Database Separation
```
┌──────────────┐
│  App Server  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  DB Server   │
└──────────────┘
```

#### Phase 3: Horizontal Scaling
```
┌──────────────┐     ┌──────────────┐
│  App Server  │     │  App Server  │
│      1       │     │      2       │
└──────┬───────┘     └──────┬───────┘
       │                    │
       └──────────┬─────────┘
                  ▼
          ┌──────────────┐
          │ Load Balancer│
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │  DB Server   │
          └──────────────┘
```

**Requirements**:
- Switch to Redis for session storage
- Use S3/MinIO for file uploads
- Add Redis for caching
- Implement connection pooling

#### Phase 4: Microservices (Future)
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Order     │  │    Menu     │  │  Finance    │
│  Service    │  │  Service    │  │  Service    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
                 ┌─────────────┐
                 │   API       │
                 │  Gateway    │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  Database   │
                 │  Cluster    │
                 └─────────────┘
```

## Deployment Architectures

### Development Environment
```
┌───────────────────────────────┐
│      Developer Laptop         │
│  ┌─────────────────────────┐  │
│  │  Flask Dev Server       │  │
│  │  (python app.py)        │  │
│  │  Port: 4009             │  │
│  └──────────┬──────────────┘  │
│             │                  │
│  ┌──────────▼──────────────┐  │
│  │  MySQL (Local)          │  │
│  │  Port: 3306             │  │
│  └─────────────────────────┘  │
└───────────────────────────────┘
```

### Production Environment (Single Server)
```
┌────────────────────────────────────────┐
│          Production Server              │
│  ┌──────────────────────────────────┐  │
│  │  Nginx (Port 80, 443)            │  │
│  │  • Reverse Proxy                 │  │
│  │  • SSL Termination               │  │
│  │  • Static Files                  │  │
│  └────────┬─────────────────────────┘  │
│           │                             │
│  ┌────────▼─────────────────────────┐  │
│  │  uWSGI (Unix Socket)             │  │
│  │  • 4 Worker Processes            │  │
│  │  • 2 Threads per Process         │  │
│  └────────┬─────────────────────────┘  │
│           │                             │
│  ┌────────▼─────────────────────────┐  │
│  │  Flask Application               │  │
│  │  (food_management.py)            │  │
│  └────────┬─────────────────────────┘  │
│           │                             │
│  ┌────────▼─────────────────────────┐  │
│  │  MySQL (localhost)               │  │
│  │  Port: 3306                      │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  File System                     │  │
│  │  /var/www/uploads/               │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

### Production Environment (Multi-Server)
```
                    Internet
                       │
                       ▼
             ┌─────────────────┐
             │  Load Balancer  │
             │  (Nginx/HAProxy)│
             └────────┬────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │  App   │  │  App   │  │  App   │
    │Server 1│  │Server 2│  │Server 3│
    └───┬────┘  └───┬────┘  └───┬────┘
        │           │            │
        └───────────┼────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ Redis  │ │ MySQL  │ │  S3/   │
    │Session │ │Primary │ │ MinIO  │
    │ Store  │ │        │ │ Files  │
    └────────┘ └───┬────┘ └────────┘
                   │
                   ▼
              ┌────────┐
              │ MySQL  │
              │Replica │
              │(Read)  │
              └────────┘
```

## Technology Stack Details

### Backend
- **Python**: 3.12+
- **Flask**: 2.3.3 - Web framework
- **mysql-connector-python**: 8.1.0 - Database driver
- **Werkzeug**: 2.3.7 - WSGI utilities, password hashing
- **Jinja2**: 3.1.2 - Template engine
- **python-dotenv**: 1.0.0 - Environment variables

### Database
- **MySQL**: 8.x
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Bootstrap 5.x framework
- **JavaScript**: Vanilla JS + jQuery
- **Icons**: Font Awesome
- **Charts**: Chart.js (for financial reports)

### Deployment
- **Web Server**: Nginx 1.18+
- **App Server**: uWSGI 2.0.30
- **Process Manager**: systemd
- **SSL**: Let's Encrypt (certbot)

### Development Tools
- **IDE**: Any Python IDE (VS Code, PyCharm)
- **Database Client**: MySQL Workbench, phpMyAdmin
- **API Testing**: Postman, curl
- **Browser DevTools**: Chrome/Firefox

---

This architecture documentation provides a comprehensive overview of the system design, component interactions, data flows, and deployment strategies for the Food Management System.
