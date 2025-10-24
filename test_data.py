#!/usr/bin/env python3
"""
Create sample data for testing finance reports
"""
import mysql.connector
from datetime import datetime, timedelta
from decimal import Decimal

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'ps',
    'password': 'Aa@123456',
    'database': 'food_management',
    'charset': 'utf8mb4'
}

def create_sample_data():
    """Create sample orders and expenses for testing"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Creating sample data...")
        
        # Check if admin user exists
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        if not admin_user:
            print("Admin user not found. Please run the main application first to initialize the database.")
            return
        
        admin_id = admin_user[0]
        today = datetime.now().date()
        
        # Create sample menu items if they don't exist
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        if cursor.fetchone()[0] == 0:
            print("Creating sample menu items...")
            sample_items = [
                ('Burger', 'Classic beef burger', 15.99, 2),
                ('Pizza', 'Margherita pizza', 18.50, 2),
                ('Salad', 'Caesar salad', 12.00, 5),
                ('Coffee', 'Espresso coffee', 4.50, 4),
                ('Pasta', 'Spaghetti carbonara', 16.75, 2)
            ]
            
            cursor.executemany("""
                INSERT INTO menu_items (name, description, price, category_id)
                VALUES (%s, %s, %s, %s)
            """, sample_items)
            print("Sample menu items created.")
        
        # Create sample clients if they don't exist
        cursor.execute("SELECT COUNT(*) FROM clients")
        if cursor.fetchone()[0] == 0:
            print("Creating sample clients...")
            sample_clients = [
                ('John Doe', '1234567890'),
                ('Jane Smith', '0987654321'),
                ('Bob Johnson', '5555555555'),
                ('Alice Brown', '1111111111')
            ]
            
            cursor.executemany("""
                INSERT INTO clients (name, mobile) VALUES (%s, %s)
            """, sample_clients)
            print("Sample clients created.")
        
        # Create sample orders for the last 7 days
        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] < 10:
            print("Creating sample orders...")
            
            # Get menu items and clients
            cursor.execute("SELECT id, name, price FROM menu_items LIMIT 5")
            menu_items = cursor.fetchall()
            
            cursor.execute("SELECT id, name, mobile FROM clients LIMIT 4")
            clients = cursor.fetchall()
            
            # Create orders for the last 7 days
            for i in range(7):
                order_date = today - timedelta(days=i)
                
                # Create 2-3 orders per day
                for j in range(2 + (i % 2)):
                    client = clients[j % len(clients)]
                    
                    # Calculate order total
                    num_items = 1 + (j % 3)  # 1-3 items per order
                    total_amount = 0
                    order_items = []
                    
                    for k in range(num_items):
                        item = menu_items[k % len(menu_items)]
                        quantity = 1 + (k % 2)  # 1-2 quantity
                        subtotal = float(item[2]) * quantity
                        total_amount += subtotal
                        
                        order_items.append({
                            'menu_item_id': item[0],
                            'menu_item_name': item[1],
                            'quantity': quantity,
                            'unit_price': float(item[2]),
                            'subtotal': subtotal
                        })
                    
                    # Insert order
                    status = 'completed' if i < 5 else 'pending'
                    cursor.execute("""
                        INSERT INTO orders (client_id, client_name, client_mobile, total_amount, 
                                          status, delivery_date, created_by)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (client[0], client[1], client[2], total_amount, status, order_date, admin_id))
                    
                    order_id = cursor.lastrowid
                    
                    # Insert order items
                    for item in order_items:
                        cursor.execute("""
                            INSERT INTO order_items (order_id, menu_item_id, menu_item_name, 
                                                    quantity, unit_price, subtotal)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (order_id, item['menu_item_id'], item['menu_item_name'],
                              item['quantity'], item['unit_price'], item['subtotal']))
            
            print("Sample orders created.")
        
        # Create sample expenses
        cursor.execute("SELECT COUNT(*) FROM expenses")
        if cursor.fetchone()[0] < 5:
            print("Creating sample expenses...")
            
            # Get expense categories
            cursor.execute("SELECT id, name FROM expense_categories LIMIT 5")
            categories = cursor.fetchall()
            
            if categories:
                sample_expenses = [
                    (categories[0][0], 'Food ingredients purchase', 150.00, today - timedelta(days=1)),
                    (categories[1][0], 'Electricity bill', 80.50, today - timedelta(days=2)),
                    (categories[2][0], 'Staff wages', 500.00, today - timedelta(days=3)),
                    (categories[3][0], 'Kitchen equipment maintenance', 120.00, today - timedelta(days=4)),
                    (categories[4][0], 'Marketing materials', 75.00, today - timedelta(days=5))
                ]
                
                cursor.executemany("""
                    INSERT INTO expenses (category_id, description, amount, expense_date, created_by)
                    VALUES (%s, %s, %s, %s, %s)
                """, [(exp[0], exp[1], exp[2], exp[3], admin_id) for exp in sample_expenses])
                
                print("Sample expenses created.")
        
        connection.commit()
        print("\nSample data creation completed successfully!")
        
        # Display summary
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM expenses")
        expense_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status IN ('completed', 'delivered')")
        total_revenue = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
        total_expenses = cursor.fetchone()[0]
        
        print(f"\nData Summary:")
        print(f"Orders: {order_count}")
        print(f"Expenses: {expense_count}")
        print(f"Total Revenue: ${total_revenue}")
        print(f"Total Expenses: ${total_expenses}")
        print(f"Profit/Loss: ${float(total_revenue) - float(total_expenses):.2f}")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    create_sample_data()
