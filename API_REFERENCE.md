# Food Management System - API Reference

## Table of Contents
1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [REST API Endpoints](#rest-api-endpoints)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Code Examples](#code-examples)

---

## API Overview

### Base URL
```
Development: http://localhost:4009
Production: https://your-domain.com
```

### API Versioning
Currently, the API does not use versioning. All endpoints are at the root level.

### Authentication Method
- **Session-based authentication** using Flask sessions
- Login required for all API endpoints
- Cookies must be enabled

### Content Type
- **Request**: `application/json` or `application/x-www-form-urlencoded`
- **Response**: `application/json`

---

## Authentication

### Login
Authenticate user and create session.

**Endpoint**: `POST /login`

**Request Body**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Success Response** (302 Redirect):
```
HTTP/1.1 302 FOUND
Location: /dashboard
Set-Cookie: session=...; Path=/; HttpOnly
```

**Error Response** (200):
```html
<!-- Login page with error message -->
```

**Example**:
```bash
curl -X POST http://localhost:4009/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" \
  -c cookies.txt
```

### Logout
End user session.

**Endpoint**: `GET /logout`

**Response** (302 Redirect):
```
HTTP/1.1 302 FOUND
Location: /login
Set-Cookie: session=; Expires=Thu, 01 Jan 1970 00:00:00 GMT
```

**Example**:
```bash
curl -X GET http://localhost:4009/logout \
  -b cookies.txt
```

### Set Language
Change user's language preference.

**Endpoint**: `GET /set_language/<language>`

**Parameters**:
- `language`: `en` (English) or `ar` (Arabic)

**Response** (302 Redirect):
```
HTTP/1.1 302 FOUND
Location: <referrer>
```

**Example**:
```bash
curl -X GET http://localhost:4009/set_language/ar \
  -b cookies.txt
```

---

## REST API Endpoints

### 1. Menu Items API

#### Get All Menu Items
Retrieve list of all available menu items.

**Endpoint**: `GET /api/menu_items`

**Authentication**: Required

**Response**:
```json
{
  "success": true,
  "menu_items": [
    {
      "id": 1,
      "name": "Burger",
      "arabic_name": "برجر",
      "description": "Classic beef burger",
      "price": 15.99,
      "category_id": 2,
      "category_name": "Main Courses",
      "image": "20250120_burger.jpg",
      "is_available": true,
      "created_at": "2025-01-15 10:30:00",
      "updated_at": "2025-01-15 10:30:00"
    },
    {
      "id": 2,
      "name": "Pizza",
      "arabic_name": "بيتزا",
      "description": "Margherita pizza",
      "price": 18.50,
      "category_id": 2,
      "category_name": "Main Courses",
      "image": null,
      "is_available": true,
      "created_at": "2025-01-15 10:35:00",
      "updated_at": "2025-01-15 10:35:00"
    }
  ]
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Database connection error"
}
```

**Example**:
```bash
curl -X GET http://localhost:4009/api/menu_items \
  -b cookies.txt \
  -H "Accept: application/json"
```

**Usage**:
Used for populating order creation forms with available menu items.

---

### 2. Customer Search API

#### Search Customers
Search for customers by name or mobile number (autocomplete).

**Endpoint**: `GET /api/customers/search`

**Authentication**: Required

**Query Parameters**:
- `q` (string, required): Search query (minimum 2 characters)

**Response**:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "mobile": "1234567890",
    "email": "john@example.com",
    "address": "123 Main St, City"
  },
  {
    "id": 5,
    "name": "Jane Doe",
    "mobile": "0987654321",
    "email": "jane@example.com",
    "address": "456 Elm St, Town"
  }
]
```

**Empty Response** (no matches):
```json
[]
```

**Example**:
```bash
curl -X GET "http://localhost:4009/api/customers/search?q=john" \
  -b cookies.txt \
  -H "Accept: application/json"
```

**Usage**:
Used for customer autocomplete in order creation form.

---

### 3. Order API

#### Get Order Details
Retrieve full details of a specific order.

**Endpoint**: `GET /api/order/<order_id>`

**Authentication**: Required

**Path Parameters**:
- `order_id` (integer): Order ID

**Response**:
```json
{
  "id": 123,
  "client_id": 5,
  "client_name": "John Doe",
  "client_mobile": "1234567890",
  "total_amount": 45.48,
  "status": "pending",
  "refund_status": "none",
  "delivery_date": "2025-01-20 14:00:00",
  "notes": "Extra sauce please",
  "created_by": 1,
  "created_at": "2025-01-19 10:15:00",
  "updated_at": "2025-01-19 10:15:00",
  "items": [
    {
      "id": 456,
      "menu_item_id": 1,
      "menu_item_name": "Burger",
      "menu_item_arabic_name": "برجر",
      "quantity": 2,
      "unit_price": 15.99,
      "subtotal": 31.98
    },
    {
      "id": 457,
      "menu_item_id": 4,
      "menu_item_name": "Coffee",
      "menu_item_arabic_name": "قهوة",
      "quantity": 3,
      "unit_price": 4.50,
      "subtotal": 13.50
    }
  ]
}
```

**Error Response** (404):
```json
{
  "error": "Order not found"
}
```

**Example**:
```bash
curl -X GET http://localhost:4009/api/order/123 \
  -b cookies.txt \
  -H "Accept: application/json"
```

---

### 4. User Management API

#### Check Username Availability
Check if a username is available for registration.

**Endpoint**: `GET /api/check-username`

**Authentication**: Required

**Query Parameters**:
- `username` (string, required): Username to check

**Response**:
```json
{
  "available": true,
  "message": "Username is available"
}
```

**Error Response**:
```json
{
  "available": false,
  "message": "Username is already taken"
}
```

**Validation Rules**:
- Minimum 3 characters
- Must be unique

**Example**:
```bash
curl -X GET "http://localhost:4009/api/check-username?username=newuser" \
  -b cookies.txt \
  -H "Accept: application/json"
```

---

#### Check Email Availability
Check if an email is available for registration.

**Endpoint**: `GET /api/check-email`

**Authentication**: Required

**Query Parameters**:
- `email` (string, required): Email to check

**Response**:
```json
{
  "available": true,
  "message": "Email is available"
}
```

**Error Response**:
```json
{
  "available": false,
  "message": "Email is already registered"
}
```

**Validation Rules**:
- Must contain `@` symbol
- Must be unique

**Example**:
```bash
curl -X GET "http://localhost:4009/api/check-email?email=new@example.com" \
  -b cookies.txt \
  -H "Accept: application/json"
```

---

#### Get User Details
Retrieve full user information.

**Endpoint**: `GET /api/get-user-details`

**Authentication**: Required

**Query Parameters**:
- `id` (integer, required): User ID

**Response**:
```json
{
  "id": 1,
  "username": "admin",
  "full_name": "System Administrator",
  "email": "admin@example.com",
  "role": "admin",
  "national_id": "12345678901234",
  "address": "123 Admin St",
  "age": 35,
  "employed_date": "2020-01-01",
  "title": "System Administrator",
  "description": "Main system administrator",
  "mobile": "1234567890",
  "profile_picture": "admin_profile.jpg",
  "is_active": true,
  "branch_names": "Main Branch, North Branch",
  "created_at": "2020-01-01 00:00:00"
}
```

**Error Response** (404):
```json
{
  "error": "User not found"
}
```

**Example**:
```bash
curl -X GET "http://localhost:4009/api/get-user-details?id=1" \
  -b cookies.txt \
  -H "Accept: application/json"
```

---

### 5. Client Analytics API

#### Get Client Analytics
Retrieve analytics data about clients.

**Endpoint**: `GET /api/clients/analytics`

**Authentication**: Required

**Response**:
```json
{
  "client_growth": [
    {
      "year": 2025,
      "month": 1,
      "new_clients": 15
    },
    {
      "year": 2024,
      "month": 12,
      "new_clients": 22
    }
  ],
  "frequency_distribution": [
    {
      "frequency_range": "1-5 Orders",
      "client_count": 42
    },
    {
      "frequency_range": "6-15 Orders",
      "client_count": 18
    },
    {
      "frequency_range": "16-30 Orders",
      "client_count": 5
    },
    {
      "frequency_range": "30+ Orders",
      "client_count": 2
    },
    {
      "frequency_range": "No Orders",
      "client_count": 10
    }
  ],
  "top_spenders": [
    {
      "name": "John Doe",
      "mobile": "1234567890",
      "total_spent": 1250.50
    },
    {
      "name": "Jane Smith",
      "mobile": "0987654321",
      "total_spent": 980.75
    }
  ]
}
```

**Error Response**:
```json
{
  "error": "Database connection error"
}
```

**Example**:
```bash
curl -X GET http://localhost:4009/api/clients/analytics \
  -b cookies.txt \
  -H "Accept: application/json"
```

**Usage**:
Used for populating charts and graphs in client analytics dashboard.

---

## Action Endpoints (POST)

### 1. Update Order Status

**Endpoint**: `POST /orders/update_status`

**Authentication**: Required

**Request Body**:
```json
{
  "order_id": 123,
  "status": "completed",
  "notes": "Customer satisfied with order"
}
```

**Valid Status Values**:
- `pending`
- `prepared`
- `completed`
- `delivered`
- `refunded`
- `partially_refunded`

**Response**:
```json
{
  "success": true,
  "message": "Order status updated successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Invalid status"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/orders/update_status \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 123,
    "status": "completed",
    "notes": "Order fulfilled"
  }'
```

---

### 2. Toggle User Status

**Endpoint**: `POST /users/toggle-status`

**Authentication**: Required (Admin only)

**Request Body**:
```json
{
  "user_id": 5
}
```

**Response**:
```json
{
  "success": true,
  "message": "User activated successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "User not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/users/toggle-status \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"user_id": 5}'
```

---

### 3. Delete User

**Endpoint**: `POST /users/delete`

**Authentication**: Required (Admin only)

**Request Body**:
```json
{
  "user_id": 5
}
```

**Response**:
```json
{
  "success": true,
  "message": "User john_doe deleted successfully"
}
```

**Error Responses**:
```json
{
  "success": false,
  "message": "You cannot delete your own account"
}
```

```json
{
  "success": false,
  "message": "User not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/users/delete \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"user_id": 5}'
```

---

### 4. Bulk User Actions

**Endpoint**: `POST /users/bulk-action`

**Authentication**: Required (Admin only)

**Request Body**:
```json
{
  "user_ids": [2, 3, 4],
  "action": "deactivate"
}
```

**Valid Actions**:
- `activate`
- `deactivate`
- `delete`

**Response**:
```json
{
  "success": true,
  "message": "Successfully deactivated 3 user(s)",
  "errors": []
}
```

**Partial Success Response**:
```json
{
  "success": true,
  "message": "Successfully deactivated 2 user(s). 1 error(s) occurred.",
  "errors": [
    "User ID 4 not found"
  ]
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/users/bulk-action \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [2, 3, 4],
    "action": "deactivate"
  }'
```

---

### 5. Mark Notification Read

**Endpoint**: `POST /notifications/mark_read/<notification_id>`

**Authentication**: Required

**Path Parameters**:
- `notification_id` (integer): Notification ID

**Response**:
```json
{
  "success": true
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Notification not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/notifications/mark_read/42 \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

---

### 6. Mark All Notifications Read

**Endpoint**: `POST /notifications/mark_all_read`

**Authentication**: Required

**Response**:
```json
{
  "success": true,
  "message": "5 notifications marked as read"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/notifications/mark_all_read \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

---

### 7. Delete Notification

**Endpoint**: `POST /notifications/delete`

**Authentication**: Required

**Request Body**:
```json
{
  "notification_id": 42
}
```

**Response**:
```json
{
  "success": true
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Notification not found or access denied"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/notifications/delete \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"notification_id": 42}'
```

---

### 8. Request Refund

**Endpoint**: `POST /request_refund/<order_id>`

**Authentication**: Required

**Path Parameters**:
- `order_id` (integer): Order ID

**Request Body**:
```json
{
  "refund_type": "partial",
  "refund_amount": 25.50,
  "refund_reason": "Item was cold when delivered"
}
```

**Valid Refund Types**:
- `full`: Full order refund (amount = order total)
- `partial`: Partial refund (specify amount)

**Response**:
```json
{
  "success": true,
  "message": "Refund requested successfully"
}
```

**Error Responses**:
```json
{
  "success": false,
  "message": "Order not found"
}
```

```json
{
  "success": false,
  "message": "Invalid refund amount"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/request_refund/123 \
  -b cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "refund_type=partial&refund_amount=25.50&refund_reason=Item was cold"
```

---

### 9. Approve Refund

**Endpoint**: `POST /approve_refund/<refund_id>`

**Authentication**: Required (Admin)

**Path Parameters**:
- `refund_id` (integer): Refund request ID

**Response**:
```json
{
  "success": true,
  "message": "Refund approved successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Refund not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/approve_refund/10 \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

---

### 10. Reject Refund

**Endpoint**: `POST /reject_refund/<refund_id>`

**Authentication**: Required (Admin)

**Path Parameters**:
- `refund_id` (integer): Refund request ID

**Request Body**:
```json
{
  "notes": "Customer not eligible for refund per policy"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Refund rejected successfully"
}
```

**Example**:
```bash
curl -X POST http://localhost:4009/reject_refund/10 \
  -b cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "notes=Not eligible per policy"
```

---

### 11. Process Refund

**Endpoint**: `POST /process_refund/<refund_id>`

**Authentication**: Required (Admin)

**Path Parameters**:
- `refund_id` (integer): Refund request ID

**Response**:
```json
{
  "success": true,
  "message": "Refund processed successfully"
}
```

**Side Effects**:
- Updates order status to `refunded` or `partially_refunded`
- Sets refund_status to `processed`
- Records processed_by and processed_date

**Example**:
```bash
curl -X POST http://localhost:4009/process_refund/10 \
  -b cookies.txt \
  -H "Content-Type: application/json"
```

---

## Response Format

### Success Response Structure
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response Structure
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

### HTTP Status Codes
- `200 OK`: Request successful
- `302 Found`: Redirect (for HTML responses)
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not authorized
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Error Handling

### Common Error Types

#### Authentication Error
```json
{
  "success": false,
  "message": "Please log in to access this page."
}
```

**HTTP Status**: 302 (redirect to /login)

#### Authorization Error
```json
{
  "success": false,
  "message": "Admin access required."
}
```

**HTTP Status**: 302 (redirect to /dashboard)

#### Database Error
```json
{
  "success": false,
  "message": "Database connection error"
}
```

**HTTP Status**: 200 (with error in JSON)

#### Validation Error
```json
{
  "success": false,
  "message": "Username and password are required"
}
```

**HTTP Status**: 200 (with error in JSON)

#### Not Found Error
```json
{
  "error": "Resource not found"
}
```

**HTTP Status**: 404

---

## Rate Limiting

**Current Status**: Not implemented

**Recommendation**: Implement rate limiting using Flask-Limiter

**Suggested Limits**:
- Login: 5 requests per minute per IP
- API endpoints: 100 requests per minute per user
- Public endpoints: 20 requests per minute per IP

**Example Implementation** (future):
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: session.get('user_id'))

@app.route('/api/menu_items')
@limiter.limit("100/minute")
def api_menu_items():
    # ...
```

---

## Code Examples

### JavaScript/jQuery Example

```javascript
// Get menu items
$.ajax({
    url: '/api/menu_items',
    method: 'GET',
    dataType: 'json',
    success: function(response) {
        if (response.success) {
            response.menu_items.forEach(function(item) {
                console.log(item.name + ' - $' + item.price);
            });
        }
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});

// Search customers
$('#customer-search').on('input', function() {
    const query = $(this).val();
    if (query.length >= 2) {
        $.get('/api/customers/search', { q: query }, function(customers) {
            // Display autocomplete results
            customers.forEach(function(customer) {
                console.log(customer.name + ' - ' + customer.mobile);
            });
        });
    }
});

// Update order status
function updateOrderStatus(orderId, newStatus) {
    $.ajax({
        url: '/orders/update_status',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            order_id: orderId,
            status: newStatus,
            notes: 'Status updated via API'
        }),
        success: function(response) {
            if (response.success) {
                alert('Order status updated!');
            } else {
                alert('Error: ' + response.message);
            }
        }
    });
}
```

### Python Requests Example

```python
import requests

# Login
session = requests.Session()
login_data = {
    'username': 'admin',
    'password': 'admin123'
}
response = session.post('http://localhost:4009/login', data=login_data)

# Get menu items
response = session.get('http://localhost:4009/api/menu_items')
menu_data = response.json()

if menu_data['success']:
    for item in menu_data['menu_items']:
        print(f"{item['name']} - ${item['price']}")

# Create order (would need to submit form)
order_data = {
    'client_name': 'John Doe',
    'client_mobile': '1234567890',
    'delivery_date': '2025-01-25 14:00',
    'notes': 'Extra napkins please',
    'cart': [
        {'item_id': 1, 'quantity': 2},
        {'item_id': 4, 'quantity': 1}
    ]
}
response = session.post('http://localhost:4009/orders/create', json=order_data)

# Update order status
status_update = {
    'order_id': 123,
    'status': 'completed'
}
response = session.post('http://localhost:4009/orders/update_status', json=status_update)
result = response.json()
print(result['message'])
```

### cURL Examples

```bash
# Login and save session
curl -X POST http://localhost:4009/login \
  -d "username=admin&password=admin123" \
  -c cookies.txt \
  -L

# Get menu items
curl http://localhost:4009/api/menu_items \
  -b cookies.txt

# Search customers
curl "http://localhost:4009/api/customers/search?q=john" \
  -b cookies.txt

# Update order status
curl -X POST http://localhost:4009/orders/update_status \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"order_id": 123, "status": "completed"}'

# Request refund
curl -X POST http://localhost:4009/request_refund/123 \
  -b cookies.txt \
  -d "refund_type=partial&refund_amount=25.50&refund_reason=Cold food"

# Mark notification read
curl -X POST http://localhost:4009/notifications/mark_read/42 \
  -b cookies.txt
```

---

## Best Practices

### 1. Session Management
Always include cookies with requests to maintain session:
```javascript
$.ajax({
    url: '/api/endpoint',
    xhrFields: {
        withCredentials: true
    }
});
```

### 2. Error Handling
Always check `success` field before processing data:
```javascript
if (response.success) {
    // Process data
} else {
    // Handle error
    console.error(response.message);
}
```

### 3. Loading States
Show loading indicator during API calls:
```javascript
$('#loading').show();
$.get('/api/menu_items', function(data) {
    $('#loading').hide();
    // Process data
});
```

### 4. Data Validation
Validate data before sending:
```javascript
function updateOrder(orderId, status) {
    const validStatuses = ['pending', 'completed', 'delivered'];
    if (!validStatuses.includes(status)) {
        alert('Invalid status');
        return;
    }
    // Send request
}
```

### 5. CSRF Protection (Future)
When CSRF protection is implemented:
```javascript
$.ajax({
    url: '/api/endpoint',
    method: 'POST',
    headers: {
        'X-CSRFToken': getCsrfToken()
    },
    data: { ... }
});
```

---

## Pagination (Future Enhancement)

Currently, API endpoints do not support pagination. For large datasets, consider implementing:

```
GET /api/orders?page=1&per_page=20
```

**Response**:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_pages": 5,
    "total_items": 95,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## WebSocket Support (Future Enhancement)

For real-time updates (e.g., new orders, status changes), consider implementing WebSockets:

```javascript
const socket = io('http://localhost:4009');

socket.on('new_order', function(order) {
    console.log('New order received:', order);
    // Update UI
});

socket.on('order_status_changed', function(data) {
    console.log('Order', data.order_id, 'status:', data.status);
    // Update UI
});
```

---

This API reference provides comprehensive documentation for all available endpoints in the Food Management System. For implementation examples and additional details, refer to the main PROJECT_DOCUMENTATION.md file.
