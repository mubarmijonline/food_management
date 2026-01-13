# Food Management System

A comprehensive Food & Beverage POS Portal built with Python Flask and MySQL. This system provides a complete restaurant management solution with order tracking, menu management, expense tracking, and financial reporting.

## Features

- **Dashboard**: Real-time business overview with key metrics
- **Menu Management**: Add, edit, and manage menu items with Arabic/English support
- **Order Management**: Create, track, and fulfill orders
- **Client Management**: Customer database with order history and analytics
- **Expense Tracking**: Track business expenses by category
- **Financial Reports**: Profit/Loss, Revenue Analysis, and more
- **User Management**: Multi-user support with admin and staff roles
- **Notifications**: Internal messaging system
- **Refund Management**: Handle order refunds with approval workflow
- **Bilingual Support**: English and Arabic interface

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or MariaDB 10.3+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/mubarmijonline/food_management.git
cd food_management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (optional)
cp .env.example .env
# Edit .env with your database credentials

# Run the application
python food_management.py
```

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`

Access the application at: `https://localhost:4009`

## API Endpoints

The system provides REST API endpoints that can be consumed by mobile applications:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/menu_items` | GET | Get all available menu items |
| `/api/customers/search` | GET | Search customers by name/mobile |
| `/orders/create` | POST | Create new order |
| `/orders/<id>` | GET | Get order details |

## 📱 Flutter Mobile App Development

Want to build a Flutter mobile app that connects to this backend? Check out our comprehensive guide:

**[Flutter Mobile Development Guide](FLUTTER_MOBILE_DEVELOPMENT_GUIDE.md)**

This guide covers:
- Setting up GCP VM for Flutter development
- Installing Flutter SDK on Linux
- Configuring VS Code with Remote-SSH
- Using GitHub Copilot for AI-assisted coding
- Integrating Claude Opus 4.5 for development help
- Connecting Flutter app to this Flask backend
- Sample Flutter project structure

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL/MariaDB
- **Frontend**: Jinja2 Templates, Bootstrap, JavaScript
- **Security**: HTTPS, Password Hashing, Session Management

## Project Structure

```
food_management/
├── food_management.py    # Main Flask application
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── menu/
│   ├── orders/
│   ├── clients/
│   ├── expenses/
│   ├── finance/
│   ├── users/
│   ├── notifications/
│   └── refunds/
├── uploads/              # File uploads directory
├── requirements.txt      # Python dependencies
├── wsgi.py              # WSGI entry point
└── README.md
```

## Configuration

Environment variables (can be set in `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_HOST` | 127.0.0.1 | MySQL server host |
| `MYSQL_PORT` | 3306 | MySQL server port |
| `MYSQL_USER` | ps | MySQL username |
| `MYSQL_PASSWORD` | Aa@123456 | MySQL password |
| `MYSQL_DB` | food_management | Database name |
| `SECRET_KEY` | (auto-generated) | Flask secret key |

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
