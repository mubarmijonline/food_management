#!/usr/bin/env python3
"""
Test finance report functionality directly
"""
import mysql.connector
from datetime import datetime, timedelta

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'ps',
    'password': 'Aa@123456',
    'database': 'food_management',
    'charset': 'utf8mb4'
}

def test_finance_calculations():
    """Test the finance calculations"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        print("Testing Finance Report Calculations...")
        print("=" * 50)
        
        # Test date range - last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        print(f"Date Range: {start_date} to {end_date}")
        print()
        
        # Get starting balance
        cursor.execute("SELECT setting_value FROM business_settings WHERE setting_key = 'starting_balance'")
        result = cursor.fetchone()
        starting_balance = float(result['setting_value']) if result else 0.0
        print(f"Starting Balance: ${starting_balance:.2f}")
        
        # Get revenue (all orders regardless of status)
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as order_count
            FROM orders 
            WHERE DATE(delivery_date) BETWEEN %s AND %s
        """, (start_date, end_date))
        revenue_data = cursor.fetchone()
        total_revenue = float(revenue_data['total_revenue'])
        order_count = revenue_data['order_count']
        
        print(f"Total Orders: {order_count}")
        print(f"Total Revenue (All Orders): ${total_revenue:.2f}")
        
        # Get completed/delivered revenue separately
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as completed_revenue, COUNT(*) as completed_count
            FROM orders 
            WHERE DATE(delivery_date) BETWEEN %s AND %s 
            AND status IN ('completed', 'delivered')
        """, (start_date, end_date))
        completed_data = cursor.fetchone()
        completed_revenue = float(completed_data['completed_revenue'])
        completed_count = completed_data['completed_count']
        
        print(f"Completed Orders: {completed_count}")
        print(f"Completed Revenue: ${completed_revenue:.2f}")
        
        # Get expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) as total_expenses, COUNT(*) as expense_count
            FROM expenses 
            WHERE expense_date BETWEEN %s AND %s
        """, (start_date, end_date))
        expense_data = cursor.fetchone()
        total_expenses = float(expense_data['total_expenses'])
        expense_count = expense_data['expense_count']
        
        print(f"Total Expenses: {expense_count} items")
        print(f"Total Expense Amount: ${total_expenses:.2f}")
        
        # Calculate profit/loss
        profit_loss = completed_revenue - total_expenses
        print()
        print(f"Profit/Loss: ${profit_loss:.2f}")
        
        # Get daily revenue breakdown
        print()
        print("Daily Revenue Breakdown:")
        print("-" * 30)
        cursor.execute("""
            SELECT DATE(delivery_date) as order_date, 
                   COALESCE(SUM(total_amount), 0) as daily_revenue,
                   COALESCE(SUM(CASE WHEN status IN ('completed', 'delivered') THEN total_amount ELSE 0 END), 0) as completed_revenue,
                   COUNT(*) as order_count
            FROM orders 
            WHERE DATE(delivery_date) BETWEEN %s AND %s
            GROUP BY DATE(delivery_date)
            ORDER BY order_date DESC
        """, (start_date, end_date))
        daily_data = cursor.fetchall()
        
        for day in daily_data:
            print(f"{day['order_date']}: ${float(day['daily_revenue']):.2f} (Completed: ${float(day['completed_revenue']):.2f}) - {day['order_count']} orders")
        
        # Get expense breakdown by category
        print()
        print("Expense Breakdown by Category:")
        print("-" * 35)
        cursor.execute("""
            SELECT ec.name as category_name, COALESCE(SUM(e.amount), 0) as total_amount, COUNT(e.id) as count
            FROM expense_categories ec
            LEFT JOIN expenses e ON ec.id = e.category_id 
                AND e.expense_date BETWEEN %s AND %s
            WHERE ec.is_active = TRUE
            GROUP BY ec.id, ec.name
            HAVING total_amount > 0
            ORDER BY total_amount DESC
        """, (start_date, end_date))
        expense_breakdown = cursor.fetchall()
        
        for category in expense_breakdown:
            print(f"{category['category_name']}: ${float(category['total_amount']):.2f} ({category['count']} items)")
        
        print()
        print("✅ Finance calculations are working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing finance calculations: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    test_finance_calculations()
