# Food Management System - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Database Schema](#database-schema)
4. [Core Features](#core-features)
5. [User Workflows](#user-workflows)
6. [API Endpoints](#api-endpoints)
7. [Security Features](#security-features)
8. [Internationalization](#internationalization)
9. [Deployment](#deployment)

---

## Project Overview

### What is this project?
This is a **Food & Beverage Point of Sale (POS) Portal** - a complete restaurant management system built with Flask (Python) and MySQL. It provides comprehensive functionality for managing restaurant operations including orders, menu items, expenses, clients, staff, and financial reporting.

### Technology Stack
- **Backend Framework**: Flask 2.3.3 (Python web framework)
- **Database**: MySQL 8.x with mysql-connector-python
- **Frontend**: HTML, CSS, JavaScript (with Bootstrap and custom styling)
- **Authentication**: Session-based with werkzeug password hashing
- **Security**: SSL/TLS support, security headers, input sanitization
- **Languages**: Bilingual support (English and Arabic)

### Key Capabilities
1. **Order Management**: Create, track, and manage customer orders
2. **Menu Management**: Manage menu items with categories and pricing
3. **Financial Tracking**: Track revenue, expenses, and generate reports
4. **Client Management**: Customer database with order history
5. **User Management**: Multi-user support with role-based access
6. **Refund System**: Process full and partial refunds
7. **Notification System**: Internal messaging and alerts
8. **WhatsApp Integration**: Send notifications via WhatsApp API

---

## System Architecture

### Application Structure
```
food_management/
├── food_management.py       # Main application file (5500+ lines)
├── wsgi.py                  # WSGI entry point for deployment
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates (Jinja2)
│   ├── base.html           # Base template with layout
│   ├── login.html          # Login page
│   ├── dashboard.html      # Main dashboard
│   ├── orders/             # Order management templates
│   ├── menu/               # Menu management templates
│   ├── expenses/           # Expense tracking templates
│   ├── finance/            # Financial reports templates
│   ├── clients/            # Client management templates
│   ├── users/              # User management templates
│   ├── notifications/      # Notification center templates
│   └── refunds/            # Refund management templates
├── uploads/                 # File upload directory
│   ├── profile/            # User profile pictures
│   ├── docs/               # User documents
│   ├── expenses/           # Expense receipts
│   └── menu/               # Menu item images
├── test_data.py            # Sample data generation script
└── test_finance.py         # Finance calculation tests
```

### Architecture Pattern
The application follows a **Monolithic Architecture** with:
- **Single-file application**: All routes and logic in `food_management.py`
- **MVC-like structure**: Templates (View), Flask routes (Controller), MySQL (Model)
- **Session-based state**: User sessions stored server-side
- **Direct database access**: SQL queries via mysql-connector

### Database Connection
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'ps',
    'password': 'Aa@123456',
    'database': 'food_management',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

---

## Database Schema

### Core Tables

#### 1. **users** - System Users
Stores staff and admin user accounts.
```sql
- id: INT (Primary Key)
- username: VARCHAR(50) UNIQUE
- password_hash: VARCHAR(255)
- role: ENUM('admin', 'staff')
- national_id: VARCHAR(20)
- name: VARCHAR(100)
- email: VARCHAR(100) UNIQUE
- address: TEXT
- age: INT
- employed_date: DATE
- title: VARCHAR(100)
- description: TEXT
- mobile: VARCHAR(20)
- profile_picture: VARCHAR(255)
- is_active: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

**Key Points**:
- Default admin: username='admin', password='admin123'
- Password stored as bcrypt hash
- Role-based access control (admin vs staff)

#### 2. **branches** - Restaurant Locations
Supports multi-branch operations.
```sql
- id: INT (Primary Key)
- name: VARCHAR(100)
- location: VARCHAR(255)
- is_active: BOOLEAN
- created_at: TIMESTAMP
```

#### 3. **user_branches** - User-Branch Assignment
Many-to-many relationship between users and branches.
```sql
- user_id: INT (FK to users)
- branch_id: INT (FK to branches)
- PRIMARY KEY (user_id, branch_id)
```

#### 4. **menu_categories** - Menu Organization
```sql
- id: INT (Primary Key)
- name: VARCHAR(100)
- description: TEXT
- is_active: BOOLEAN
- created_at: TIMESTAMP
```

**Default Categories**:
- Appetizers
- Main Courses
- Desserts
- Beverages
- Salads

#### 5. **menu_items** - Restaurant Menu
```sql
- id: INT (Primary Key)
- name: VARCHAR(100)              # English name
- arabic_name: VARCHAR(100)       # Arabic name
- description: TEXT
- price: DECIMAL(10, 2)
- category_id: INT (FK)
- image: VARCHAR(255)
- is_available: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

**Key Features**:
- Bilingual support (English/Arabic names)
- Price tracking with history
- Availability toggle

#### 6. **price_log** - Price Change Tracking
Audit trail for price changes.
```sql
- id: INT (Primary Key)
- menu_item_id: INT (FK)
- old_price: DECIMAL(10, 2)
- new_price: DECIMAL(10, 2)
- changed_by: INT (FK to users)
- change_reason: TEXT
- created_at: TIMESTAMP
```

#### 7. **clients** - Customer Database
```sql
- id: INT (Primary Key)
- name: VARCHAR(100)
- mobile: VARCHAR(20)
- email: VARCHAR(100)
- address: TEXT
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### 8. **orders** - Customer Orders
Central table for all order transactions.
```sql
- id: INT (Primary Key)
- client_id: INT (FK to clients)
- client_name: VARCHAR(100)
- client_mobile: VARCHAR(20)
- total_amount: DECIMAL(10, 2)
- status: ENUM('pending', 'completed', 'prepared', 'delivered', 'refunded', 'partially_refunded')
- refund_status: ENUM('none', 'requested', 'approved', 'processed')
- delivery_date: DATETIME
- notes: TEXT
- created_by: INT (FK to users)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

**Order Lifecycle**:
1. **pending** → Order created, not yet prepared
2. **prepared** → Food is ready for delivery/pickup
3. **completed** → Order fulfilled (in-house)
4. **delivered** → Order delivered to customer
5. **refunded** → Full refund processed
6. **partially_refunded** → Partial refund processed

#### 9. **order_items** - Order Line Items
```sql
- id: INT (Primary Key)
- order_id: INT (FK to orders)
- menu_item_id: INT (FK to menu_items)
- menu_item_name: VARCHAR(100)
- menu_item_arabic_name: VARCHAR(100)
- quantity: INT
- unit_price: DECIMAL(10, 2)
- subtotal: DECIMAL(10, 2)
```

**Why store names?**
- Historical record - even if menu item is deleted/renamed
- Price snapshot - preserves price at time of order

#### 10. **expense_categories** - Expense Types
```sql
- id: INT (Primary Key)
- name: VARCHAR(100)
- description: TEXT
- is_active: BOOLEAN
- created_at: TIMESTAMP
```

**Default Categories**:
- Ingredients
- Utilities
- Staff Salaries
- Equipment
- Marketing
- Rent
- Other

#### 11. **expenses** - Business Expenses
```sql
- id: INT (Primary Key)
- category_id: INT (FK)
- description: TEXT
- amount: DECIMAL(10, 2)
- expense_date: DATE
- receipt_document: VARCHAR(255)
- created_by: INT (FK to users)
- created_at: TIMESTAMP
```

#### 12. **refunds** - Refund Requests
```sql
- id: INT (Primary Key)
- order_id: INT (FK to orders)
- refund_amount: DECIMAL(10, 2)
- refund_type: ENUM('full', 'partial')
- refund_reason: TEXT
- refund_status: ENUM('pending', 'approved', 'rejected', 'processed')
- requested_by: INT (FK to users)
- approved_by: INT (FK to users)
- processed_by: INT (FK to users)
- request_date: TIMESTAMP
- approval_date: TIMESTAMP
- processed_date: TIMESTAMP
- notes: TEXT
```

**Refund Workflow**:
1. Staff requests refund → status='pending'
2. Admin approves/rejects → status='approved'/'rejected'
3. Admin processes refund → status='processed'
4. Order status updated to 'refunded' or 'partially_refunded'

#### 13. **notifications** - System Notifications
```sql
- id: INT (Primary Key)
- user_id: INT (FK, NULL for broadcast)
- message: TEXT
- is_read: BOOLEAN
- created_by: INT (FK to users)
- created_at: TIMESTAMP
```

**Types**:
- User-specific (user_id set)
- Broadcast (user_id = NULL)

#### 14. **business_settings** - Configuration
```sql
- id: INT (Primary Key)
- setting_key: VARCHAR(100) UNIQUE
- setting_value: TEXT
- updated_by: INT (FK to users)
- updated_at: TIMESTAMP
```

**Current Settings**:
- `starting_balance`: Initial capital for P&L calculations

#### 15. **user_documents** - Staff Documents
```sql
- id: INT (Primary Key)
- user_id: INT (FK to users)
- document_name: VARCHAR(255)
- file_path: VARCHAR(500)
- uploaded_at: TIMESTAMP
```

---

## Core Features

### 1. Authentication & Authorization

#### Login System
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Validates username/password
    # Checks password hash using check_password_hash()
    # Creates session with user_id, username, role, name
    # Redirects to dashboard
```

**Session Data**:
- `user_id`: User's database ID
- `username`: Login username
- `role`: 'admin' or 'staff'
- `name`: Display name
- `language`: User's language preference ('en' or 'ar')

#### Authorization Decorators
```python
@login_required  # Any authenticated user
@admin_required  # Admin role only
```

### 2. Dashboard

**URL**: `/dashboard`

**Displays**:
- Orders today (by delivery date)
- Revenue today (completed/delivered orders)
- Pending orders count
- Recent orders (last 5)
- Unread notifications
- Quick action buttons

**Statistics Calculation**:
```python
# Orders for today's delivery
SELECT COUNT(*) FROM orders WHERE DATE(delivery_date) = CURDATE()

# Revenue for today (only completed/delivered)
SELECT SUM(total_amount) FROM orders 
WHERE DATE(delivery_date) = CURDATE() 
AND status IN ('completed', 'delivered')
```

### 3. Menu Management

#### List Menu Items
**URL**: `/menu`

**Features**:
- Filter by category
- Search by name (English/Arabic)
- Filter by availability
- Display price and category
- Quick edit/delete actions

#### Add Menu Item
**URL**: `/menu/add`

**Fields**:
- English name (required)
- Arabic name (optional)
- Category (dropdown)
- Price (decimal)
- Description
- Image upload
- Availability toggle

**Price Change Logging**:
When price is updated, old price is logged in `price_log` table with:
- Old price
- New price
- Changed by (user)
- Change reason

#### Edit Menu Item
**URL**: `/menu/edit/<id>`

**Same fields as add, but pre-filled**

### 4. Order Management

#### Create Order
**URL**: `/orders/create`

**Process**:
1. **Select Menu Items**: Add items to cart with quantity
2. **Customer Information**:
   - Search existing customers (autocomplete)
   - Or enter new customer (name + mobile)
3. **Delivery Information**:
   - Delivery date/time picker
   - Order notes
4. **Place Order**: Creates order and order_items records

**Cart Management** (Client-side JavaScript):
- Add/remove items
- Increase/decrease quantity
- Calculate total dynamically
- Clear cart

**Database Transaction**:
```python
# Check/create client
if existing_client:
    client_id = existing_client.id
else:
    INSERT INTO clients (name, mobile) VALUES (...)
    client_id = lastrowid

# Create order
INSERT INTO orders (client_id, client_name, client_mobile, 
                   total_amount, delivery_date, created_by, ...)
order_id = lastrowid

# Create order items
for item in cart:
    INSERT INTO order_items (order_id, menu_item_id, name, 
                            quantity, unit_price, subtotal)
```

#### View Orders
**URL**: `/orders`

**Filters**:
- Status (pending, completed, prepared, delivered)
- Date range
- Search by client name/mobile

**Display**:
- Order ID
- Client information
- Total amount
- Status with color coding
- Delivery date
- Actions (view, edit status, refund)

#### Order Details
**URL**: `/orders/<id>`

**Shows**:
- Full client information
- Order items with quantities and prices
- Total amount
- Status history
- Notes
- Actions (change status, request refund, duplicate)

#### Update Order Status
**URL**: `/orders/update_status` (POST)

**Workflow**:
```
pending → prepared → delivered
        ↘ completed
```

**Business Logic**:
- Only certain status transitions allowed
- Status changes logged
- Can include notes for change

### 5. Expense Management

#### Add Expense
**URL**: `/expenses/add`

**Fields**:
- Category (dropdown)
- Description
- Amount
- Expense date
- Receipt upload (optional)

#### View Expenses
**URL**: `/expenses`

**Features**:
- Filter by category
- Filter by date range
- Search by description
- Display total expenses
- Download receipt documents

### 6. Financial Reports

#### Finance Dashboard
**URL**: `/finance`

**Report Types**:
1. **Profit & Loss Statement**
   - Starting balance
   - Revenue (from orders)
   - Expenses (from expenses table)
   - Net profit/loss
   
2. **Revenue Analysis**
   - Daily revenue breakdown
   - Order count trends
   - Average order value
   
3. **Expense Breakdown**
   - By category
   - Monthly trends
   - Top expense categories
   
4. **Daily Summary**
   - Orders per day
   - Revenue per day
   - Expenses per day
   
5. **Menu Performance**
   - Most ordered items
   - Revenue by item
   - Item popularity
   
6. **Monthly Trends**
   - Month-over-month comparison
   - Growth rates
   
7. **Tax Summary**
   - VAT calculations (if applicable)
   
8. **Refund Analysis**
   - Refund rate
   - Total refunds
   - Refund reasons

#### Generate Report
**URL**: `/finance/generate`

**Parameters**:
- Report type (dropdown)
- Date range (start/end)
- Export format (PDF/CSV/Excel)

**Calculation Example** (Profit & Loss):
```python
# Get starting balance
SELECT setting_value FROM business_settings 
WHERE setting_key = 'starting_balance'

# Get revenue
SELECT SUM(total_amount) FROM orders 
WHERE delivery_date BETWEEN start_date AND end_date
AND status IN ('completed', 'delivered')

# Get expenses
SELECT SUM(amount) FROM expenses 
WHERE expense_date BETWEEN start_date AND end_date

# Calculate
profit_loss = revenue - expenses
ending_balance = starting_balance + profit_loss
```

### 7. Client Management

#### Client List
**URL**: `/clients`

**Analytics**:
- Total clients
- Active clients (with orders)
- Total revenue
- Average client value
- New clients this month
- Top clients by orders

#### Client Details
**URL**: `/clients/<id>`

**Information**:
- Contact details
- Order statistics
  - Total orders
  - Total spent
  - Average order value
  - Last order date
- Recent orders (last 20)
- Monthly order trends (last 12 months)
- Favorite items (most ordered)

**Favorite Items Query**:
```sql
SELECT menu_item_name, SUM(quantity) as total_quantity
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
WHERE o.client_id = ?
GROUP BY menu_item_id
ORDER BY total_quantity DESC
LIMIT 10
```

#### Edit Client
**URL**: `/clients/edit/<id>`

**Editable Fields**:
- Name
- Mobile
- Email
- Address

### 8. User Management (Admin Only)

#### User List
**URL**: `/users`

**Features**:
- Add new users
- Edit user details
- Activate/deactivate users
- Delete users
- Bulk actions (activate, deactivate, delete)
- Export users to CSV
- View user details in modal

#### Add User
**URL**: `/users/add`

**Fields**:
- Username (unique)
- Password
- Role (admin/staff)
- Full name
- Email
- National ID
- Address
- Age
- Employed date
- Title
- Description
- Mobile
- Profile picture upload
- Branch assignments (multi-select)
- Document uploads (multiple files)

#### Edit User
**URL**: `/users/edit/<id>`

**Same fields as add, plus**:
- Change password (optional)
- View assigned branches

**Security**:
- Username uniqueness check
- Email validation
- Password hashing before storage
- Prevent self-deletion

### 9. Notification System

#### Notification Center
**URL**: `/notifications`

**Types**:
- System notifications
- Order notifications
- Inventory alerts

**Actions**:
- Mark as read
- Mark all as read
- Delete notification
- Filter by type

#### Send Notification
**URL**: `/notifications/send` (Admin only)

**Options**:
- Send to all users (broadcast)
- Send to specific user
- Custom message

**Database**:
```sql
-- Broadcast (all users)
INSERT INTO notifications (user_id, message, created_by)
VALUES (NULL, ?, ?)

-- Specific user
INSERT INTO notifications (user_id, message, created_by)
VALUES (?, ?, ?)
```

### 10. Refund System

#### Refund Management
**URL**: `/refunds`

**List Shows**:
- Refund ID
- Order number
- Customer name
- Refund amount
- Refund type (full/partial)
- Status (pending, approved, rejected, processed)
- Requested by
- Request date
- Actions

#### Request Refund
**URL**: `/request_refund/<order_id>`

**Process**:
1. Select refund type (full/partial)
2. If partial, enter amount
3. Enter reason
4. Submit request
5. Order refund_status → 'requested'
6. Notification sent to admin

#### Approve Refund
**URL**: `/approve_refund/<refund_id>` (POST)

**Action**:
- Update refund status → 'approved'
- Set approved_by and approval_date
- Order refund_status → 'approved'

#### Reject Refund
**URL**: `/reject_refund/<refund_id>` (POST)

**Action**:
- Update refund status → 'rejected'
- Add rejection notes
- Order refund_status → 'none'

#### Process Refund
**URL**: `/process_refund/<refund_id>` (POST)

**Action**:
- Update refund status → 'processed'
- Set processed_by and processed_date
- Update order status:
  - Full refund → 'refunded'
  - Partial refund → 'partially_refunded'
- Order refund_status → 'processed'

---

## User Workflows

### Workflow 1: Taking a Customer Order

```
1. Staff logs in → Dashboard
2. Click "Create New Order"
3. Browse menu items (filter by category)
4. Click items to add to cart
   - Set quantity
   - Add special instructions (optional)
5. Cart updates with total
6. Enter customer information:
   - Search existing customer OR
   - Enter new customer (name + mobile)
7. Set delivery date/time
8. Add order notes (optional)
9. Click "Place Order"
10. Order created with status='pending'
11. Receipt can be printed
12. WhatsApp notification sent to customer (if configured)
```

### Workflow 2: Kitchen Preparation

```
1. Kitchen staff views pending orders
2. Filter by delivery_date = TODAY
3. Prepare food items
4. Mark order as "Prepared & Ready"
5. Status changes: pending → prepared
6. Customer notified (if WhatsApp enabled)
```

### Workflow 3: Order Delivery

```
1. Delivery staff views prepared orders
2. Pick up order
3. Deliver to customer
4. Mark as "Delivered"
5. Status changes: prepared → delivered
6. Revenue counted in financial reports
```

### Workflow 4: Processing a Refund

```
1. Customer requests refund
2. Staff opens order details
3. Click "Request Refund"
4. Select type (full/partial)
5. Enter amount (if partial)
6. Enter reason
7. Submit → refund_status='requested'
8. Admin reviews refund list
9. Admin approves refund
10. Admin processes refund
11. Order status → 'refunded' or 'partially_refunded'
12. Customer receives refund
```

### Workflow 5: Generating Financial Reports

```
1. Admin logs in
2. Navigate to Finance section
3. Select report type (e.g., Profit & Loss)
4. Set date range
5. Click "Generate Report"
6. View report with:
   - Starting balance
   - Total revenue
   - Total expenses
   - Net profit/loss
   - Charts and graphs
7. Export to PDF/CSV/Excel (optional)
```

---

## API Endpoints

### REST-like JSON APIs

#### 1. Menu Items
```
GET /api/menu_items
Returns: List of all available menu items with categories
Response: {
  "success": true,
  "menu_items": [
    {
      "id": 1,
      "name": "Burger",
      "arabic_name": "برجر",
      "price": 15.99,
      "category_name": "Main Courses",
      "is_available": true
    },
    ...
  ]
}
```

#### 2. Customer Search
```
GET /api/customers/search?q=<query>
Returns: Matching customers for autocomplete
Response: [
  {
    "id": 1,
    "name": "John Doe",
    "mobile": "1234567890",
    "email": "john@example.com",
    "address": "123 Main St"
  },
  ...
]
```

#### 3. Order Details
```
GET /api/order/<order_id>
Returns: Full order details with items
Response: {
  "id": 123,
  "client_name": "John Doe",
  "total_amount": 45.50,
  "status": "pending",
  "items": [
    {
      "name": "Burger",
      "quantity": 2,
      "unit_price": 15.99,
      "subtotal": 31.98
    },
    ...
  ]
}
```

#### 4. Username Availability
```
GET /api/check-username?username=<username>
Returns: Whether username is available
Response: {
  "available": true,
  "message": "Username is available"
}
```

#### 5. Email Availability
```
GET /api/check-email?email=<email>
Returns: Whether email is available
Response: {
  "available": false,
  "message": "Email is already registered"
}
```

#### 6. User Details
```
GET /api/get-user-details?id=<user_id>
Returns: Full user information
Response: {
  "id": 1,
  "username": "admin",
  "full_name": "System Administrator",
  "role": "admin",
  "email": "admin@example.com",
  "branch_names": "Main Branch, North Branch",
  ...
}
```

#### 7. Client Analytics
```
GET /api/clients/analytics
Returns: Client analytics data
Response: {
  "client_growth": [
    {"year": 2025, "month": 1, "new_clients": 15},
    ...
  ],
  "frequency_distribution": [
    {"frequency_range": "1-5 Orders", "client_count": 42},
    ...
  ],
  "top_spenders": [
    {"name": "John Doe", "total_spent": 1250.00},
    ...
  ]
}
```

### AJAX Action Endpoints

#### Update Order Status
```
POST /orders/update_status
Body: {
  "order_id": 123,
  "status": "completed",
  "notes": "Customer satisfied"
}
Response: {
  "success": true,
  "message": "Order status updated"
}
```

#### Toggle User Status
```
POST /users/toggle-status
Body: {
  "user_id": 5
}
Response: {
  "success": true,
  "message": "User activated successfully"
}
```

#### Delete User
```
POST /users/delete
Body: {
  "user_id": 5
}
Response: {
  "success": true,
  "message": "User john_doe deleted successfully"
}
```

#### Bulk User Action
```
POST /users/bulk-action
Body: {
  "user_ids": [2, 3, 4],
  "action": "deactivate"
}
Response: {
  "success": true,
  "message": "Successfully deactivated 3 user(s)"
}
```

#### Mark Notification Read
```
POST /notifications/mark_read/<notification_id>
Response: {
  "success": true
}
```

#### Mark All Notifications Read
```
POST /notifications/mark_all_read
Response: {
  "success": true,
  "message": "5 notifications marked as read"
}
```

---

## Security Features

### 1. Authentication & Session Management
- **Password Hashing**: Uses `werkzeug.security.generate_password_hash()`
- **Secure Sessions**: Flask session with secret key
- **Login Required**: Decorators protect all authenticated routes
- **Role-Based Access**: Admin-only routes protected

### 2. Input Validation & Sanitization
- **SQL Injection Prevention**: Parameterized queries with mysql-connector
- **File Upload Security**:
  - Filename sanitization with `secure_filename()`
  - Extension whitelist: `txt, pdf, png, jpg, jpeg, gif, doc, docx`
  - Path traversal prevention with `safe_join()`
- **Form Validation**: Server-side validation of all inputs

### 3. Security Headers
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; ..."
```

### 4. SSL/TLS Support
- HTTPS enabled if `cert.pem` and `key.pem` exist
- TLS 1.2+ with secure SSL context
- Automatic HTTP to HTTPS upgrade

### 5. Access Control
- **File Access**: Uploaded files require login
- **User Isolation**: Users can't delete themselves
- **Admin Protection**: Critical operations require admin role
- **Branch Isolation**: Users assigned to specific branches (future feature)

### 6. CSRF Protection (Missing - Recommendation)
**Current State**: No CSRF tokens implemented
**Recommendation**: Add Flask-WTF for CSRF protection

### 7. Rate Limiting (Missing - Recommendation)
**Current State**: No rate limiting
**Recommendation**: Add Flask-Limiter for API rate limiting

---

## Internationalization (i18n)

### Supported Languages
- English (en) - Default
- Arabic (ar)

### Translation System

#### Translation Dictionary
```python
TRANSLATIONS = {
    'en': {
        'Dashboard': 'Dashboard',
        'Orders': 'Orders',
        ...
    },
    'ar': {
        'Dashboard': 'لوحة التحكم',
        'Orders': 'الطلبات',
        ...
    }
}
```

#### Translation Function
```python
def _(text):
    """Get translation for current language"""
    language = session.get('language', 'en')
    return TRANSLATIONS.get(language, {}).get(text, text)
```

#### Template Usage
```html
<h1>{{ _('Dashboard') }}</h1>
<button>{{ _('Create New Order') }}</button>
```

### Language Direction
- English: Left-to-Right (LTR)
- Arabic: Right-to-Left (RTL)

```python
def get_language_direction():
    return 'rtl' if get_current_language() == 'ar' else 'ltr'
```

### Switch Language
```
GET /set_language/<language>
- Sets session['language']
- Redirects back to previous page
```

### Bilingual Data
Menu items support both English and Arabic names:
```sql
SELECT name, arabic_name FROM menu_items
```

Display logic:
```python
# Show Arabic name if available and language is Arabic
display_name = item.arabic_name if (language == 'ar' and item.arabic_name) else item.name
```

---

## Deployment

### Development Server

#### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USER=ps
export MYSQL_PASSWORD=Aa@123456
export MYSQL_DB=food_management
export SECRET_KEY=your-secret-key

# Run application
python food_management.py
```

#### Access
- **HTTP**: http://localhost:4009
- **HTTPS**: https://localhost:4009 (if SSL certs exist)

### Production Deployment

#### WSGI Configuration
File: `wsgi.py`
```python
from food_management import app
application = app
```

#### uWSGI Configuration
File: `foodie.ini`
```ini
[uwsgi]
module = wsgi:application
master = true
processes = 4
threads = 2
socket = /tmp/food_management.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```

#### Run with uWSGI
```bash
uwsgi --ini foodie.ini
```

### Nginx Configuration (Example)
```nginx
server {
    listen 443 ssl;
    server_name foodie.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/food_management.sock;
    }
    
    location /uploads {
        alias /path/to/uploads;
    }
}
```

### Environment Variables
```bash
# Database
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=ps
MYSQL_PASSWORD=Aa@123456
MYSQL_DB=food_management

# Application
SECRET_KEY=your-random-secret-key-here
UPLOAD_DIR=/path/to/uploads

# WhatsApp API (if using)
WHATSAPP_API_TOKEN=your-token-here
```

### Database Setup
```bash
# Create database
mysql -u root -p
CREATE DATABASE food_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Application will auto-create tables on first run
python food_management.py
```

### File Permissions
```bash
# Upload directory must be writable
chmod 755 uploads/
chmod 755 uploads/profile/
chmod 755 uploads/docs/
chmod 755 uploads/expenses/
chmod 755 uploads/menu/
```

### SSL Certificates
```bash
# Generate self-signed certificate (development)
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365

# Production: Use Let's Encrypt
certbot certonly --nginx -d foodie.example.com
```

### Systemd Service (Linux)
File: `/etc/systemd/system/food-management.service`
```ini
[Unit]
Description=Food Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/food_management
Environment="PATH=/var/www/food_management/venv/bin"
ExecStart=/var/www/food_management/venv/bin/uwsgi --ini foodie.ini

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable food-management
sudo systemctl start food-management
sudo systemctl status food-management
```

---

## WhatsApp Integration

### Configuration
```python
def send_wa_nini_kitchen(mobile, message):
    url = "https://www.wasenderapi.com/api/send-message"
    headers = {
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
    }
    data = {
        "to": f"+20{mobile}",  # Egypt country code
        "text": message
    }
    response = requests.post(url, json=data, headers=headers)
```

### Use Cases
- Order confirmation to customer
- Order ready notification
- Delivery notification
- Refund processed notification

### Mobile Number Format
- Removes spaces and special characters
- Handles Egyptian numbers (+20 prefix)
- Validates length (minimum 10 digits)

---

## Testing

### Test Data Generation
```bash
python test_data.py
```

Creates:
- 5 menu items
- 4 clients
- 14 orders (last 7 days)
- 5 expenses

### Finance Calculations Test
```bash
python test_finance.py
```

Validates:
- Revenue calculations
- Expense calculations
- Profit/loss calculations
- Daily breakdowns
- Category summaries

---

## Key Business Logic

### Revenue Recognition
Revenue is counted when order status is:
- `completed` OR `delivered`

Pending orders are NOT counted in revenue.

### Order Total Calculation
```python
total = sum(item.quantity * item.unit_price for item in order_items)
```

### Profit/Loss Calculation
```python
profit_loss = (revenue from completed orders) - (expenses) + starting_balance
```

### Client Value Calculation
```python
client_value = sum(order.total_amount for order in client.orders)
avg_order_value = client_value / order_count
```

### Menu Performance
```python
# Most ordered item
SELECT menu_item_name, SUM(quantity) as total_qty
FROM order_items
GROUP BY menu_item_id
ORDER BY total_qty DESC
```

---

## Database Migrations

The application includes automatic migration system in `run_migrations()`:

### Migration 1: Add delivery_date
```sql
ALTER TABLE orders 
ADD COLUMN delivery_date DATE NOT NULL DEFAULT (CURDATE())
```

### Migration 2: Add email to users
```sql
ALTER TABLE users 
ADD COLUMN email VARCHAR(100) UNIQUE
```

### Migration 3: Add arabic_name to menu_items
```sql
ALTER TABLE menu_items 
ADD COLUMN arabic_name VARCHAR(100) AFTER name
```

### Migration 4: Add menu_item_arabic_name to order_items
```sql
ALTER TABLE order_items 
ADD COLUMN menu_item_arabic_name VARCHAR(100) AFTER menu_item_name
```

### Migration 5: Add refund support
```sql
ALTER TABLE orders 
ADD COLUMN refund_status ENUM('none', 'requested', 'approved', 'processed')

ALTER TABLE orders 
MODIFY COLUMN status ENUM('pending', 'completed', 'delivered', 'refunded', 'partially_refunded')

CREATE TABLE refunds (...)
```

### Migration 6: Update delivery_date to DATETIME
```sql
ALTER TABLE orders 
MODIFY COLUMN delivery_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
```

### Migration 7: Add 'prepared' status
```sql
ALTER TABLE orders 
MODIFY COLUMN status ENUM('pending', 'completed', 'prepared', 'delivered', 'refunded', 'partially_refunded')
```

---

## Common Queries

### Get Today's Orders
```sql
SELECT * FROM orders 
WHERE DATE(delivery_date) = CURDATE()
ORDER BY created_at DESC
```

### Get Pending Orders
```sql
SELECT * FROM orders 
WHERE status = 'pending' AND DATE(delivery_date) = CURDATE()
ORDER BY delivery_date ASC
```

### Get Top Clients
```sql
SELECT c.*, COUNT(o.id) as order_count, SUM(o.total_amount) as total_spent
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id
GROUP BY c.id
ORDER BY total_spent DESC
LIMIT 10
```

### Get Menu Performance
```sql
SELECT 
    oi.menu_item_name,
    SUM(oi.quantity) as total_ordered,
    SUM(oi.subtotal) as total_revenue,
    COUNT(DISTINCT oi.order_id) as order_count
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
WHERE o.status IN ('completed', 'delivered')
GROUP BY oi.menu_item_id
ORDER BY total_revenue DESC
```

### Get Expense Breakdown
```sql
SELECT 
    ec.name as category,
    COUNT(e.id) as expense_count,
    SUM(e.amount) as total_amount
FROM expense_categories ec
LEFT JOIN expenses e ON ec.id = e.category_id
WHERE e.expense_date BETWEEN ? AND ?
GROUP BY ec.id
ORDER BY total_amount DESC
```

---

## Troubleshooting

### Database Connection Issues
```python
# Check DB_CONFIG settings
# Ensure MySQL server is running
# Verify credentials and permissions
```

### Upload Directory Permissions
```bash
# Ensure directories exist and are writable
mkdir -p uploads/{profile,docs,expenses,menu}
chmod -R 755 uploads/
```

### SSL Certificate Errors
```bash
# For development, use self-signed cert
# Browser will show warning - can be ignored
# For production, use valid SSL cert from Let's Encrypt
```

### Session Issues
```python
# Ensure SECRET_KEY is set
# Check session cookie settings
# Clear browser cookies if needed
```

### Database Migration Failures
```sql
-- Check if column exists before adding
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'orders' AND COLUMN_NAME = 'delivery_date'

-- If migration failed, may need to run manually
```

---

## Future Enhancements

### Recommended Improvements

1. **CSRF Protection**
   - Add Flask-WTF
   - Implement CSRF tokens on all forms

2. **API Rate Limiting**
   - Add Flask-Limiter
   - Prevent API abuse

3. **Inventory Management**
   - Track ingredient stock
   - Low stock alerts
   - Auto-deduction on orders

4. **Table Management**
   - Restaurant table/seat assignment
   - QR code ordering

5. **Loyalty Program**
   - Points system
   - Rewards tracking
   - Discount codes

6. **Advanced Analytics**
   - Peak hours analysis
   - Staff performance metrics
   - Customer retention analysis

7. **Multi-tenancy**
   - Support multiple restaurants
   - Separate databases or tenant isolation

8. **Mobile App**
   - Customer mobile app
   - Staff mobile app for order management

9. **Payment Integration**
   - Stripe, PayPal integration
   - Cash, card, online payment tracking

10. **Reservation System**
    - Table reservations
    - Event booking

---

## Conclusion

This Food Management System is a comprehensive, production-ready restaurant POS application with:

✅ **Complete order lifecycle management**
✅ **Financial tracking and reporting**
✅ **Multi-user support with role-based access**
✅ **Bilingual interface (English/Arabic)**
✅ **Client relationship management**
✅ **Refund processing**
✅ **Notification system**
✅ **WhatsApp integration**
✅ **Security features**
✅ **SSL/TLS support**
✅ **Export capabilities**

The system is built using industry-standard technologies and follows best practices for web application development. It's suitable for small to medium-sized restaurants and food service businesses.

For questions or support, refer to the code comments in `food_management.py` which is extensively documented.
