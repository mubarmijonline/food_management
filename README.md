# Food Management System

A comprehensive Food & Beverage Point of Sale (POS) Portal built with Flask and MySQL. This system provides complete restaurant management functionality including orders, menu items, expenses, clients, staff management, and financial reporting.

## 🌟 Key Features

- **Order Management**: Create, track, and manage customer orders with real-time status updates
- **Menu Management**: Manage menu items with categories, pricing, and bilingual support (English/Arabic)
- **Financial Tracking**: Track revenue, expenses, and generate detailed financial reports
- **Client Management**: Customer database with order history and analytics
- **User Management**: Multi-user support with role-based access control (Admin/Staff)
- **Refund System**: Process full and partial refunds with approval workflow
- **Notification System**: Internal messaging and alerts for staff
- **WhatsApp Integration**: Send order notifications via WhatsApp API
- **Bilingual Interface**: Full support for English and Arabic languages
- **Financial Reports**: Profit & Loss, Revenue Analysis, Expense Breakdown, and more

## 📚 Documentation

Complete documentation is available in the following files:

- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Comprehensive project overview, features, and workflows
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture, component design, and deployment strategies
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API endpoint documentation with examples

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- MySQL 8.x
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mubarmijonline/food_management.git
cd food_management
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure database**
Edit database settings in `food_management.py` or set environment variables:
```bash
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USER=ps
export MYSQL_PASSWORD=Aa@123456
export MYSQL_DB=food_management
```

4. **Run the application**
```bash
python food_management.py
```

The application will:
- Create the database if it doesn't exist
- Create all required tables
- Seed initial data (admin user, categories)
- Run database migrations
- Start the web server

5. **Access the application**
- HTTP: http://localhost:4009
- HTTPS: https://localhost:4009 (if SSL certificates exist)

### Default Login Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3 (Python web framework)
- **Database**: MySQL 8.x with utf8mb4 character set
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap framework)
- **Authentication**: Session-based with werkzeug password hashing
- **Security**: SSL/TLS support, security headers, input sanitization
- **Deployment**: uWSGI, Nginx (production)

## 📁 Project Structure

```
food_management/
├── food_management.py       # Main application (5500+ lines)
├── wsgi.py                  # WSGI entry point
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
│   ├── base.html           # Base layout
│   ├── dashboard.html      # Main dashboard
│   ├── orders/             # Order templates
│   ├── menu/               # Menu templates
│   ├── finance/            # Finance templates
│   └── ...
├── uploads/                 # File uploads
│   ├── profile/            # User profile pictures
│   ├── docs/               # User documents
│   ├── expenses/           # Expense receipts
│   └── menu/               # Menu images
├── test_data.py            # Sample data generator
└── test_finance.py         # Finance test script
```

## 📊 Database Schema

The system uses 15 MySQL tables:

**Core Tables**:
- `users` - System users (admin/staff)
- `branches` - Restaurant locations
- `menu_categories` - Menu organization
- `menu_items` - Menu with bilingual names
- `clients` - Customer database
- `orders` - Customer orders
- `order_items` - Order line items
- `expenses` - Business expenses
- `expense_categories` - Expense types
- `refunds` - Refund requests
- `notifications` - System notifications

**Supporting Tables**:
- `user_branches` - User-branch assignments
- `price_log` - Price change audit trail
- `business_settings` - System configuration
- `user_documents` - Staff document uploads

## 🔐 Security Features

- Password hashing using werkzeug.security
- SQL injection prevention with parameterized queries
- File upload security (sanitization, extension whitelist)
- Session-based authentication
- Role-based access control
- Security headers (X-Frame-Options, CSP, HSTS, etc.)
- SSL/TLS support
- Input validation and sanitization

## 📱 Main Features

### Order Management
- Create orders with multiple menu items
- Customer search and autocomplete
- Delivery date/time scheduling
- Order status tracking (Pending → Prepared → Delivered)
- Receipt generation and printing
- WhatsApp notifications

### Menu Management
- Add/edit/delete menu items
- Category organization
- Bilingual names (English/Arabic)
- Price change tracking
- Availability toggle
- Image uploads

### Financial Reports
- Profit & Loss Statement
- Revenue Analysis
- Expense Breakdown
- Daily Sales Summary
- Menu Performance
- Monthly Trends
- Tax Summary
- Refund Analysis

### Client Management
- Customer database
- Order history tracking
- Purchase analytics
- Favorite items analysis
- Monthly spending trends
- Client lifetime value

### User Management (Admin)
- Add/edit/delete users
- Role assignment (Admin/Staff)
- Branch assignments
- Profile pictures
- Document uploads
- Bulk actions (activate/deactivate/delete)
- User activity tracking

### Refund System
- Request full or partial refunds
- Approval workflow
- Refund processing
- Order status updates
- Refund analytics

## 🌍 Internationalization

Full bilingual support:
- **English** (default)
- **Arabic** with RTL (right-to-left) layout

Switch languages with a single click. All UI elements, menu items, and reports support both languages.

## 📈 Sample Data

Generate test data for development:

```bash
# Create sample menu items, clients, orders, and expenses
python test_data.py

# Test finance calculations
python test_finance.py
```

## 🚀 Production Deployment

### Using uWSGI

1. **Install uWSGI**
```bash
pip install uwsgi
```

2. **Run with uWSGI**
```bash
uwsgi --ini foodie.ini
```

### Using Nginx (Reverse Proxy)

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
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

### Systemd Service

Create `/etc/systemd/system/food-management.service`:

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
```

## 🔧 Configuration

### Environment Variables

```bash
# Database
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=ps
MYSQL_PASSWORD=Aa@123456
MYSQL_DB=food_management

# Application
SECRET_KEY=your-secret-key-here
UPLOAD_DIR=/path/to/uploads

# WhatsApp API (optional)
WHATSAPP_API_TOKEN=your-token-here
```

### SSL Certificates

For development:
```bash
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365
```

For production (Let's Encrypt):
```bash
certbot certonly --nginx -d your-domain.com
```

## 📝 API Documentation

The system provides RESTful JSON APIs for:
- Menu items listing
- Customer search
- Order details
- User management
- Client analytics

See **[API_REFERENCE.md](API_REFERENCE.md)** for complete API documentation.

## 🧪 Testing

```bash
# Run sample data generation
python test_data.py

# Test finance calculations
python test_finance.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source. Please check the license file for details.

## 👥 Support

For issues, questions, or feature requests, please open an issue in the GitHub repository.

## 🎯 Roadmap

Future enhancements planned:
- [ ] CSRF protection with Flask-WTF
- [ ] API rate limiting
- [ ] Inventory management system
- [ ] Table/seat management
- [ ] Loyalty program
- [ ] Advanced analytics dashboard
- [ ] Multi-tenancy support
- [ ] Mobile app (iOS/Android)
- [ ] Payment gateway integration
- [ ] Reservation system

## 📞 Contact

For more information or support, please contact the repository maintainer.

---

**Built with ❤️ using Flask and MySQL**
