#!/usr/bin/env python3
"""
Food & Beverage POS Portal - Flask Application
Single file implementation with MySQL database
Author: GitHub Copilot
Date: August 20, 2025
"""

import os
import sys
import ssl
import logging
import csv
import io
import re
import requests
from datetime import datetime, timedelta
from decimal import Decimal
import json
import hashlib
import secrets
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, session, jsonify, send_from_directory, make_response
)
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'food-management-secret-key-2025')

# Language translations
LANGUAGES = {
    'en': 'English',
    'ar': 'العربية'
}

TRANSLATIONS = {
    'en': {
        'Food Management System': 'Food Management System',
        'Dashboard': 'Dashboard',
        'Menu Items': 'Menu Items',
        'Orders': 'Orders',
        'Expenses': 'Expenses',
        'Finance': 'Finance',
        'Analytics': 'Analytics',
        'Clients': 'Clients',
        'Users': 'Users',
        'Notifications': 'Notifications',
        'Profile': 'Profile',
        'Settings': 'Settings',
        'Logout': 'Logout',
        'Login': 'Login',
        'Username': 'Username',
        'Password': 'Password',
        'Welcome': 'Welcome',
        'Total Revenue': 'Total Revenue',
        'Total Orders': 'Total Orders',
        'Active Users': 'Active Users',
        'Menu Categories': 'Menu Categories',
        'Create New Order': 'Create New Order',
        'Add Menu Item': 'Add Menu Item',
        'Edit Menu Item': 'Edit Menu Item',
        'Customer Name': 'Customer Name',
        'Mobile Number': 'Mobile Number',
        'Order Total': 'Order Total',
        'Order Status': 'Order Status',
        'Pending': 'Pending',
        'Completed': 'Completed',
        'Prepared': 'Prepared & Ready',
        'Delivered': 'Delivered',
        'Cancel': 'Cancel',
        'Save': 'Save',
        'Delete': 'Delete',
        'Edit': 'Edit',
        'View': 'View',
        'Add': 'Add',
        'Search': 'Search',
        'Filter': 'Filter',
        'Export': 'Export',
        'Print': 'Print',
        'Back': 'Back',
        'Next': 'Next',
        'Previous': 'Previous',
        'Loading': 'Loading',
        'No data available': 'No data available',
        'Are you sure?': 'Are you sure?',
        'Success': 'Success',
        'Error': 'Error',
        'Warning': 'Warning',
        'Info': 'Info',
        'Language changed successfully.': 'Language changed successfully.',
        'Invalid language selection.': 'Invalid language selection.',
        'Order Cart': 'Order Cart',
        'Cart is empty': 'Cart is empty',
        'Click on menu items to add them': 'Click on menu items to add them',
        'Total': 'Total',
        'Clear Cart': 'Clear Cart',
        'Customer Information': 'Customer Information',
        'Search Existing Customer': 'Search Existing Customer',
        'Type customer name or mobile...': 'Type customer name or mobile...',
        'Or fill in details below for new customer': 'Or fill in details below for new customer',
        'Delivery Date': 'Delivery Date',
        'When should this order be delivered/ready': 'When should this order be delivered/ready',
        'Order Notes': 'Order Notes',
        'Special instructions or notes...': 'Special instructions or notes...',
        'Place Order': 'Place Order',
        'Filter by Category': 'Filter by Category',
        'All Categories': 'All Categories',
        'Search Items': 'Search Items',
        'Search menu items (English/Arabic)...': 'Search menu items (English/Arabic)...',
        'Add items to cart and complete the order': 'Add items to cart and complete the order',
        'to Orders': 'to Orders',
        'Added another': 'Added another',
        'to cart': 'to cart',
        'added to cart': 'added to cart',
        'removed from cart': 'removed from cart',
        'Increased': 'Increased',
        'quantity': 'quantity',
        'Decreased': 'Decreased',
        'Are you sure you want to clear the cart?': 'Are you sure you want to clear the cart?',
        'Please enter customer name and mobile number.': 'Please enter customer name and mobile number.',
        'Please select a delivery date.': 'Please select a delivery date.',
        'Please add items to cart before creating order.': 'Please add items to cart before creating order.',
        'Order created successfully!': 'Order created successfully!',
        'Error creating order. Please try again.': 'Error creating order. Please try again.',
        'No customers found': 'No customers found',
        'No items found': 'No items found',
        'Try adjusting your search or filter criteria': 'Try adjusting your search or filter criteria',
        'Added': 'Added',
        'Special instructions (e.g. no pickles)': 'Special instructions (e.g. no pickles)',
        'Special Instructions': 'Special Instructions',
        'without pickles': 'without pickles',
        'no onions': 'no onions',
        'extra sauce': 'extra sauce',
        'Special Request': 'Special Request',
        'Add special instructions for this item...': 'Add special instructions for this item...',
        'Duplicate Order': 'Duplicate Order',
        'Create a new order with the same items?': 'Create a new order with the same items?',
        'Yes, Duplicate': 'Yes, Duplicate',
        'Feature Coming Soon': 'Feature Coming Soon',
        'This feature would create a new order with the same items for quick reordering.': 'This feature would create a new order with the same items for quick reordering.',
        'RECEIPT': 'RECEIPT',
        'Item': 'Item',
        'Qty': 'Qty',
        'Price': 'Price',
        'TOTAL AMOUNT': 'TOTAL AMOUNT',
        'Generated on': 'Generated on',
        'each': 'each',
        "Here's your business overview.": "Here's your business overview.",
        'Orders Today': 'Orders Today',
        'Revenue Today': 'Revenue Today',
        'Pending Orders': 'Pending Orders',
        'Recent Orders': 'Recent Orders',
        'Order ID': 'Order ID',
        'Client': 'Client',
        'Amount': 'Amount',
        'Status': 'Status',
        'Date': 'Date',
        'Action': 'Action',
        'No recent orders found': 'No recent orders found',
        'View All Orders': 'View All Orders',
        'Quick Actions': 'Quick Actions',
        'New Order': 'New Order',
        'Add Expense': 'Add Expense',
        'View Reports': 'View Reports',
        'Send Notification': 'Send Notification',
        'You have': 'You have',
        'unread notification': 'unread notification',
        'View all': 'View all',
        'System Information': 'System Information',
        'User Role': 'User Role',
        'Current Time': 'Current Time',
        "Today's Date": "Today's Date",
        'System Status': 'System Status',
        'Online': 'Online',
        'Manage your restaurant menu items and pricing': 'Manage your restaurant menu items and pricing',
        'Search by name (English/Arabic)...': 'Search by name (English/Arabic)...',
        'Availability': 'Availability',
        'All Items': 'All Items',
        'Available': 'Available',
        'Unavailable': 'Unavailable',
        'Manage customer orders and track order status': 'Manage customer orders and track order status',
        'Order Date': 'Order Date',
        'Today': 'Today',
        'Yesterday': 'Yesterday',
        'All Orders': 'All Orders',
        'Sign in to access your dashboard': 'Sign in to access your dashboard',
        'Sign In': 'Sign In',
        'Default Admin Access': 'Default Admin Access',
        'Create a new menu item for your restaurant': 'Create a new menu item for your restaurant',
        'Back to Menu': 'Back to Menu',
        'Item Information': 'Item Information',
        'Item Name (English)': 'Item Name (English)',
        'e.g., Grilled Chicken Sandwich': 'e.g., Grilled Chicken Sandwich',
        'Item Name (Arabic)': 'Item Name (Arabic)',
        'optional': 'optional',
        'Optional: Add Arabic name for better customer experience': 'Optional: Add Arabic name for better customer experience',
        'Category': 'Category',
        'Order': 'Order',
        'View order details and manage status': 'View order details and manage status',
        'Back to Orders': 'Back to Orders',
        'Order Information': 'Order Information',
        'All orders in the system': 'All orders in the system',
        "Today's orders": "Today's orders",
        'Orders for': 'Orders for',
        'Filter by Status': 'Filter by Status',
        'All Statuses': 'All Statuses',
        'Search Orders': 'Search Orders',
        'Search by client name or mobile...': 'Search by client name or mobile...',
        'Filter by Date': 'Filter by Date',
        'Clear Filters': 'Clear Filters',
        'Client Information': 'Client Information',
        'Total Amount': 'Total Amount',
        'Created By': 'Created By',
        'Actions': 'Actions',
        'No orders found matching your criteria': 'No orders found matching your criteria',
        'No Orders Yet': 'No Orders Yet',
        'Start taking orders to see them here': 'Start taking orders to see them here',
        'Create First Order': 'Create First Order',
        'Update Order Status': 'Update Order Status',
        'Are you sure you want to update the order status?': 'Are you sure you want to update the order status?',
        'Update Status': 'Update Status',
        'Order Details': 'Order Details',
        'Loading...': 'Loading...',
        'Loading order details...': 'Loading order details...',
        'Close': 'Close',
        'Change Status': 'Change Status',
        'Change Order Status': 'Change Order Status',
        'Select New Status': 'Select New Status',
        'Notes (Optional)': 'Notes (Optional)',
        'Add any notes about this status change...': 'Add any notes about this status change...',
        'Status changes will be logged and cannot be undone.': 'Status changes will be logged and cannot be undone.',
        'Mark as Completed': 'Mark as Completed',
        'Mark as Delivered': 'Mark as Delivered',
        'Updating...': 'Updating...',
        'updated successfully': 'updated successfully',
        'Revert': 'Revert',
        'Pending Orders': 'Pending Orders',
        'Completed Orders': 'Completed Orders',
        'Delivered Orders': 'Delivered Orders',
        'Open in New Page': 'Open in New Page',
        'Finance Reports': 'Finance Reports',
        'Generate financial reports and analysis': 'Generate financial reports and analysis',
        'Export Data': 'Export Data',
        'Refunds': 'Refunds',
        'Request Refund': 'Request Refund',
        'Refund Amount': 'Refund Amount',
        'Refund Reason': 'Refund Reason',
        'Refund Status': 'Refund Status',
        'Refund Type': 'Refund Type',
        'Full Refund': 'Full Refund',
        'Partial Refund': 'Partial Refund',
        'Refund Requested': 'Refund Requested',
        'Approve Refund': 'Approve Refund',
        'Reject Refund': 'Reject Refund',
        'Process Refund': 'Process Refund',
        'Refunded': 'Refunded',
        'Partially Refunded': 'Partially Refunded',
        'Refund Rate': 'Refund Rate',
        'Total Refunds': 'Total Refunds',
        'Refund Analysis': 'Refund Analysis',
        'Pending Refunds': 'Pending Refunds',
        'Approved': 'Approved',
        'Rejected': 'Rejected',
        'Processed': 'Processed',
        'Refund successfully requested': 'Refund successfully requested',
        'Refund approved successfully': 'Refund approved successfully',
        'Refund rejected successfully': 'Refund rejected successfully',
        'Refund processed successfully': 'Refund processed successfully',
        'error_occurred': 'An error occurred',
        'order_not_found': 'Order not found',
        'invalid_refund_amount': 'Invalid refund amount',
        'refund_requested': 'Refund requested successfully',
        'refund_approved': 'Refund approved successfully',
        'refund_not_found': 'Refund not found',
        'refund_rejected': 'Refund rejected successfully',
        'refund_processed': 'Refund processed successfully',
        'refund_management': 'Refund Management',
        'refund_requests': 'Refund Requests',
        'refund_id': 'Refund ID',
        'order_number': 'Order Number',
        'customer': 'Customer',
        'request_date': 'Request Date',
        'no_refunds': 'No Refund Requests',
        'no_refunds_message': 'There are no refund requests to display.',
        'refund_details': 'Refund Details',
        'rejection_reason': 'Rejection Reason',
        'approve': 'Approve',
        'reject': 'Reject',
        'process': 'Process',
        'view': 'View',
        'food_management_system': 'Food Management System'
    },
    'ar': {
        'Food Management System': 'نظام إدارة الطعام',
        'Dashboard': 'لوحة التحكم',
        'Menu Items': 'عناصر القائمة',
        'Orders': 'الطلبات',
        'Expenses': 'المصاريف',
        'Finance': 'المالية',
        'Analytics': 'التحليلات',
        'Clients': 'العملاء',
        'Users': 'المستخدمون',
        'Notifications': 'الإشعارات',
        'Profile': 'الملف الشخصي',
        'Settings': 'الإعدادات',
        'Logout': 'تسجيل الخروج',
        'Login': 'تسجيل الدخول',
        'Username': 'اسم المستخدم',
        'Password': 'كلمة المرور',
        'Welcome': 'مرحباً',
        'Total Revenue': 'إجمالي الإيرادات',
        'Total Orders': 'إجمالي الطلبات',
        'Active Users': 'المستخدمون النشطون',
        'Menu Categories': 'فئات القائمة',
        'Create New Order': 'إنشاء طلب جديد',
        'Add Menu Item': 'إضافة عنصر للقائمة',
        'Edit Menu Item': 'تعديل عنصر القائمة',
        'Customer Name': 'اسم العميل',
        'Mobile Number': 'رقم الجوال',
        'Order Total': 'إجمالي الطلب',
        'Order Status': 'حالة الطلب',
        'Pending': 'في الانتظار',
        'Completed': 'مكتمل',
        'Prepared': 'جاهز للتوصيل',
        'Delivered': 'تم التوصيل',
        'Cancel': 'إلغاء',
        'Save': 'حفظ',
        'Delete': 'حذف',
        'Edit': 'تعديل',
        'View': 'عرض',
        'Add': 'إضافة',
        'Search': 'بحث',
        'Filter': 'تصفية',
        'Export': 'تصدير',
        'Print': 'طباعة',
        'Back': 'رجوع',
        'Next': 'التالي',
        'Previous': 'السابق',
        'Loading': 'جارٍ التحميل',
        'No data available': 'لا توجد بيانات متاحة',
        'Are you sure?': 'هل أنت متأكد؟',
        'Success': 'نجح',
        'Error': 'خطأ',
        'Warning': 'تحذير',
        'Info': 'معلومات',
        'Language changed successfully.': 'تم تغيير اللغة بنجاح.',
        'Invalid language selection.': 'اختيار لغة غير صحيح.',
        'Order Cart': 'سلة الطلبات',
        'Cart is empty': 'السلة فارغة',
        'Click on menu items to add them': 'انقر على عناصر القائمة لإضافتها',
        'Total': 'المجموع',
        'Clear Cart': 'مسح السلة',
        'Customer Information': 'معلومات العميل',
        'Search Existing Customer': 'البحث عن عميل موجود',
        'Type customer name or mobile...': 'اكتب اسم العميل أو رقم الجوال...',
        'Or fill in details below for new customer': 'أو املأ التفاصيل أدناه لعميل جديد',
        'Delivery Date': 'تاريخ التوصيل',
        'When should this order be delivered/ready': 'متى يجب توصيل/تجهيز هذا الطلب',
        'Order Notes': 'ملاحظات الطلب',
        'Special instructions or notes...': 'تعليمات خاصة أو ملاحظات...',
        'Place Order': 'تأكيد الطلب',
        'Filter by Category': 'تصفية حسب الفئة',
        'All Categories': 'جميع الفئات',
        'Search Items': 'البحث عن العناصر',
        'Search menu items (English/Arabic)...': 'البحث في عناصر القائمة (الإنجليزية/العربية)...',
        'Add items to cart and complete the order': 'أضف العناصر إلى السلة وأكمل الطلب',
        'to Orders': 'إلى الطلبات',
        'Added another': 'تمت إضافة آخر',
        'to cart': 'إلى السلة',
        'added to cart': 'تمت الإضافة إلى السلة',
        'removed from cart': 'تمت الإزالة من السلة',
        'Increased': 'تمت زيادة',
        'quantity': 'الكمية',
        'Decreased': 'تم تقليل',
        'Are you sure you want to clear the cart?': 'هل أنت متأكد من إفراغ السلة؟',
        'Please enter customer name and mobile number.': 'يرجى إدخال اسم العميل ورقم الجوال.',
        'Please select a delivery date.': 'يرجى اختيار تاريخ التوصيل.',
        'Please add items to cart before creating order.': 'يرجى إضافة عناصر إلى السلة قبل إنشاء الطلب.',
        'Order created successfully!': 'تم إنشاء الطلب بنجاح!',
        'Error creating order. Please try again.': 'خطأ في إنشاء الطلب. يرجى المحاولة مرة أخرى.',
        'No customers found': 'لم يتم العثور على عملاء',
        'No items found': 'لم يتم العثور على عناصر',
        'Try adjusting your search or filter criteria': 'حاول تعديل معايير البحث أو التصفية',
        'Added': 'تمت الإضافة',
        'Special instructions (e.g. no pickles)': 'تعليمات خاصة (مثل بدون مخلل)',
        'Special Instructions': 'تعليمات خاصة',
        'without pickles': 'بدون مخلل',
        'no onions': 'بدون بصل',
        'extra sauce': 'صوص إضافي',
        'Special Request': 'طلب خاص',
        'Add special instructions for this item...': 'أضف تعليمات خاصة لهذا العنصر...',
        'Duplicate Order': 'نسخ الطلب',
        'Create a new order with the same items?': 'إنشاء طلب جديد بنفس العناصر؟',
        'Yes, Duplicate': 'نعم، انسخ',
        'Feature Coming Soon': 'ميزة قادمة قريباً',
        'This feature would create a new order with the same items for quick reordering.': 'ستقوم هذه الميزة بإنشاء طلب جديد بنفس العناصر لإعادة الطلب السريع.',
        'RECEIPT': 'إيصال',
        'Item': 'العنصر',
        'Qty': 'الكمية',
        'Price': 'السعر',
        'TOTAL AMOUNT': 'المبلغ الإجمالي',
        'Generated on': 'تم الإنشاء في',
        'each': 'للواحد',
        "Here's your business overview.": 'إليك نظرة عامة على عملك.',
        'Orders Today': 'طلبات اليوم',
        'Revenue Today': 'إيرادات اليوم',
        'Pending Orders': 'الطلبات المعلقة',
        'Recent Orders': 'الطلبات الأخيرة',
        'Order ID': 'رقم الطلب',
        'Client': 'العميل',
        'Amount': 'المبلغ',
        'Status': 'الحالة',
        'Date': 'التاريخ',
        'Action': 'الإجراء',
        'No recent orders found': 'لم يتم العثور على طلبات حديثة',
        'View All Orders': 'عرض جميع الطلبات',
        'Quick Actions': 'الإجراءات السريعة',
        'New Order': 'طلب جديد',
        'Add Expense': 'إضافة مصروف',
        'View Reports': 'عرض التقارير',
        'Send Notification': 'إرسال إشعار',
        'You have': 'لديك',
        'unread notification': 'إشعار غير مقروء',
        'View all': 'عرض الكل',
        'System Information': 'معلومات النظام',
        'User Role': 'دور المستخدم',
        'Current Time': 'الوقت الحالي',
        "Today's Date": 'تاريخ اليوم',
        'System Status': 'حالة النظام',
        'Online': 'متصل',
        'Manage your restaurant menu items and pricing': 'إدارة عناصر قائمة المطعم والتسعير',
        'Search by name (English/Arabic)...': 'البحث بالاسم (الإنجليزية/العربية)...',
        'Availability': 'التوفر',
        'All Items': 'جميع العناصر',
        'Available': 'متوفر',
        'Unavailable': 'غير متوفر',
        'Manage customer orders and track order status': 'إدارة طلبات العملاء وتتبع حالة الطلب',
        'Order Date': 'تاريخ الطلب',
        'Today': 'اليوم',
        'Yesterday': 'أمس',
        'All Orders': 'جميع الطلبات',
        'Sign in to access your dashboard': 'سجل الدخول للوصول إلى لوحة التحكم',
        'Sign In': 'تسجيل الدخول',
        'Default Admin Access': 'الوصول الافتراضي للمشرف',
        'Create a new menu item for your restaurant': 'إنشاء عنصر جديد في قائمة مطعمك',
        'Back to Menu': 'العودة إلى القائمة',
        'Item Information': 'معلومات العنصر',
        'Item Name (English)': 'اسم العنصر (الإنجليزية)',
        'e.g., Grilled Chicken Sandwich': 'مثال: ساندويش دجاج مشوي',
        'Item Name (Arabic)': 'اسم العنصر (العربية)',
        'optional': 'اختياري',
        'Optional: Add Arabic name for better customer experience': 'اختياري: أضف الاسم العربي لتجربة أفضل للعملاء',
        'Category': 'الفئة',
        'Order': 'الطلب',
        'View order details and manage status': 'عرض تفاصيل الطلب وإدارة الحالة',
        'Back to Orders': 'العودة إلى الطلبات',
        'Order Information': 'معلومات الطلب',
        'All orders in the system': 'جميع الطلبات في النظام',
        "Today's orders": 'طلبات اليوم',
        'Orders for': 'طلبات بتاريخ',
        'Filter by Status': 'تصفية حسب الحالة',
        'All Statuses': 'جميع الحالات',
        'Search Orders': 'البحث في الطلبات',
        'Search by client name or mobile...': 'البحث باسم العميل أو رقم الجوال...',
        'Filter by Date': 'تصفية حسب التاريخ',
        'Clear Filters': 'مسح المرشحات',
        'Client Information': 'معلومات العميل',
        'Total Amount': 'المبلغ الإجمالي',
        'Created By': 'تم الإنشاء بواسطة',
        'Actions': 'الإجراءات',
        'No orders found matching your criteria': 'لم يتم العثور على طلبات تطابق معاييرك',
        'No Orders Yet': 'لا توجد طلبات بعد',
        'Start taking orders to see them here': 'ابدأ في استلام الطلبات لرؤيتها هنا',
        'Create First Order': 'إنشاء أول طلب',
        'Update Order Status': 'تحديث حالة الطلب',
        'Are you sure you want to update the order status?': 'هل أنت متأكد من تحديث حالة الطلب؟',
        'Update Status': 'تحديث الحالة',
        'Order Details': 'تفاصيل الطلب',
        'Loading...': 'جارٍ التحميل...',
        'Loading order details...': 'جارٍ تحميل تفاصيل الطلب...',
        'Close': 'إغلاق',
        'Change Status': 'تغيير الحالة',
        'Change Order Status': 'تغيير حالة الطلب',
        'Select New Status': 'اختر الحالة الجديدة',
        'Notes (Optional)': 'ملاحظات (اختياري)',
        'Add any notes about this status change...': 'أضف أي ملاحظات حول تغيير الحالة هذا...',
        'Status changes will be logged and cannot be undone.': 'سيتم تسجيل تغييرات الحالة ولا يمكن التراجع عنها.',
        'Mark as Completed': 'وضع علامة كمكتمل',
        'Mark as Delivered': 'وضع علامة كمُسلم',
        'Updating...': 'جارٍ التحديث...',
        'updated successfully': 'تم التحديث بنجاح',
        'Revert': 'التراجع',
        'Pending Orders': 'الطلبات المعلقة',
        'Completed Orders': 'الطلبات المكتملة',
        'Delivered Orders': 'الطلبات المُسلمة',
        'Open in New Page': 'فتح في صفحة جديدة',
        'Finance Reports': 'التقارير المالية',
        'Generate financial reports and analysis': 'إنشاء التقارير المالية والتحليل',
        'Export Data': 'تصدير البيانات',
        'Refunds': 'المبالغ المسترجعة',
        'Request Refund': 'طلب استرداد',
        'Refund Amount': 'مبلغ الاسترداد',
        'Refund Reason': 'سبب الاسترداد',
        'Refund Status': 'حالة الاسترداد',
        'Refund Type': 'نوع الاسترداد',
        'Full Refund': 'استرداد كامل',
        'Partial Refund': 'استرداد جزئي',
        'Refund Requested': 'تم طلب الاسترداد',
        'Approve Refund': 'الموافقة على الاسترداد',
        'Reject Refund': 'رفض الاسترداد',
        'Process Refund': 'معالجة الاسترداد',
        'Refunded': 'مسترد',
        'Partially Refunded': 'مسترد جزئياً',
        'Refund Rate': 'معدل الاسترداد',
        'Total Refunds': 'إجمالي المبالغ المستردة',
        'Refund Analysis': 'تحليل الاستردادات',
        'Pending Refunds': 'الاستردادات المعلقة',
        'Approved': 'موافق عليه',
        'Rejected': 'مرفوض',
        'Processed': 'تمت المعالجة',
        'Refund successfully requested': 'تم طلب الاسترداد بنجاح',
        'Refund approved successfully': 'تمت الموافقة على الاسترداد بنجاح',
        'Refund rejected successfully': 'تم رفض الاسترداد بنجاح',
        'Refund processed successfully': 'تمت معالجة الاسترداد بنجاح',
        'error_occurred': 'حدث خطأ',
        'order_not_found': 'الطلب غير موجود',
        'invalid_refund_amount': 'مبلغ الاسترداد غير صحيح',
        'refund_requested': 'تم طلب الاسترداد بنجاح',
        'refund_approved': 'تمت الموافقة على الاسترداد بنجاح',
        'refund_not_found': 'الاسترداد غير موجود',
        'refund_rejected': 'تم رفض الاسترداد بنجاح',
        'refund_processed': 'تمت معالجة الاسترداد بنجاح',
        'refund_management': 'إدارة الاستردادات',
        'refund_requests': 'طلبات الاسترداد',
        'refund_id': 'رقم الاسترداد',
        'order_number': 'رقم الطلب',
        'customer': 'العميل',
        'request_date': 'تاريخ الطلب',
        'no_refunds': 'لا توجد طلبات استرداد',
        'no_refunds_message': 'لا توجد طلبات استرداد للعرض.',
        'refund_details': 'تفاصيل الاسترداد',
        'rejection_reason': 'سبب الرفض',
        'approve': 'موافقة',
        'reject': 'رفض',
        'process': 'معالجة',
        'view': 'عرض',
        'food_management_system': 'نظام إدارة الطعام',
        'Filter by Status': 'تصفية حسب الحالة',
        'All Statuses': 'جميع الحالات',
        'Search Orders': 'البحث في الطلبات',
        'Search by client name or mobile...': 'البحث باسم العميل أو رقم الجوال...',
        'Filter by Date': 'تصفية حسب التاريخ',
        'Clear Filters': 'مسح المرشحات',
        'Client Information': 'معلومات العميل',
        'Total Amount': 'المبلغ الإجمالي',
        'Created By': 'أنشأه',
        'Actions': 'الإجراءات',
        'No orders found matching your criteria': 'لم يتم العثور على طلبات تطابق معاييرك',
        'No Orders Yet': 'لا توجد طلبات بعد',
        'Start taking orders to see them here': 'ابدأ بأخذ الطلبات لرؤيتها هنا',
        'Create First Order': 'إنشاء أول طلب',
        'Update Order Status': 'تحديث حالة الطلب',
        'Are you sure you want to update the order status?': 'هل أنت متأكد من تحديث حالة الطلب؟',
        'Update Status': 'تحديث الحالة',
        'Order Details': 'تفاصيل الطلب',
        'Loading...': 'جاري التحميل...',
        'Loading order details...': 'جاري تحميل تفاصيل الطلب...',
        'Close': 'إغلاق',
        'Change Status': 'تغيير الحالة',
        'Change Order Status': 'تغيير حالة الطلب',
        'Select New Status': 'اختر الحالة الجديدة',
        'Notes (Optional)': 'ملاحظات (اختياري)',
        'Add any notes about this status change...': 'أضف أي ملاحظات حول تغيير الحالة...',
        'Status changes will be logged and cannot be undone.': 'سيتم تسجيل تغييرات الحالة ولا يمكن التراجع عنها.',
        'Mark as Completed': 'تحديد كمكتمل',
        'Mark as Delivered': 'تحديد كمسلم',
        'Updating...': 'جاري التحديث...',
        'updated successfully': 'تم التحديث بنجاح',
        'Revert': 'تراجع',
        'Pending Orders': 'الطلبات المعلقة',
        'Completed Orders': 'الطلبات المكتملة',
        'Delivered Orders': 'الطلبات المسلمة',
        'Yes, clear it!': 'نعم، امسحها!',
        'Cancel': 'إلغاء',
        'Cart cleared!': 'تم مسح السلة!',
        'Missing Information': 'معلومات مفقودة',
        'Missing Delivery Date': 'تاريخ التوصيل مفقود',
        'Empty Cart': 'السلة فارغة',
        'OK': 'موافق',
        'Order Created Successfully!': 'تم إنشاء الطلب بنجاح!',
        'View Orders': 'عرض الطلبات',
        'Print Receipt': 'طباعة الإيصال',
        'Error Creating Order': 'خطأ في إنشاء الطلب',
        'Network Error': 'خطأ في الشبكة',
        'Error': 'خطأ',
        'Order ID not found': 'رقم الطلب غير موجود',
        'Generating Receipt...': 'جاري إنشاء الإيصال...',
        'Unable to fetch order details for receipt': 'غير قادر على جلب تفاصيل الطلب للإيصال',
        'Error generating receipt': 'خطأ في إنشاء الإيصال',
        'Order Receipt': 'إيصال الطلب',
        'RECEIPT': 'الإيصال',
        'Order #': 'طلب رقم',
        'Date': 'التاريخ',
        'Customer': 'العميل',
        'Mobile': 'الجوال',
        'Delivery': 'التوصيل',
        'Notes': 'الملاحظات',
        'Item': 'العنصر',
        'Qty': 'الكمية',
        'Price': 'السعر',
        'Total': 'المجموع',
        'TOTAL AMOUNT': 'المبلغ الإجمالي',
        'Thank you for your order!': 'شكراً لك على طلبك!',
        'Generated on': 'تم الإنشاء في'
    }
}

# Default language
DEFAULT_LANGUAGE = 'en'

def get_current_language():
    """Get the current language from session or default"""
    return session.get('language', DEFAULT_LANGUAGE)

def _(text):
    """Translation function"""
    language = get_current_language()
    return TRANSLATIONS.get(language, {}).get(text, text)

def get_language_direction():
    """Get text direction for current language"""
    return 'rtl' if get_current_language() == 'ar' else 'ltr'

def send_wa_nini_kitchen(mobile, message):
    try:
        # Clean and format mobile number
        mobile = mobile.strip()
        mobile = re.sub(r"\s", "", mobile)
        
        # Remove any + or country code prefixes
        if mobile.startswith('+20'):
            mobile = mobile[3:]
        elif mobile.startswith('20'):
            mobile = mobile[2:]
        elif mobile.startswith('0'):
            mobile = mobile[1:]
        
        # Ensure it's numeric only
        mobile = re.sub(r"[^\d]", "", mobile)
        
        if len(mobile) < 10:
            logger.warning(f'Invalid mobile number length: {mobile}')
            return {'success': False, 'message': 'Check Mobile length!'}

        url = "https://www.wasenderapi.com/api/send-message"
        headers = {
            "Authorization": "Bearer 16b2cc2db9ca5e1e249fe82c038e7353929761a1669b28104b96dd3dfdecdfe6",
            "Content-Type": "application/json"
        }

        data = {
            "to": f"+20{mobile}",
            "text": message
        }

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        
        logger.info(f"WhatsApp API response: {response_data}")
        
        if response.status_code == 200:
            return {'success': True, 'message': 'WhatsApp message sent successfully'}
        else:
            return {'success': False, 'message': f'WhatsApp API error: {response_data}'}
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return {'success': False, 'message': f'Error: {str(e)}'}


def get_translations():
    """Get all translations for current language"""
    language = get_current_language()
    return TRANSLATIONS.get(language, TRANSLATIONS['en'])

# Make translation functions available in templates
@app.context_processor
def inject_i18n():
    return {
        '_': _,
        'current_language': get_current_language(),
        'language_direction': get_language_direction(),
        'available_languages': LANGUAGES
    }

# Context processor to provide user info to templates
@app.context_processor
def inject_user():
    """Inject user information into all templates"""
    return {
        'current_user': {
            'id': session.get('user_id'),
            'username': session.get('username'),
            'role': session.get('role'),
            'name': session.get('name'),
            'full_name': session.get('full_name', session.get('name', ''))
        } if 'user_id' in session else None
    }

# Security headers
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data:; font-src 'self' cdn.jsdelivr.net"
    return response

# Database configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'ps'),
    'password': os.getenv('MYSQL_PASSWORD', 'Aa@123456'),
    'database': os.getenv('MYSQL_DB', 'food_management'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# Upload configuration
UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/development/projects/food_management/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

# Ensure upload directories exist
os.makedirs(os.path.join(UPLOAD_DIR, 'profile'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'docs'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'expenses'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'menu'), exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection and initialization
def get_db_connection():
    """Get database connection with error handling"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        # Connect without database name first
        config = DB_CONFIG.copy()
        db_name = config.pop('database')
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.close()
        connection.close()
        logger.info(f"Database '{db_name}' created or already exists")
        
    except Error as e:
        logger.error(f"Error creating database: {e}")

def create_tables():
    """Create all required tables"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'staff') DEFAULT 'staff',
                national_id VARCHAR(20),
                name VARCHAR(100),
                address TEXT,
                age INT,
                employed_date DATE,
                title VARCHAR(100),
                description TEXT,
                mobile VARCHAR(20),
                profile_picture VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Branches table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS branches (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                location VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User branches (many-to-many)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_branches (
                user_id INT,
                branch_id INT,
                PRIMARY KEY (user_id, branch_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE
            )
        """)
        
        # Menu categories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Menu items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category_id INT,
                image VARCHAR(255),
                is_available BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES menu_categories(id)
            )
        """)
        
        # Price change log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                menu_item_id INT NOT NULL,
                old_price DECIMAL(10, 2),
                new_price DECIMAL(10, 2) NOT NULL,
                changed_by INT NOT NULL,
                change_reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE,
                FOREIGN KEY (changed_by) REFERENCES users(id)
            )
        """)
        
        # Clients
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                email VARCHAR(100),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Orders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                client_name VARCHAR(100) NOT NULL,
                client_mobile VARCHAR(20) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                status ENUM('pending', 'completed', 'prepared', 'delivered', 'refunded', 'partially_refunded') DEFAULT 'pending',
                refund_status ENUM('none', 'requested', 'approved', 'processed') DEFAULT 'none',
                notes TEXT,
                created_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Order items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                menu_item_id INT NOT NULL,
                menu_item_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
            )
        """)
        
        # Expense categories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Expenses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category_id INT,
                description TEXT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                expense_date DATE NOT NULL,
                receipt_document VARCHAR(255),
                created_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES expense_categories(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Business settings (for starting balance)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT NOT NULL,
                updated_by INT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (updated_by) REFERENCES users(id)
            )
        """)
        
        # Notifications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NULL,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # User documents
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                document_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Refunds table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refunds (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                refund_amount DECIMAL(10, 2) NOT NULL,
                refund_type ENUM('full', 'partial') NOT NULL,
                refund_reason TEXT NOT NULL,
                refund_status ENUM('pending', 'approved', 'rejected', 'processed') DEFAULT 'pending',
                requested_by INT NOT NULL,
                approved_by INT NULL,
                processed_by INT NULL,
                request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approval_date TIMESTAMP NULL,
                processed_date TIMESTAMP NULL,
                notes TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (requested_by) REFERENCES users(id),
                FOREIGN KEY (approved_by) REFERENCES users(id),
                FOREIGN KEY (processed_by) REFERENCES users(id)
            )
        """)
        
        connection.commit()
        logger.info("All tables created successfully")
        return True
        
    except Error as e:
        logger.error(f"Error creating tables: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def seed_initial_data():
    """Seed initial data including admin user and default categories"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Check if admin user exists
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if cursor.fetchone():
            logger.info("Admin user already exists")
        else:
            # Create admin user
            admin_password = generate_password_hash('admin123')
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, name, is_active)
                VALUES ('admin', %s, 'admin', 'System Administrator', TRUE)
            """, (admin_password,))
            logger.info("Admin user created: username=admin, password=admin123")
        
        # Insert default branches
        cursor.execute("SELECT COUNT(*) FROM branches")
        if cursor.fetchone()[0] == 0:
            default_branches = [
                ('Main Branch', 'Downtown Location'),
                ('North Branch', 'North Side Location'),
                ('South Branch', 'South Side Location')
            ]
            cursor.executemany("""
                INSERT INTO branches (name, location) VALUES (%s, %s)
            """, default_branches)
            logger.info("Default branches created")
        
        # Insert default menu categories
        cursor.execute("SELECT COUNT(*) FROM menu_categories")
        if cursor.fetchone()[0] == 0:
            default_categories = [
                ('Appetizers', 'Starter dishes and snacks'),
                ('Main Courses', 'Primary dishes'),
                ('Desserts', 'Sweet treats'),
                ('Beverages', 'Drinks and refreshments'),
                ('Salads', 'Fresh salads and healthy options')
            ]
            cursor.executemany("""
                INSERT INTO menu_categories (name, description) VALUES (%s, %s)
            """, default_categories)
            logger.info("Default menu categories created")
        
        # Insert default expense categories
        cursor.execute("SELECT COUNT(*) FROM expense_categories")
        if cursor.fetchone()[0] == 0:
            default_expense_categories = [
                ('Ingredients', 'Food ingredients and supplies'),
                ('Utilities', 'Electricity, water, gas'),
                ('Staff Salaries', 'Employee wages and benefits'),
                ('Equipment', 'Kitchen equipment and maintenance'),
                ('Marketing', 'Advertising and promotional expenses'),
                ('Rent', 'Property rent and lease payments'),
                ('Other', 'Miscellaneous expenses')
            ]
            cursor.executemany("""
                INSERT INTO expense_categories (name, description) VALUES (%s, %s)
            """, default_expense_categories)
            logger.info("Default expense categories created")
        
        # Set default starting balance
        cursor.execute("SELECT COUNT(*) FROM business_settings WHERE setting_key = 'starting_balance'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO business_settings (setting_key, setting_value, updated_by)
                SELECT 'starting_balance', '0.00', id FROM users WHERE username = 'admin' LIMIT 1
            """)
            logger.info("Default starting balance set to 0.00")
        
        connection.commit()
        return True
        
    except Error as e:
        logger.error(f"Error seeding initial data: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def run_migrations():
    """Run database migrations"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Check if delivery_date column exists in orders table
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'orders' 
            AND COLUMN_NAME = 'delivery_date'
        """, (DB_CONFIG['database'],))
        
        if not cursor.fetchone():
            # Add delivery_date column
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN delivery_date DATE NOT NULL DEFAULT (CURDATE())
            """)
            logger.info("Added delivery_date column to orders table")
        
        # Check if email column exists in users table
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'email'
        """, (DB_CONFIG['database'],))
        
        if not cursor.fetchone():
            # Add email column
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN email VARCHAR(100) UNIQUE
            """)
            logger.info("Added email column to users table")
        
        # Check if arabic_name column exists in menu_items table
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'menu_items' 
            AND COLUMN_NAME = 'arabic_name'
        """, (DB_CONFIG['database'],))
        
        if not cursor.fetchone():
            # Add arabic_name column
            cursor.execute("""
                ALTER TABLE menu_items 
                ADD COLUMN arabic_name VARCHAR(100) AFTER name
            """)
            logger.info("Added arabic_name column to menu_items table")
        
        # Check if menu_item_arabic_name column exists in order_items table
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'order_items' 
            AND COLUMN_NAME = 'menu_item_arabic_name'
        """, (DB_CONFIG['database'],))
        
        if not cursor.fetchone():
            # Add menu_item_arabic_name column
            cursor.execute("""
                ALTER TABLE order_items 
                ADD COLUMN menu_item_arabic_name VARCHAR(100) AFTER menu_item_name
            """)
            logger.info("Added menu_item_arabic_name column to order_items table")
        
        # Check if refund_status column exists in orders table
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'orders' 
            AND COLUMN_NAME = 'refund_status'
        """, (DB_CONFIG['database'],))
        
        if not cursor.fetchone():
            # Add refund_status column and update status enum
            cursor.execute("""
                ALTER TABLE orders 
                ADD COLUMN refund_status ENUM('none', 'requested', 'approved', 'processed') DEFAULT 'none'
            """)
            # Update status enum to include refund statuses
            cursor.execute("""
                ALTER TABLE orders 
                MODIFY COLUMN status ENUM('pending', 'completed', 'delivered', 'refunded', 'partially_refunded') DEFAULT 'pending'
            """)
            logger.info("Added refund_status column and updated status enum in orders table")
        
        # Check if refunds table exists
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'refunds'
        """, (DB_CONFIG['database'],))
        
        if not cursor.fetchone():
            # Create refunds table
            cursor.execute("""
                CREATE TABLE refunds (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    refund_amount DECIMAL(10, 2) NOT NULL,
                    refund_type ENUM('full', 'partial') NOT NULL,
                    refund_reason TEXT NOT NULL,
                    refund_status ENUM('pending', 'approved', 'rejected', 'processed') DEFAULT 'pending',
                    requested_by INT NOT NULL,
                    approved_by INT NULL,
                    processed_by INT NULL,
                    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    approval_date TIMESTAMP NULL,
                    processed_date TIMESTAMP NULL,
                    notes TEXT,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (requested_by) REFERENCES users(id),
                    FOREIGN KEY (approved_by) REFERENCES users(id),
                    FOREIGN KEY (processed_by) REFERENCES users(id)
                )
            """)
            logger.info("Created refunds table")
        
        # Migration 8: Update delivery_date to DATETIME for time support
        cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'orders' AND COLUMN_NAME = 'delivery_date'
        """, (DB_CONFIG['database'],))
        
        column_info = cursor.fetchone()
        if column_info and 'date' in column_info[0].lower() and 'datetime' not in column_info[0].lower():
            cursor.execute("""
                ALTER TABLE orders 
                MODIFY COLUMN delivery_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            """)
            logger.info("Updated delivery_date column to DATETIME in orders table")
        
        # Migration 9: Add 'prepared' status to orders table
        cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'orders' AND COLUMN_NAME = 'status'
        """, (DB_CONFIG['database'],))
        
        status_column_info = cursor.fetchone()
        if status_column_info and 'prepared' not in status_column_info[0]:
            cursor.execute("""
                ALTER TABLE orders 
                MODIFY COLUMN status ENUM('pending', 'completed', 'prepared', 'delivered', 'refunded', 'partially_refunded') DEFAULT 'pending'
            """)
            logger.info("Added 'prepared' status to orders table status ENUM")
        
        connection.commit()
        return True
        
    except Error as e:
        logger.error(f"Error running migrations: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# Initialize database on startup
def init_database():
    """Initialize database, tables, and seed data"""
    create_database_if_not_exists()
    if create_tables():
        seed_initial_data()
        run_migrations()  # Add this line
        logger.info("Database initialization completed successfully")
    else:
        logger.error("Database initialization failed")

# Authentication and authorization decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def safe_join(directory, filename):
    """Safely join directory and filename, preventing path traversal"""
    filename = secure_filename(filename)
    if not filename or '..' in filename or filename.startswith('/'):
        return None
    return os.path.join(directory, filename)

def get_user_by_id(user_id):
    """Get user information by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s AND is_active = TRUE", (user_id,))
        return cursor.fetchone()
    except Error as e:
        logger.error(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# Finance report helper functions
def get_report_title(report_type):
    """Get the display title for a report type"""
    titles = {
        'profit_loss': 'Profit & Loss Statement',
        'revenue_analysis': 'Revenue Analysis',
        'expense_breakdown': 'Expense Breakdown',
        'daily_summary': 'Daily Sales Summary',
        'menu_performance': 'Menu Performance',
        'monthly_trends': 'Monthly Trends',
        'tax_summary': 'Tax Summary',
        'refund_analysis': 'Refund Analysis'
    }
    return titles.get(report_type, 'Finance Report')

def get_report_type_display(report_type):
    """Get the short display name for a report type"""
    displays = {
        'profit_loss': 'Profit & Loss',
        'revenue_analysis': 'Revenue',
        'expense_breakdown': 'Expenses',
        'daily_summary': 'Daily Summary',
        'menu_performance': 'Menu Performance',
        'monthly_trends': 'Monthly Trends',
        'tax_summary': 'Tax',
        'refund_analysis': 'Refunds'
    }
    return displays.get(report_type, 'Finance')

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('login.html')
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error. Please try again.', 'danger')
            return render_template('login.html')
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, username, password_hash, role, name 
                FROM users 
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['name'] = user['name']
                session['full_name'] = user['name']  # Add for template compatibility
                
                flash(f'Welcome back, {user["name"] or user["username"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
                
        except Error as e:
            logger.error(f"Login error: {e}")
            flash('Login error. Please try again.', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/set_language/<language>')
def set_language(language):
    """Set the user's language preference"""
    if language in LANGUAGES:
        session['language'] = language
        flash(_('Language changed successfully.'), 'success')
    else:
        flash(_('Invalid language selection.'), 'error')
    
    # Redirect back to the referring page or dashboard
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('dashboard.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get dashboard statistics
        stats = {}
        
        # Total orders for today's delivery
        cursor.execute("""
            SELECT COUNT(*) as count FROM orders 
            WHERE DATE(delivery_date) = CURDATE()
        """)
        stats['orders_today'] = cursor.fetchone()['count']
        
        # Total revenue for today's delivery
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as total FROM orders 
            WHERE DATE(delivery_date) = CURDATE() AND status IN ('completed', 'delivered')
        """)
        stats['revenue_today'] = cursor.fetchone()['total']
        
        # Pending orders for today
        cursor.execute("""
            SELECT COUNT(*) as count FROM orders 
            WHERE DATE(delivery_date) = CURDATE() AND status = 'pending'
        """)
        stats['pending_orders'] = cursor.fetchone()['count']
        
        # Total menu items
        cursor.execute("SELECT COUNT(*) as count FROM menu_items WHERE is_available = TRUE")
        stats['menu_items'] = cursor.fetchone()['count']
        
        # Recent orders (today's deliveries)
        cursor.execute("""
            SELECT o.*, c.name as client_name 
            FROM orders o
            LEFT JOIN clients c ON o.client_id = c.id
            WHERE DATE(o.delivery_date) = CURDATE()
            ORDER BY o.created_at DESC 
            LIMIT 5
        """)
        recent_orders = cursor.fetchall()
        
        # Unread notifications count
        user_id = session['user_id']
        cursor.execute("""
            SELECT COUNT(*) as count FROM notifications 
            WHERE (user_id = %s OR user_id IS NULL) AND is_read = FALSE
        """, (user_id,))
        stats['unread_notifications'] = cursor.fetchone()['count']
        
        return render_template('dashboard.html', stats=stats, recent_orders=recent_orders)
        
    except Error as e:
        logger.error(f"Dashboard error: {e}")
        flash('Error loading dashboard data.', 'danger')
        return render_template('dashboard.html')
    finally:
        cursor.close()
        connection.close()

# Menu management routes
@app.route('/menu')
@login_required
def menu_items():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('menu/list.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get all menu items with categories
        cursor.execute("""
            SELECT mi.*, mc.name as category_name 
            FROM menu_items mi
            LEFT JOIN menu_categories mc ON mi.category_id = mc.id
            ORDER BY mc.name, mi.name
        """)
        menu_items = cursor.fetchall()
        
        # Get categories for filter
        cursor.execute("SELECT * FROM menu_categories WHERE is_active = TRUE ORDER BY name")
        categories = cursor.fetchall()
        
        return render_template('menu/list.html', menu_items=menu_items, categories=categories)
        
    except Error as e:
        logger.error(f"Menu items error: {e}")
        flash('Error loading menu items.', 'danger')
        return render_template('menu/list.html')
    finally:
        cursor.close()
        connection.close()

@app.route('/menu/add', methods=['GET', 'POST'])
@login_required
def add_menu_item():
    if session.get('role') != 'admin':
        flash('Only administrators can add menu items.', 'danger')
        return redirect(url_for('menu_items'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        arabic_name = request.form.get('arabic_name', '').strip()
        description = request.form.get('description', '')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        is_available = request.form.get('is_available', '1') == '1'
        
        if not name or not price:
            flash('Name and price are required.', 'danger')
            return render_template('menu/add.html')
        
        try:
            price = float(price)
            if price < 0:
                flash('Price must be a positive number.', 'danger')
                return render_template('menu/add.html')
        except ValueError:
            flash('Invalid price format.', 'danger')
            return render_template('menu/add.html')
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    # Create secure filename
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    
                    # Save to menu directory
                    menu_dir = os.path.join(UPLOAD_DIR, 'menu')
                    file_path = os.path.join(menu_dir, filename)
                    file.save(file_path)
                    image_filename = f"menu/{filename}"
                else:
                    flash('Invalid file type. Please upload an image file.', 'danger')
                    return render_template('menu/add.html')
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'danger')
            return render_template('menu/add.html')
        
        try:
            cursor = connection.cursor()
            
            # Insert new menu item
            cursor.execute("""
                INSERT INTO menu_items (name, arabic_name, description, price, category_id, is_available, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, arabic_name if arabic_name else None, description, price, category_id if category_id else None, is_available, image_filename))
            
            # Get the ID of the newly created menu item
            menu_item_id = cursor.lastrowid
            
            # Log the initial price as a price change (from NULL to price)
            cursor.execute("""
                INSERT INTO price_log (menu_item_id, old_price, new_price, changed_by, change_reason)
                VALUES (%s, %s, %s, %s, %s)
            """, (menu_item_id, None, price, session['user_id'], 'Initial price setting'))
            
            connection.commit()
            flash('Menu item added successfully!', 'success')
            return redirect(url_for('menu_items'))
            
        except Error as e:
            logger.error(f"Add menu item error: {e}")
            flash('Error adding menu item.', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    # Get categories for dropdown
    connection = get_db_connection()
    categories = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu_categories WHERE is_active = TRUE ORDER BY name")
            categories = cursor.fetchall()
        except Error as e:
            logger.error(f"Get categories error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('menu/add.html', categories=categories)

@app.route('/menu/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_menu_item(item_id):
    if session.get('role') != 'admin':
        flash('Only administrators can edit menu items.', 'danger')
        return redirect(url_for('menu_items'))
    
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('menu_items'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get current menu item
        cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        
        if not item:
            flash('Menu item not found.', 'danger')
            return redirect(url_for('menu_items'))
        
        if request.method == 'POST':
            name = request.form.get('name')
            arabic_name = request.form.get('arabic_name', '').strip()
            description = request.form.get('description', '')
            new_price = request.form.get('price')
            category_id = request.form.get('category_id')
            is_available = request.form.get('is_available', '1') == '1'
            change_reason = request.form.get('change_reason', '')
            
            if not name or not new_price:
                flash('Name and price are required.', 'danger')
                return render_template('menu/edit.html', item=item)
            
            try:
                new_price = float(new_price)
                if new_price < 0:
                    flash('Price must be a positive number.', 'danger')
                    return render_template('menu/edit.html', item=item)
            except ValueError:
                flash('Invalid price format.', 'danger')
                return render_template('menu/edit.html', item=item)
            
            old_price = float(item['price'])
            
            # Handle image upload
            image_filename = item['image']  # Keep existing image by default
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    if allowed_file(file.filename):
                        # Create secure filename
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        
                        # Save to menu directory
                        menu_dir = os.path.join(UPLOAD_DIR, 'menu')
                        file_path = os.path.join(menu_dir, filename)
                        file.save(file_path)
                        image_filename = f"menu/{filename}"
                    else:
                        flash('Invalid file type. Please upload an image file.', 'danger')
                        return render_template('menu/edit.html', item=item)
            
            # Update menu item
            cursor.execute("""
                UPDATE menu_items 
                SET name = %s, arabic_name = %s, description = %s, price = %s, category_id = %s, is_available = %s, image = %s, updated_at = NOW()
                WHERE id = %s
            """, (name, arabic_name if arabic_name else None, description, new_price, category_id if category_id else None, is_available, image_filename, item_id))
            
            # Log price change if price changed
            if old_price != new_price:
                cursor.execute("""
                    INSERT INTO price_log (menu_item_id, old_price, new_price, changed_by, change_reason)
                    VALUES (%s, %s, %s, %s, %s)
                """, (item_id, old_price, new_price, session['user_id'], change_reason))
            
            connection.commit()
            flash('Menu item updated successfully!', 'success')
            return redirect(url_for('menu_items'))
        
        # Get categories for dropdown
        cursor.execute("SELECT * FROM menu_categories WHERE is_active = TRUE ORDER BY name")
        categories = cursor.fetchall()
        
        # Get price history for this item
        cursor.execute("""
            SELECT 
                pl.old_price,
                pl.new_price,
                pl.change_reason,
                pl.created_at,
                u.username as changed_by_username
            FROM price_log pl
            LEFT JOIN users u ON pl.changed_by = u.id
            WHERE pl.menu_item_id = %s
            ORDER BY pl.created_at DESC
            LIMIT 10
        """, (item_id,))
        price_history = cursor.fetchall()
        
        return render_template('menu/edit.html', item=item, categories=categories, price_history=price_history)
        
    except Error as e:
        logger.error(f"Edit menu item error: {e}")
        flash('Error updating menu item.', 'danger')
        return redirect(url_for('menu_items'))
    finally:
        cursor.close()
        connection.close()

# Orders management routes
@app.route('/orders')
@login_required
def orders():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('orders/list.html', 
                             orders=[], 
                             selected_date=today, 
                             today=today,
                             menu_items=[],
                             categories=[])
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get delivery date filter from query params
        delivery_date = request.args.get('delivery_date', '')
        show_all = request.args.get('show_all', '')
        
        # Build query based on filter
        if show_all == 'true':
            # Show all orders
            query = """
                SELECT o.*, u.name as created_by_name 
                FROM orders o
                LEFT JOIN users u ON o.created_by = u.id
                ORDER BY 
                    CASE WHEN o.status = 'pending' THEN 0 ELSE 1 END,
                    o.delivery_date ASC,
                    o.created_at DESC
            """
            cursor.execute(query)
            selected_date = 'all'
        elif delivery_date:
            try:
                # Validate date format
                datetime.strptime(delivery_date, '%Y-%m-%d')
                query = """
                    SELECT o.*, u.name as created_by_name 
                    FROM orders o
                    LEFT JOIN users u ON o.created_by = u.id
                    WHERE DATE(o.delivery_date) = %s
                    ORDER BY 
                        CASE WHEN o.status = 'pending' THEN 0 ELSE 1 END,
                        o.delivery_date ASC,
                        o.created_at DESC
                """
                cursor.execute(query, (delivery_date,))
                selected_date = delivery_date
            except ValueError:
                # Invalid date format, show today's orders
                cursor.execute("""
                    SELECT o.*, u.name as created_by_name 
                    FROM orders o
                    LEFT JOIN users u ON o.created_by = u.id
                    WHERE DATE(o.delivery_date) = CURDATE()
                    ORDER BY 
                        CASE WHEN o.status = 'pending' THEN 0 ELSE 1 END,
                        o.delivery_date ASC,
                        o.created_at DESC
                """)
                selected_date = datetime.now().strftime('%Y-%m-%d')
        else:
            # No filter, show today's orders by default
            cursor.execute("""
                SELECT o.*, u.name as created_by_name 
                FROM orders o
                LEFT JOIN users u ON o.created_by = u.id
                WHERE DATE(o.delivery_date) = CURDATE()
                ORDER BY 
                    CASE WHEN o.status = 'pending' THEN 0 ELSE 1 END,
                    o.delivery_date ASC,
                    o.created_at DESC
            """)
            selected_date = datetime.now().strftime('%Y-%m-%d')
        
        orders = cursor.fetchall()
        
        # Get menu items and categories for the POS modal
        cursor.execute("""
            SELECT mi.*, mc.name as category_name 
            FROM menu_items mi
            LEFT JOIN menu_categories mc ON mi.category_id = mc.id
            WHERE mi.is_available = TRUE
            ORDER BY mc.name, mi.name
        """)
        menu_items = cursor.fetchall()
        
        cursor.execute("SELECT * FROM menu_categories WHERE is_active = TRUE ORDER BY name")
        categories = cursor.fetchall()
        
        # Get today's date for template comparison
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if this is an AJAX reload request
        if request.args.get('ajax_reload') == '1':
            # Return only the updated data as JSON for AJAX requests
            return jsonify({
                'success': True,
                'orders': orders,
                'selected_date': selected_date,
                'today': today,
                'menu_items': menu_items,
                'categories': categories
            })
        
        return render_template('orders/list.html', 
                             orders=orders, 
                             selected_date=selected_date, 
                             today=today,
                             menu_items=menu_items,
                             categories=categories)
        
    except Error as e:
        logger.error(f"Orders error: {e}")
        
        # Handle AJAX requests differently
        if request.args.get('ajax_reload') == '1':
            return jsonify({'success': False, 'message': 'Error loading orders'})
        
        flash('Error loading orders.', 'danger')
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('orders/list.html', 
                             orders=[], 
                             selected_date=today, 
                             today=today,
                             menu_items=[],
                             categories=[])
    finally:
        cursor.close()
        connection.close()

@app.route('/orders/create', methods=['GET', 'POST'])
@login_required
def create_order():
    if request.method == 'GET':
        # Redirect to orders page with modal parameter
        return redirect(url_for('orders', open_pos=1))
    
    if request.method == 'POST':
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            client_name = data.get('client_name')
            client_mobile = data.get('client_mobile')
            delivery_date = data.get('delivery_date')
            notes = data.get('notes', '')
            cart_items = data.get('cart_items')  # Already a list/dict
        else:
            client_name = request.form.get('client_name')
            client_mobile = request.form.get('client_mobile')
            delivery_date = request.form.get('delivery_date')
            customer_id = request.form.get('customer_id')
            notes = request.form.get('notes', '')
            cart_items = request.form.get('cart_items')  # JSON string
            
            # Parse JSON string for form data
            try:
                cart_items = json.loads(cart_items) if cart_items else None
            except json.JSONDecodeError:
                return jsonify({'success': False, 'message': 'Invalid cart data.'})
        
        if not client_name or not client_mobile or not delivery_date or not cart_items:
            return jsonify({'success': False, 'message': 'Client name, mobile, delivery date, and cart items are required.'})
        
        if not cart_items:
            return jsonify({'success': False, 'message': 'Cart cannot be empty.'})
        
        # Validate delivery date and time
        try:
            # Handle both date and datetime formats
            if 'T' in delivery_date:
                # datetime-local format: YYYY-MM-DDTHH:MM
                delivery_datetime_obj = datetime.strptime(delivery_date, '%Y-%m-%dT%H:%M')
            else:
                # date format: YYYY-MM-DD (set default time to 12:00)
                delivery_datetime_obj = datetime.strptime(delivery_date + 'T12:00', '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid delivery date/time format.'})
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection error.'})
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Check if client exists, if not create one
            cursor.execute("SELECT id FROM clients WHERE mobile = %s", (client_mobile,))
            client = cursor.fetchone()
            
            if not client:
                cursor.execute("""
                    INSERT INTO clients (name, mobile) VALUES (%s, %s)
                """, (client_name, client_mobile))
                client_id = cursor.lastrowid
            else:
                client_id = client['id']
                # Update client name if different
                cursor.execute("""
                    UPDATE clients SET name = %s WHERE id = %s
                """, (client_name, client_id))
            
            # Calculate total amount
            total_amount = 0
            valid_items = []
            
            for item in cart_items:
                item_id = item.get('id')
                quantity = int(item.get('quantity', 0))
                special_request = item.get('special_request', '')
                cooking_preference = item.get('cooking_preference', 'مستوي')  # Default to well-done
                
                if quantity <= 0:
                    continue
                
                # Get current price and names from database
                cursor.execute("SELECT name, arabic_name, price FROM menu_items WHERE id = %s AND is_available = TRUE", (item_id,))
                menu_item = cursor.fetchone()
                
                if menu_item:
                    unit_price = float(menu_item['price'])
                    subtotal = unit_price * quantity
                    total_amount += subtotal
                    
                    valid_items.append({
                        'id': item_id,
                        'name': menu_item['name'],
                        'arabic_name': menu_item['arabic_name'],
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'subtotal': subtotal,
                        'special_request': special_request,
                        'cooking_preference': cooking_preference
                    })
            
            if not valid_items:
                return jsonify({'success': False, 'message': 'No valid items in cart.'})
            
            # Create order
            cursor.execute("""
                INSERT INTO orders (client_id, client_name, client_mobile, total_amount, delivery_date, notes, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (client_id, client_name, client_mobile, total_amount, delivery_datetime_obj, notes, session['user_id']))
            
            order_id = cursor.lastrowid
            
            # Add order items
            for item in valid_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, menu_item_id, menu_item_name, menu_item_arabic_name, quantity, unit_price, subtotal, special_request, cooking_preference)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (order_id, item['id'], item['name'], item['arabic_name'], item['quantity'], item['unit_price'], item['subtotal'], item['special_request'], item['cooking_preference']))
            
            connection.commit()
            
            # Send WhatsApp notification to customer
            try:
                # Build order details in Arabic with English item details
                order_details = f"""
شكراً لطلبك من Nini's Kitchen 

تفاصيل طلبك #{order_id}:
"""
                
                for item in valid_items:
                    item_name = item['name']
                    if item['arabic_name']:
                        item_name = f"{item['arabic_name']} ({item['name']})"
                    
                    order_details += f"• {item['quantity']} X {item_name}"
                    
                    # Add cooking preference
                    cooking_pref = item.get('cooking_preference', 'مستوي')
                    order_details += f" - {cooking_pref}"
                    
                    if item['special_request']:
                        order_details += f" - {item['special_request']}"
                    order_details += f" - {item['subtotal']:.2f} EGP\n"
                
                # Format delivery date with English day name and date
                delivery_formatted = delivery_datetime_obj.strftime('%A %d %B %I:%M %p')
                
                order_details += f"""
📅 معاد الاستلام: {delivery_formatted}
💰 المبلغ الإجمالي: {total_amount:.2f} EGP

شكراً لثقتكم بنا! ✨

Powered by MubarmiJ 🚀"""
                
                # Send WhatsApp message
                send_wa_nini_kitchen(client_mobile, order_details)
                
            except Exception as e:
                logger.warning(f"Failed to send WhatsApp notification: {e}")
                # Don't fail the order creation if WhatsApp fails
            
            return jsonify({'success': True, 'message': 'Order created successfully!', 'order_id': order_id})
            
        except Error as e:
            logger.error(f"Create order error: {e}")
            return jsonify({'success': False, 'message': 'Error creating order.'})
        finally:
            cursor.close()
            connection.close()
    
    # Get menu items for cart
    connection = get_db_connection()
    menu_items = []
    categories = []
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT mi.*, mc.name as category_name 
                FROM menu_items mi
                LEFT JOIN menu_categories mc ON mi.category_id = mc.id
                WHERE mi.is_available = TRUE
                ORDER BY mc.name, mi.name
            """)
            menu_items = cursor.fetchall()
            
            cursor.execute("SELECT * FROM menu_categories WHERE is_active = TRUE ORDER BY name")
            categories = cursor.fetchall()
            
        except Error as e:
            logger.error(f"Get menu items error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('orders/create.html', menu_items=menu_items, categories=categories)

@app.route('/orders/view/<int:order_id>')
@login_required
def view_order(order_id):
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('orders'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT o.*, u.name as created_by_name 
            FROM orders o
            LEFT JOIN users u ON o.created_by = u.id
            WHERE o.id = %s
        """, (order_id,))
        
        order = cursor.fetchone()
        if not order:
            flash('Order not found.', 'danger')
            return redirect(url_for('orders'))
        
        # Get order items
        cursor.execute("""
            SELECT oi.*, mi.description as menu_item_description, mi.arabic_name as menu_item_arabic_name_current
            FROM order_items oi
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        order_items = cursor.fetchall()
        
        return render_template('orders/view.html', order=order, order_items=order_items)
        
    except Error as e:
        logger.error(f"View order error: {e}")
        flash('Error loading order details.', 'danger')
        return redirect(url_for('orders'))
    finally:
        cursor.close()
        connection.close()

@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('orders'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT o.*, u.name as created_by_name 
            FROM orders o
            LEFT JOIN users u ON o.created_by = u.id
            WHERE o.id = %s
        """, (order_id,))
        
        order = cursor.fetchone()
        if not order:
            flash('Order not found.', 'danger')
            return redirect(url_for('orders'))
        
        # Check if order can be edited (only pending orders)
        if order['status'] != 'pending':
            flash('Only pending orders can be edited.', 'warning')
            return redirect(url_for('view_order', order_id=order_id))
        
        if request.method == 'GET':
            # Get order items for editing
            cursor.execute("""
                SELECT oi.*, mi.description as menu_item_description, mi.arabic_name as menu_item_arabic_name,
                       mi.price as current_price, mi.category_id, c.name as category_name
                FROM order_items oi
                LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                LEFT JOIN menu_categories c ON mi.category_id = c.id
                WHERE oi.order_id = %s
            """, (order_id,))
            
            order_items = cursor.fetchall()
            
            # Get all menu items for adding new items
            cursor.execute("""
                SELECT mi.*, c.name as category_name 
                FROM menu_items mi
                LEFT JOIN menu_categories c ON mi.category_id = c.id
                WHERE mi.is_available = TRUE
                ORDER BY c.name, mi.name
            """)
            menu_items = cursor.fetchall()
            
            # Get categories for filtering
            cursor.execute("SELECT * FROM menu_categories WHERE is_active = TRUE ORDER BY name")
            categories = cursor.fetchall()
            
            return render_template('orders/edit.html', 
                                 order=order, 
                                 order_items=order_items, 
                                 menu_items=menu_items, 
                                 categories=categories)
        
        elif request.method == 'POST':
            # Handle order update
            if request.is_json:
                data = request.get_json()
                client_name = data.get('client_name')
                client_mobile = data.get('client_mobile')
                delivery_date = data.get('delivery_date')
                notes = data.get('notes', '')
                cart_items = data.get('cart_items')  # Already a list/dict
                customer_id = data.get('customer_id')
            else:
                client_name = request.form.get('client_name')
                client_mobile = request.form.get('client_mobile')
                delivery_date = request.form.get('delivery_date')
                customer_id = request.form.get('customer_id')
                notes = request.form.get('notes', '')
                cart_items_str = request.form.get('cart_items')
                cart_items = json.loads(cart_items_str) if cart_items_str else []

            # Validate input
            if not client_name or not client_mobile or not cart_items:
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Missing required fields'}), 400
                else:
                    flash('Missing required fields.', 'danger')
                    return redirect(url_for('edit_order', order_id=order_id))

            # Calculate new total
            total_amount = 0
            processed_items = []
            
            for item in cart_items:
                item_id = item.get('id')
                quantity = int(item.get('quantity', 1))
                special_request = item.get('special_request', '')
                cooking_preference = item.get('cooking_preference', 'مستوي')  # Default to well-done
                
                # Get current menu item details
                cursor.execute("SELECT name, arabic_name, price FROM menu_items WHERE id = %s", (item_id,))
                menu_item = cursor.fetchone()
                
                if menu_item:
                    unit_price = float(menu_item['price'])
                    subtotal = quantity * unit_price
                    total_amount += subtotal
                    
                    processed_items.append({
                        'id': item_id,
                        'name': menu_item['name'],
                        'arabic_name': menu_item['arabic_name'],
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'subtotal': subtotal,
                        'special_request': special_request,
                        'cooking_preference': cooking_preference
                    })

            # Update order
            cursor.execute("""
                UPDATE orders 
                SET client_name = %s, client_mobile = %s, delivery_date = %s, notes = %s,
                    total_amount = %s, client_id = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (client_name, client_mobile, delivery_date, notes, total_amount, customer_id, order_id))
            
            # Log the order modification for audit trail
            old_total = order['total_amount']
            if old_total != total_amount:
                logger.info(f"Order #{order_id} total amount changed from ${old_total:.2f} to ${total_amount:.2f} by user {session.get('user_id')}")
            
            # Delete existing order items
            cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
            
            # Insert new order items
            for item in processed_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, menu_item_id, menu_item_name, menu_item_arabic_name, 
                                           quantity, unit_price, subtotal, special_request, cooking_preference)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (order_id, item['id'], item['name'], item['arabic_name'], 
                      item['quantity'], item['unit_price'], item['subtotal'], item['special_request'], item['cooking_preference']))
            
            connection.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Order updated successfully!', 'order_id': order_id})
            else:
                flash('Order updated successfully!', 'success')
                return redirect(url_for('view_order', order_id=order_id))
        
    except Error as e:
        connection.rollback()
        logger.error(f"Edit order error: {e}")
        if request.is_json:
            return jsonify({'success': False, 'message': 'Database error occurred'}), 500
        else:
            flash('Database error occurred.', 'danger')
            return redirect(url_for('view_order', order_id=order_id))
    finally:
        cursor.close()
        connection.close()

@app.route('/orders/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        new_status = data.get('status')
        old_status = data.get('old_status')
        notes = data.get('notes')
    else:
        new_status = request.form.get('status')
        old_status = request.form.get('old_status')
        notes = request.form.get('notes')
    
    if new_status not in ['pending', 'completed', 'prepared', 'delivered', 'refunded', 'partially_refunded']:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid status.'})
        flash('Invalid status.', 'danger')
        return redirect(url_for('view_order', order_id=order_id))
    
    connection = get_db_connection()
    if not connection:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Database connection error.'})
        flash('Database connection error.', 'danger')
        return redirect(url_for('view_order', order_id=order_id))
    
    try:
        cursor = connection.cursor()
        
        # Get current status before update for revert functionality
        cursor.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
        current_order = cursor.fetchone()
        if not current_order:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Order not found.'})
            flash('Order not found.', 'danger')
            return redirect(url_for('orders'))
        
        current_status = current_order[0]
        
        
        cursor.execute("""
            UPDATE orders SET status = %s, updated_at = NOW() WHERE id = %s
        """, (new_status, order_id))
        
        connection.commit()
        
        # Return JSON response for AJAX requests
        if request.is_json:
            return jsonify({
                'success': True, 
                'message': f'Order status updated to {new_status}.',
                'new_status': new_status,
                'old_status': current_status,
                'order_id': order_id
            })
        
        flash(f'Order status updated to {new_status}.', 'success')
        
    except Error as e:
        logger.error(f"Update order status error: {e}")
        if request.is_json:
            return jsonify({'success': False, 'message': 'Error updating order status.'})
        flash('Error updating order status.', 'danger')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('view_order', order_id=order_id))

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    """Delete an entire order (only if in pending, prepared, or ready status)"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error.'})
    
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Check if order exists and is in deletable status
        cursor.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        
        if not order:
            return jsonify({'success': False, 'message': 'Order not found.'})
        
        order_status = order[0]
        if order_status not in ['pending', 'prepared', 'ready']:
            return jsonify({'success': False, 'message': 'Only pending, prepared, or ready orders can be deleted.'})
        
        # Disable autocommit to handle transaction manually
        connection.autocommit = False
        
        # Delete order items first (foreign key constraint)
        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
        
        # Delete the order
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        
        # Commit the transaction
        connection.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Order #{order_id} has been deleted successfully.'
        })
        
    except Error as e:
        # Rollback transaction on error
        if connection:
            connection.rollback()
        logger.error(f"Delete order error: {e}")
        return jsonify({'success': False, 'message': 'Error deleting order.'})
    finally:
        if cursor:
            cursor.close()
        if connection:
            # Re-enable autocommit before closing
            connection.autocommit = True
            connection.close()

@app.route('/api/order/<int:order_id>')
@login_required
def api_order_details(order_id):
    """API endpoint to get order details for modal display"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT o.*, u.name as created_by_name 
            FROM orders o
            LEFT JOIN users u ON o.created_by = u.id
            WHERE o.id = %s
        """, (order_id,))
        
        order = cursor.fetchone()
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        # Get order items
        cursor.execute("""
            SELECT oi.*, oi.unit_price as price, mi.description as menu_item_description,
                   CASE 
                       WHEN oi.special_request LIKE '%[PREPARED]%' THEN 1
                       ELSE 0
                   END as prepared
            FROM order_items oi
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        order_items = cursor.fetchall()
        
        # Convert decimal/datetime objects to JSON serializable formats
        if order['total_amount']:
            order['total_amount'] = float(order['total_amount'])
        if order['created_at']:
            order['created_at'] = order['created_at'].isoformat()
        if order['delivery_date']:
            order['delivery_date'] = order['delivery_date'].isoformat()
        
        for item in order_items:
            if item['unit_price']:
                item['price'] = float(item['unit_price'])  # Convert unit_price to price for frontend
            if item['subtotal']:
                item['subtotal'] = float(item['subtotal'])
        
        return jsonify({
            'success': True, 
            'order': order, 
            'order_items': order_items
        })
        
    except Error as e:
        logger.error(f"API order details error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/api/order/<int:order_id>/mark-all-prepared', methods=['POST'])
@login_required
def api_mark_all_prepared(order_id):
    """API endpoint to mark all items in an order as prepared"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        
        # Check if order exists and is not already completed/delivered
        cursor.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        if order[0] in ['completed', 'delivered']:
            return jsonify({'success': False, 'message': 'Cannot modify completed or delivered orders'})
        
        # Update all order items to add [PREPARED] marker if not already present
        cursor.execute("""
            UPDATE order_items 
            SET special_request = CASE 
                WHEN special_request IS NULL OR special_request = '' THEN '[PREPARED]'
                WHEN special_request NOT LIKE '%[PREPARED]%' THEN CONCAT(special_request, ' [PREPARED]')
                ELSE special_request
            END
            WHERE order_id = %s
        """, (order_id,))
        
        # Check if all items are now prepared and update order status accordingly
        cursor.execute("""
            SELECT COUNT(*) as total_items,
                   SUM(CASE WHEN special_request LIKE '%[PREPARED]%' THEN 1 ELSE 0 END) as prepared_items
            FROM order_items 
            WHERE order_id = %s
        """, (order_id,))
        
        result = cursor.fetchone()
        if result and result[0] == result[1]:  # All items are prepared
            cursor.execute("UPDATE orders SET status = 'prepared' WHERE id = %s", (order_id,))
        
        connection.commit()
        
        return jsonify({
            'success': True, 
            'message': 'All items marked as prepared successfully',
            'order_status': 'prepared' if result and result[0] == result[1] else 'pending'
        })
        
    except Error as e:
        logger.error(f"API mark all prepared error: {e}")
        connection.rollback()
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/preparation')
@login_required
def preparation():
    """Kitchen preparation page - aggregates all order items by delivery date"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('preparation/index.html', preparation_items=[], selected_date='today', today=datetime.now().strftime('%Y-%m-%d'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get delivery date filter from query params
        delivery_date = request.args.get('delivery_date', '')
        
        # Build query based on filter
        if delivery_date == 'tomorrow':
            # Tomorrow's orders
            target_date = datetime.now() + timedelta(days=1)
            date_filter = target_date.strftime('%Y-%m-%d')
            selected_date = 'tomorrow'
        elif delivery_date and delivery_date != 'today':
            try:
                # Validate custom date format
                datetime.strptime(delivery_date, '%Y-%m-%d')
                date_filter = delivery_date
                selected_date = delivery_date
            except ValueError:
                # Invalid date format, show today's orders
                date_filter = datetime.now().strftime('%Y-%m-%d')
                selected_date = 'today'
        else:
            # Today's orders (default)
            date_filter = datetime.now().strftime('%Y-%m-%d')
            selected_date = 'today'
        
        # Get individual order items for the selected date
        cursor.execute("""
            SELECT 
                oi.id as order_item_id,
                oi.menu_item_name,
                oi.menu_item_arabic_name,
                oi.quantity,
                oi.special_request,
                o.id as order_id,
                o.client_name,
                o.status as order_status,
                CASE 
                    WHEN oi.special_request LIKE '%[PREPARED]%' THEN 'prepared'
                    ELSE 'pending'
                END as preparation_status
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE DATE(o.delivery_date) = %s
            AND o.status IN ('pending', 'completed', 'prepared', 'ready')
            ORDER BY oi.menu_item_name, o.id
        """, (date_filter,))
        
        order_items = cursor.fetchall()
        
        # Group items by menu item name for display
        preparation_items = {}
        for item in order_items:
            menu_name = item['menu_item_name']
            if menu_name not in preparation_items:
                preparation_items[menu_name] = {
                    'menu_item_name': item['menu_item_name'],
                    'menu_item_arabic_name': item['menu_item_arabic_name'],
                    'order_items': []
                }
            
            # Clean special request
            special_request = item['special_request'] or ''
            special_request = special_request.replace('[PREPARED]', '').strip()
            if not special_request or special_request.lower() in ['none', 'null']:
                special_request = None
            
            preparation_items[menu_name]['order_items'].append({
                'order_item_id': item['order_item_id'],
                'order_id': item['order_id'],
                'client_name': item['client_name'],
                'quantity': item['quantity'],
                'special_request': special_request,
                'preparation_status': item['preparation_status'],
                'order_status': item['order_status']
            })
        
        # Convert to list for template
        preparation_items = list(preparation_items.values())
        
        # Get today's date for template comparison
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check if this is an AJAX reload request
        if request.args.get('ajax_reload') == '1':
            # Return only the updated data as JSON for AJAX requests
            return jsonify({
                'success': True,
                'preparation_items': preparation_items,
                'selected_date': selected_date,
                'today': today,
                'tomorrow': tomorrow,
                'date_filter': date_filter
            })
        
        return render_template('preparation/index.html', 
                             preparation_items=preparation_items, 
                             selected_date=selected_date,
                             today=today,
                             tomorrow=tomorrow,
                             date_filter=date_filter)
        
    except Error as e:
        logger.error(f"Preparation error: {e}")
        
        # Handle AJAX requests differently
        if request.args.get('ajax_reload') == '1':
            return jsonify({'success': False, 'message': 'Error loading preparation data'})
        
        flash('Error loading preparation data.', 'danger')
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('preparation/index.html', 
                             preparation_items=[], 
                             selected_date='today', 
                             today=today)
    finally:
        cursor.close()
        connection.close()

@app.route('/preparation/mark_prepared', methods=['POST'])
@login_required
def mark_item_prepared():
    """Mark a specific order item as prepared and update order status if all items are ready"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        data = request.get_json()
        order_item_id = data.get('order_item_id')
        
        if not order_item_id:
            return jsonify({'success': False, 'message': 'Missing order item ID'})
        
        cursor = connection.cursor(dictionary=True)
        
        # Get order item details
        cursor.execute("""
            SELECT oi.*, o.id as order_id
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE oi.id = %s
        """, (order_item_id,))
        
        order_item = cursor.fetchone()
        if not order_item:
            return jsonify({'success': False, 'message': 'Order item not found'})
        
        order_id = order_item['order_id']
        
        # Mark the specific order item as prepared
        current_request = order_item['special_request'] or ''
        if '[PREPARED]' not in current_request:
            new_request = current_request.strip()
            if new_request:
                new_request += ' [PREPARED]'
            else:
                new_request = '[PREPARED]'
            
            cursor.execute("""
                UPDATE order_items 
                SET special_request = %s
                WHERE id = %s
            """, (new_request, order_item_id))
        
        # Check if all items in this order are now prepared
        cursor.execute("""
            SELECT COUNT(*) as total_items,
                   SUM(CASE WHEN special_request LIKE '%[PREPARED]%' THEN 1 ELSE 0 END) as prepared_items
            FROM order_items 
            WHERE order_id = %s
        """, (order_id,))
        
        item_status = cursor.fetchone()
        orders_ready = []
        
        # If all items are prepared, update order status to "prepared"
        if item_status['total_items'] == item_status['prepared_items']:
            cursor.execute("""
                UPDATE orders 
                SET status = 'prepared' 
                WHERE id = %s
            """, (order_id,))
            
            # Get order details for notification
            cursor.execute("""
                SELECT id, client_name, total_amount
                FROM orders 
                WHERE id = %s
            """, (order_id,))
            
            order_details = cursor.fetchone()
            if order_details:
                orders_ready.append(order_details)
        
        connection.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Order item marked as prepared',
            'orders_ready': orders_ready
        })
        
    except Error as e:
        logger.error(f"Error marking item as prepared: {e}")
        connection.rollback()
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/preparation/redo_prepared', methods=['POST'])
@login_required
def redo_prepared_item():
    """Mark a prepared item as pending again"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        data = request.get_json()
        order_item_id = data.get('order_item_id')
        
        if not order_item_id:
            return jsonify({'success': False, 'message': 'Missing order item ID'})
        
        cursor = connection.cursor(dictionary=True)
        
        # Get order item details
        cursor.execute("""
            SELECT oi.*, o.id as order_id
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE oi.id = %s
        """, (order_item_id,))
        
        order_item = cursor.fetchone()
        if not order_item:
            return jsonify({'success': False, 'message': 'Order item not found'})
        
        order_id = order_item['order_id']
        
        # Remove the [PREPARED] marker from special_request
        current_request = order_item['special_request'] or ''
        new_request = current_request.replace('[PREPARED]', '').strip()
        if not new_request:
            new_request = None
        
        cursor.execute("""
            UPDATE order_items 
            SET special_request = %s
            WHERE id = %s
        """, (new_request, order_item_id))
        
        # Check if this was the last prepared item, if so, revert order status to pending
        cursor.execute("""
            SELECT COUNT(*) as total_items,
                   SUM(CASE WHEN special_request LIKE '%[PREPARED]%' THEN 1 ELSE 0 END) as prepared_items
            FROM order_items 
            WHERE order_id = %s
        """, (order_id,))
        
        item_status = cursor.fetchone()
        
        # If no items are prepared, update order status back to pending
        if item_status['prepared_items'] == 0:
            cursor.execute("""
                UPDATE orders 
                SET status = 'pending' 
                WHERE id = %s AND status = 'prepared'
            """, (order_id,))
        
        connection.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Order item marked as pending',
        })
        
    except Error as e:
        logger.error(f"Error redoing prepared item: {e}")
        connection.rollback()
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

# Expenses management routes
@app.route('/expenses')
@login_required
def expenses():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('expenses/list.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get all expenses with categories and user info
        cursor.execute("""
            SELECT e.*, ec.name as category_name, u.name as created_by_name 
            FROM expenses e
            LEFT JOIN expense_categories ec ON e.category_id = ec.id
            LEFT JOIN users u ON e.created_by = u.id
            ORDER BY e.expense_date DESC, e.created_at DESC
        """)
        expenses = cursor.fetchall()
        
        # Calculate today's expenses
        today = datetime.now().date()
        today_expenses = [exp for exp in expenses if exp['expense_date'] == today]
        today_count = len(today_expenses)
        
        return render_template('expenses/list.html', expenses=expenses, today_count=today_count)
        
    except Error as e:
        logger.error(f"Expenses error: {e}")
        flash('Error loading expenses.', 'danger')
        return render_template('expenses/list.html')
    finally:
        cursor.close()
        connection.close()

@app.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        amount = request.form.get('amount')
        expense_date = request.form.get('expense_date')
        
        if not description or not amount or not expense_date:
            flash('Description, amount, and date are required.', 'danger')
            return render_template('expenses/add.html')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Amount must be a positive number.', 'danger')
                return render_template('expenses/add.html')
        except ValueError:
            flash('Invalid amount format.', 'danger')
            return render_template('expenses/add.html')
        
        # Handle file upload
        receipt_document = None
        if 'receipt_document' in request.files:
            file = request.files['receipt_document']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Generate unique filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # Create expense directory if it doesn't exist
                expense_dir = os.path.join(UPLOAD_DIR, 'expenses')
                os.makedirs(expense_dir, exist_ok=True)
                
                file_path = safe_join(expense_dir, filename)
                if file_path:
                    file.save(file_path)
                    receipt_document = filename
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'danger')
            return render_template('expenses/add.html')
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO expenses (category_id, description, amount, expense_date, receipt_document, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (category_id if category_id else None, description, amount, expense_date, receipt_document, session['user_id']))
            
            connection.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses'))
            
        except Error as e:
            logger.error(f"Add expense error: {e}")
            flash('Error adding expense.', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    # Get categories for dropdown
    connection = get_db_connection()
    categories = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM expense_categories WHERE is_active = TRUE ORDER BY name")
            categories = cursor.fetchall()
        except Error as e:
            logger.error(f"Get expense categories error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('expenses/add.html', categories=categories)

# Finance and analytics routes
@app.route('/finance')
@login_required
def finance_reports():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('finance/reports.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get current month data by default
        from datetime import date
        today = date.today()
        start_of_month = today.replace(day=1)
        
        # Get starting balance
        cursor.execute("SELECT setting_value FROM business_settings WHERE setting_key = 'starting_balance'")
        result = cursor.fetchone()
        starting_balance = float(result['setting_value']) if result else 0.0
        
        # Get current month revenue (all orders)
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as order_count
            FROM orders 
            WHERE DATE(delivery_date) >= %s AND DATE(delivery_date) <= %s
        """, (start_of_month, today))
        revenue_data = cursor.fetchone()
        
        # Get completed/delivered revenue
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as completed_revenue, COUNT(*) as completed_count
            FROM orders 
            WHERE DATE(delivery_date) >= %s AND DATE(delivery_date) <= %s 
            AND status IN ('completed', 'delivered')
        """, (start_of_month, today))
        completed_data = cursor.fetchone()
        
        # Get current month expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) as total_expenses, COUNT(*) as expense_count
            FROM expenses 
            WHERE expense_date >= %s AND expense_date <= %s
        """, (start_of_month, today))
        expense_data = cursor.fetchone()
        
        # Calculate profit/loss
        total_revenue = float(revenue_data['total_revenue'])
        completed_revenue = float(completed_data['completed_revenue'])
        total_expenses = float(expense_data['total_expenses'])
        
        # Get refund data for current month
        cursor.execute("""
            SELECT COALESCE(SUM(r.refund_amount), 0) as total_refunds, COUNT(*) as refund_count,
                   COUNT(CASE WHEN r.refund_status = 'pending' THEN 1 END) as pending_refunds,
                   COUNT(CASE WHEN r.refund_status = 'approved' THEN 1 END) as approved_refunds,
                   COUNT(CASE WHEN r.refund_status = 'processed' THEN 1 END) as processed_refunds
            FROM refunds r
            JOIN orders o ON r.order_id = o.id
            WHERE DATE(o.delivery_date) >= %s AND DATE(o.delivery_date) <= %s
        """, (start_of_month, today))
        refund_data = cursor.fetchone()
        
        total_refunds = float(refund_data['total_refunds'])
        net_revenue = completed_revenue - total_refunds  # Revenue after refunds
        profit_loss = net_revenue - total_expenses
        
        # Calculate refund rate
        refund_rate = (total_refunds / completed_revenue * 100) if completed_revenue > 0 else 0
        
        # Get recent orders (last 10)
        cursor.execute("""
            SELECT o.id, o.client_name, o.total_amount, o.status, o.delivery_date, o.created_at,
                   u.name as created_by_name
            FROM orders o
            LEFT JOIN users u ON o.created_by = u.id
            ORDER BY o.created_at DESC
            LIMIT 10
        """)
        recent_orders = cursor.fetchall()
        
        # Get recent expenses (last 10)
        cursor.execute("""
            SELECT e.id, e.description, e.amount, e.expense_date, e.created_at,
                   ec.name as category_name, u.name as created_by_name
            FROM expenses e
            LEFT JOIN expense_categories ec ON e.category_id = ec.id
            LEFT JOIN users u ON e.created_by = u.id
            ORDER BY e.created_at DESC
            LIMIT 10
        """)
        recent_expenses = cursor.fetchall()
        
        # Get top expense categories this month
        cursor.execute("""
            SELECT ec.name as category_name, COALESCE(SUM(e.amount), 0) as total_amount
            FROM expense_categories ec
            LEFT JOIN expenses e ON ec.id = e.category_id 
                AND e.expense_date >= %s AND e.expense_date <= %s
            WHERE ec.is_active = TRUE
            GROUP BY ec.id, ec.name
            HAVING total_amount > 0
            ORDER BY total_amount DESC
            LIMIT 5
        """, (start_of_month, today))
        top_expense_categories = cursor.fetchall()
        
        # Prepare dashboard data
        dashboard_data = {
            'period_start': start_of_month.strftime('%Y-%m-%d'),
            'period_end': today.strftime('%Y-%m-%d'),
            'period_name': f"{today.strftime('%B %Y')} (Month to Date)",
            'starting_balance': starting_balance,
            'total_revenue': total_revenue,
            'completed_revenue': completed_revenue,
            'net_revenue': net_revenue,
            'total_expenses': total_expenses,
            'total_refunds': total_refunds,
            'refund_rate': refund_rate,
            'profit_loss': profit_loss,
            'order_count': revenue_data['order_count'],
            'completed_count': completed_data['completed_count'],
            'expense_count': expense_data['expense_count'],
            'refund_count': refund_data['refund_count'],
            'pending_refunds': refund_data['pending_refunds'],
            'approved_refunds': refund_data['approved_refunds'],
            'processed_refunds': refund_data['processed_refunds'],
            'recent_orders': recent_orders,
            'recent_expenses': recent_expenses,
            'top_expense_categories': top_expense_categories
        }
        
        return render_template('finance/reports.html', data=dashboard_data)
        
    except Error as e:
        logger.error(f"Finance dashboard error: {e}")
        flash('Error loading finance data.', 'danger')
        return render_template('finance/reports.html')
    finally:
        cursor.close()
        connection.close()

@app.route('/finance/report', methods=['POST'])
@login_required
def generate_finance_report():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    report_type = request.form.get('report_type')
    format_type = request.form.get('format', 'html')
    
    if not start_date or not end_date or not report_type:
        flash('Start date, end date, and report type are required.', 'danger')
        return redirect(url_for('finance_reports'))
    
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('finance_reports'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get starting balance (handle missing table gracefully)
        try:
            cursor.execute("SELECT setting_value FROM business_settings WHERE setting_key = 'starting_balance'")
            result = cursor.fetchone()
            starting_balance = float(result['setting_value']) if result else 0.0
        except Error:
            # Table doesn't exist or other error, use default
            starting_balance = 0.0
        
        # Common queries for all report types
        # Get revenue (all orders regardless of status to show complete picture)
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as order_count
            FROM orders 
            WHERE DATE(delivery_date) BETWEEN %s AND %s
        """, (start_date, end_date))
        revenue_data = cursor.fetchone()
        
        # Get completed/delivered revenue separately
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) as completed_revenue, COUNT(*) as completed_count
            FROM orders 
            WHERE DATE(delivery_date) BETWEEN %s AND %s 
            AND status IN ('completed', 'delivered')
        """, (start_date, end_date))
        completed_data = cursor.fetchone()
        
        # Get expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) as total_expenses, COUNT(*) as expense_count
            FROM expenses 
            WHERE expense_date BETWEEN %s AND %s
        """, (start_date, end_date))
        expense_data = cursor.fetchone()
        
        # Calculate profit/loss
        total_revenue = float(revenue_data['total_revenue'])
        completed_revenue = float(completed_data['completed_revenue'])
        total_expenses = float(expense_data['total_expenses'])
        profit_loss = completed_revenue - total_expenses
        
        # Generate different reports based on type
        report_data = {
            'report_type': report_type,
            'start_date': start_date,
            'end_date': end_date,
            'starting_balance': starting_balance,
            'total_revenue': total_revenue,
            'completed_revenue': completed_revenue,
            'total_expenses': total_expenses,
            'profit_loss': profit_loss,
            'order_count': revenue_data['order_count'],
            'completed_count': completed_data['completed_count'],
            'expense_count': expense_data['expense_count']
        }
        
        if report_type == 'profit_loss':
            # Standard profit & loss report with expense breakdown
            cursor.execute("""
                SELECT ec.name as category_name, COALESCE(SUM(e.amount), 0) as total_amount, COUNT(e.id) as count
                FROM expense_categories ec
                LEFT JOIN expenses e ON ec.id = e.category_id 
                    AND e.expense_date BETWEEN %s AND %s
                WHERE ec.is_active = TRUE
                GROUP BY ec.id, ec.name
                ORDER BY total_amount DESC
            """, (start_date, end_date))
            report_data['expense_breakdown'] = cursor.fetchall()
            
        elif report_type == 'revenue_analysis':
            # Revenue analysis with daily breakdown
            cursor.execute("""
                SELECT DATE(delivery_date) as order_date, 
                       COALESCE(SUM(total_amount), 0) as daily_revenue,
                       COALESCE(SUM(CASE WHEN status IN ('completed', 'delivered') THEN total_amount ELSE 0 END), 0) as completed_revenue,
                       COUNT(*) as order_count,
                       AVG(total_amount) as avg_order_value
                FROM orders 
                WHERE DATE(delivery_date) BETWEEN %s AND %s
                GROUP BY DATE(delivery_date)
                ORDER BY order_date
            """, (start_date, end_date))
            report_data['daily_revenue'] = cursor.fetchall()
            
        elif report_type == 'expense_breakdown':
            # Detailed expense breakdown
            cursor.execute("""
                SELECT e.*, ec.name as category_name, u.name as created_by_name
                FROM expenses e
                LEFT JOIN expense_categories ec ON e.category_id = ec.id
                LEFT JOIN users u ON e.created_by = u.id
                WHERE e.expense_date BETWEEN %s AND %s
                ORDER BY e.expense_date DESC, e.created_at DESC
            """, (start_date, end_date))
            report_data['detailed_expenses'] = cursor.fetchall()
            
            cursor.execute("""
                SELECT ec.name as category_name, COALESCE(SUM(e.amount), 0) as total_amount, COUNT(e.id) as count
                FROM expense_categories ec
                LEFT JOIN expenses e ON ec.id = e.category_id 
                    AND e.expense_date BETWEEN %s AND %s
                WHERE ec.is_active = TRUE
                GROUP BY ec.id, ec.name
                ORDER BY total_amount DESC
            """, (start_date, end_date))
            report_data['expense_breakdown'] = cursor.fetchall()
            
        elif report_type == 'daily_summary':
            # Daily sales summary
            cursor.execute("""
                SELECT DATE(delivery_date) as order_date,
                       COALESCE(SUM(total_amount), 0) as daily_revenue,
                       COALESCE(SUM(CASE WHEN status IN ('completed', 'delivered') THEN total_amount ELSE 0 END), 0) as completed_revenue,
                       COUNT(*) as order_count,
                       COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders,
                       COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_orders,
                       COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_orders,
                       AVG(total_amount) as avg_order_value
                FROM orders 
                WHERE DATE(delivery_date) BETWEEN %s AND %s
                GROUP BY DATE(delivery_date)
                ORDER BY order_date DESC
            """, (start_date, end_date))
            report_data['daily_summary'] = cursor.fetchall()
            
        elif report_type == 'menu_performance':
            # Menu item performance analysis
            cursor.execute("""
                SELECT mi.name as item_name, mi.arabic_name,
                       COALESCE(SUM(oi.quantity), 0) as total_quantity,
                       COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue,
                       COUNT(DISTINCT o.id) as order_count,
                       AVG(oi.unit_price) as avg_price,
                       mi.price as current_price
                FROM menu_items mi
                LEFT JOIN order_items oi ON mi.id = oi.menu_item_id
                LEFT JOIN orders o ON oi.order_id = o.id 
                    AND DATE(o.delivery_date) BETWEEN %s AND %s
                WHERE mi.is_available = TRUE
                GROUP BY mi.id, mi.name, mi.arabic_name, mi.price
                ORDER BY total_revenue DESC, total_quantity DESC
            """, (start_date, end_date))
            report_data['menu_performance'] = cursor.fetchall()
            
        elif report_type == 'monthly_trends':
            # Monthly trends analysis
            cursor.execute("""
                SELECT 
                    YEAR(delivery_date) as year,
                    MONTH(delivery_date) as month,
                    MONTHNAME(delivery_date) as month_name,
                    COALESCE(SUM(total_amount), 0) as monthly_revenue,
                    COALESCE(SUM(CASE WHEN status IN ('completed', 'delivered') THEN total_amount ELSE 0 END), 0) as completed_revenue,
                    COUNT(*) as order_count,
                    AVG(total_amount) as avg_order_value
                FROM orders 
                WHERE DATE(delivery_date) BETWEEN %s AND %s
                GROUP BY YEAR(delivery_date), MONTH(delivery_date)
                ORDER BY year DESC, month DESC
            """, (start_date, end_date))
            report_data['monthly_trends'] = cursor.fetchall()
            
        elif report_type == 'tax_summary':
            # Tax summary report
            tax_rate = 0.15  # 15% default tax rate
            report_data['tax_rate'] = tax_rate
            report_data['taxable_revenue'] = completed_revenue
            report_data['tax_amount'] = completed_revenue * tax_rate
            report_data['net_after_tax'] = completed_revenue - (completed_revenue * tax_rate)
            
        elif report_type == 'refund_analysis':
            # Refund analysis report
            cursor.execute("""
                SELECT r.*, o.client_name, o.client_mobile, o.total_amount as order_total,
                       o.delivery_date, u.name as requested_by_name
                FROM refunds r
                JOIN orders o ON r.order_id = o.id
                LEFT JOIN users u ON r.requested_by = u.id
                WHERE DATE(o.delivery_date) BETWEEN %s AND %s
                ORDER BY r.request_date DESC
            """, (start_date, end_date))
            report_data['refund_details'] = cursor.fetchall()
            
            # Refund statistics by status
            cursor.execute("""
                SELECT r.refund_status, COUNT(*) as count, 
                       COALESCE(SUM(r.refund_amount), 0) as total_amount
                FROM refunds r
                JOIN orders o ON r.order_id = o.id
                WHERE DATE(o.delivery_date) BETWEEN %s AND %s
                GROUP BY r.refund_status
            """, (start_date, end_date))
            report_data['refund_by_status'] = cursor.fetchall()
            
            # Daily refund trend
            cursor.execute("""
                SELECT DATE(r.request_date) as refund_date,
                       COUNT(*) as daily_refund_count,
                       COALESCE(SUM(r.refund_amount), 0) as daily_refund_amount
                FROM refunds r
                JOIN orders o ON r.order_id = o.id
                WHERE DATE(o.delivery_date) BETWEEN %s AND %s
                GROUP BY DATE(r.request_date)
                ORDER BY refund_date
            """, (start_date, end_date))
            report_data['daily_refund_trend'] = cursor.fetchall()
            
            # Refund reasons analysis
            cursor.execute("""
                SELECT r.refund_reason, COUNT(*) as count,
                       COALESCE(SUM(r.refund_amount), 0) as total_amount
                FROM refunds r
                JOIN orders o ON r.order_id = o.id
                WHERE DATE(o.delivery_date) BETWEEN %s AND %s
                GROUP BY r.refund_reason
                ORDER BY count DESC
            """, (start_date, end_date))
            report_data['refund_by_reason'] = cursor.fetchall()
            
        # Prepare template variables
        from datetime import datetime
        template_vars = {
            'report_type': report_type,
            'report_title': get_report_title(report_type),
            'report_type_display': get_report_type_display(report_type),
            'start_date': datetime.strptime(start_date, '%Y-%m-%d').date(),
            'end_date': datetime.strptime(end_date, '%Y-%m-%d').date(),
            'generated_date': datetime.now(),
            'starting_balance': starting_balance,
            'total_revenue': total_revenue,
            'completed_revenue': completed_revenue,
            'total_expenses': total_expenses,
            'profit_loss': profit_loss,
            'net_profit': profit_loss,
            'order_count': revenue_data['order_count'],
            'completed_count': completed_data['completed_count'],
            'expense_count': expense_data['expense_count'],
            'total_orders': revenue_data['order_count'],
            'avg_order_value': total_revenue / revenue_data['order_count'] if revenue_data['order_count'] > 0 else 0,
            'profit_margin': (profit_loss / completed_revenue * 100) if completed_revenue > 0 else 0
        }
        
        # Add report-specific data
        if report_type == 'profit_loss':
            expense_breakdown = {}
            if 'expense_breakdown' in report_data:
                for item in report_data['expense_breakdown']:
                    expense_breakdown[item['category_name']] = float(item['total_amount'])
            template_vars['expense_breakdown'] = expense_breakdown
            
            # Create revenue breakdown (simplified for now)
            template_vars['revenue_breakdown'] = {
                'Order Sales': completed_revenue
            }
            
        elif report_type == 'revenue_analysis':
            template_vars['daily_revenue'] = []
            if 'daily_revenue' in report_data:
                for item in report_data['daily_revenue']:
                    template_vars['daily_revenue'].append({
                        'date': datetime.strptime(str(item['order_date']), '%Y-%m-%d').date(),
                        'order_count': item['order_count'],
                        'revenue': float(item['daily_revenue']),
                        'avg_order_value': float(item['avg_order_value'])
                    })
            
            # Calculate averages
            num_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
            template_vars['avg_daily_revenue'] = total_revenue / num_days if num_days > 0 else 0
            
        elif report_type == 'expense_breakdown':
            template_vars['expenses_detail'] = []
            if 'detailed_expenses' in report_data:
                for expense in report_data['detailed_expenses']:
                    template_vars['expenses_detail'].append({
                        'expense_date': expense['expense_date'],
                        'description': expense['description'],
                        'category_name': expense['category_name'],
                        'amount': float(expense['amount'])
                    })
            
            # Calculate averages
            num_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
            template_vars['avg_daily_expenses'] = total_expenses / num_days if num_days > 0 else 0
            template_vars['avg_expense_amount'] = total_expenses / expense_data['expense_count'] if expense_data['expense_count'] > 0 else 0
            
        elif report_type == 'menu_performance':
            template_vars['menu_performance'] = []
            if 'menu_performance' in report_data:
                for item in report_data['menu_performance']:
                    template_vars['menu_performance'].append({
                        'name': f"{item['item_name']} ({item['arabic_name']})" if item['arabic_name'] else item['item_name'],
                        'quantity_sold': int(item['total_quantity']),
                        'revenue': float(item['total_revenue']),
                        'avg_price': float(item['avg_price'])
                    })
        
        # Handle different output formats
        if format_type == 'pdf':
            flash('PDF export is not yet implemented. Showing web view instead.', 'info')
            return render_template('finance/report_result.html', **template_vars)
        elif format_type == 'excel':
            flash('Excel export is not yet implemented. Showing web view instead.', 'info')
            return render_template('finance/report_result.html', **template_vars)
        else:  # html format
            return render_template('finance/report_result.html', **template_vars)
        
    except Error as e:
        logger.error(f"Finance report error: {e}")
        flash('Error generating finance report.', 'danger')
        return redirect(url_for('finance_reports'))
    finally:
        cursor.close()
        connection.close()

@app.route('/finance/export', methods=['POST'])
@login_required
def export_finance_data():
    export_type = request.form.get('export_type')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    export_format = request.form.get('format')
    
    if not start_date or not end_date or not export_type or not export_format:
        flash('All fields are required for export.', 'danger')
        return redirect(url_for('finance_reports'))
    
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('finance_reports'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        export_data = []
        
        if export_type in ['all', 'orders']:
            # Get orders data
            cursor.execute("""
                SELECT o.id as order_id, o.client_name, o.client_mobile, o.total_amount, 
                       o.status, o.delivery_date, o.created_at, o.notes,
                       u.name as created_by_name
                FROM orders o
                LEFT JOIN users u ON o.created_by = u.id
                WHERE DATE(o.delivery_date) BETWEEN %s AND %s
                ORDER BY o.delivery_date DESC, o.created_at DESC
            """, (start_date, end_date))
            orders = cursor.fetchall()
            
            for order in orders:
                export_data.append({
                    'type': 'order',
                    'date': order['delivery_date'].strftime('%Y-%m-%d'),
                    'description': f"Order #{order['order_id']} - {order['client_name']}",
                    'amount': float(order['total_amount']),
                    'status': order['status'],
                    'client': order['client_name'],
                    'mobile': order['client_mobile'],
                    'notes': order['notes'] or '',
                    'created_by': order['created_by_name']
                })
        
        if export_type in ['all', 'expenses']:
            # Get expenses data
            cursor.execute("""
                SELECT e.*, ec.name as category_name, u.name as created_by_name
                FROM expenses e
                LEFT JOIN expense_categories ec ON e.category_id = ec.id
                LEFT JOIN users u ON e.created_by = u.id
                WHERE e.expense_date BETWEEN %s AND %s
                ORDER BY e.expense_date DESC, e.created_at DESC
            """, (start_date, end_date))
            expenses = cursor.fetchall()
            
            for expense in expenses:
                export_data.append({
                    'type': 'expense',
                    'date': expense['expense_date'].strftime('%Y-%m-%d'),
                    'description': expense['description'],
                    'amount': -float(expense['amount']),  # Negative for expenses
                    'category': expense['category_name'] or 'Uncategorized',
                    'created_by': expense['created_by_name'],
                    'receipt': expense['receipt_document'] or ''
                })
        
        if export_format == 'csv':
            output = io.StringIO()
            
            if export_type == 'summary':
                # Create summary CSV
                writer = csv.writer(output)
                writer.writerow(['Date Range', f"{start_date} to {end_date}"])
                writer.writerow([])
                
                # Calculate totals
                total_revenue = sum(item['amount'] for item in export_data if item['type'] == 'order')
                total_expenses = sum(abs(item['amount']) for item in export_data if item['type'] == 'expense')
                profit_loss = total_revenue - total_expenses
                
                writer.writerow(['Summary'])
                writer.writerow(['Total Revenue', f"${total_revenue:.2f}"])
                writer.writerow(['Total Expenses', f"${total_expenses:.2f}"])
                writer.writerow(['Profit/Loss', f"${profit_loss:.2f}"])
                writer.writerow([])
                
                # Revenue by day
                revenue_by_day = {}
                for item in export_data:
                    if item['type'] == 'order':
                        date = item['date']
                        revenue_by_day[date] = revenue_by_day.get(date, 0) + item['amount']
                
                writer.writerow(['Daily Revenue'])
                writer.writerow(['Date', 'Revenue'])
                for date, revenue in sorted(revenue_by_day.items()):
                    writer.writerow([date, f"${revenue:.2f}"])
            else:
                # Create detailed CSV
                if export_type in ['all', 'orders'] and export_type in ['all', 'expenses']:
                    writer = csv.writer(output)
                    writer.writerow(['Type', 'Date', 'Description', 'Amount', 'Status/Category', 'Client/Created By', 'Mobile/Receipt', 'Notes']);
                    
                    for item in sorted(export_data, key=lambda x: x['date'], reverse=True):
                        if item['type'] == 'order':
                            writer.writerow([
                                'Order',
                                item['date'],
                                item['description'],
                                f"${item['amount']:.2f}",
                                item['status'],
                                item['client'],
                                item['mobile'],
                                item['notes']
                            ])
                        else:
                            writer.writerow([
                                'Expense',
                                item['date'],
                                item['description'],
                                f"${abs(item['amount']):.2f}",
                                item['category'],
                                item['created_by'],
                                item['receipt'],
                                ''
                            ])
                elif export_type == 'orders':
                    writer = csv.writer(output)
                    writer.writerow(['Order ID', 'Date', 'Client Name', 'Mobile', 'Amount', 'Status', 'Notes', 'Created By'])
                    
                    for item in export_data:
                        if item['type'] == 'order':
                            writer.writerow([
                                item['description'].split('#')[1].split(' - ')[0],
                                item['date'],
                                item['client'],
                                item['mobile'],
                                f"${item['amount']:.2f}",
                                item['status'],
                                item['notes'],
                                item['created_by']
                            ])
                else:  # expenses
                    writer = csv.writer(output)
                    writer.writerow(['Date', 'Description', 'Amount', 'Category', 'Created By', 'Receipt']);
                    
                    for item in export_data:
                        if item['type'] == 'expense':
                            writer.writerow([
                                item['date'],
                                item['description'],
                                f"${abs(item['amount']):.2f}",
                                item['category'],
                                item['created_by'],
                                item['receipt']
                            ])
            
            # Return CSV file
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=finance_export_{start_date}_to_{end_date}.csv'
            return response
        
        elif export_format == 'json':
            # Return JSON data
            return jsonify({
                'export_type': export_type,
                'date_range': f"{start_date} to {end_date}",
                'data': export_data,
                'summary': {
                    'total_revenue': sum(item['amount'] for item in export_data if item['type'] == 'order'),
                    'total_expenses': sum(abs(item['amount']) for item in export_data if item['type'] == 'expense'),
                    'total_records': len(export_data)
                }
            })
        
        else:  # PDF format
            flash('PDF export is not yet implemented. Please use CSV format.', 'info')
            return redirect(url_for('finance_reports'))
            
    except Error as e:
        logger.error(f"Export finance data error: {e}")
        flash('Error exporting finance data.', 'danger')
        return redirect(url_for('finance_reports'))
    finally:
        cursor.close()
        connection.close()

@app.route('/analytics')
@login_required
def analytics():
    connection = get_db_connection()
    if not connection:
        if request.is_json or request.args.get('period') or request.args.get('start_date'):
            return jsonify({'error': 'Database connection error'})
        flash('Database connection error.', 'danger')
        return render_template('analytics/dashboard.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get date range based on parameters
        period = request.args.get('period', '30_days')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date and end_date:
            # Custom date range
            current_start = start_date
            current_end = end_date
            # Calculate previous period for comparison
            from datetime import datetime, timedelta
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            period_days = (end_dt - start_dt).days
            prev_end_dt = start_dt - timedelta(days=1)
            prev_start_dt = prev_end_dt - timedelta(days=period_days)
            prev_start = prev_start_dt.strftime('%Y-%m-%d')
            prev_end = prev_end_dt.strftime('%Y-%m-%d')
        elif period == '7_days':
            current_start = 'DATE_SUB(NOW(), INTERVAL 7 DAY)'
            current_end = 'NOW()'
            prev_start = 'DATE_SUB(NOW(), INTERVAL 14 DAY)'
            prev_end = 'DATE_SUB(NOW(), INTERVAL 7 DAY)'
        elif period == '90_days':
            current_start = 'DATE_SUB(NOW(), INTERVAL 90 DAY)'
            current_end = 'NOW()'
            prev_start = 'DATE_SUB(NOW(), INTERVAL 180 DAY)'
            prev_end = 'DATE_SUB(NOW(), INTERVAL 90 DAY)'
        else:  # default 30_days
            current_start = 'DATE_SUB(NOW(), INTERVAL 30 DAY)'
            current_end = 'NOW()'
            prev_start = 'DATE_SUB(NOW(), INTERVAL 60 DAY)'
            prev_end = 'DATE_SUB(NOW(), INTERVAL 30 DAY)'
        
        # Calculate current period revenue
        if start_date and end_date:
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as total_orders
                FROM orders
                WHERE DATE(created_at) BETWEEN %s AND %s
                AND status IN ('completed', 'delivered')
            """, (current_start, current_end))
        else:
            cursor.execute(f"""
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as total_orders
                FROM orders
                WHERE created_at >= {current_start}
                AND status IN ('completed', 'delivered')
            """)
        current_period = cursor.fetchone()
        
        # Calculate previous period revenue
        if start_date and end_date:
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as total_orders
                FROM orders
                WHERE DATE(created_at) BETWEEN %s AND %s
                AND status IN ('completed', 'delivered')
            """, (prev_start, prev_end))
        else:
            cursor.execute(f"""
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue, COUNT(*) as total_orders
                FROM orders
                WHERE created_at >= {prev_start} AND created_at < {prev_end}
                AND status IN ('completed', 'delivered')
            """)
        previous_period = cursor.fetchone()
        
        # Calculate trends
        current_revenue = float(current_period['total_revenue'])
        previous_revenue = float(previous_period['total_revenue'])
        current_orders = current_period['total_orders']
        previous_orders = previous_period['total_orders']
        
        revenue_trend = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
        orders_trend = ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0
        avg_order_value = current_revenue / current_orders if current_orders > 0 else 0
        prev_avg_order_value = previous_revenue / previous_orders if previous_orders > 0 else 0
        avg_trend = ((avg_order_value - prev_avg_order_value) / prev_avg_order_value * 100) if prev_avg_order_value > 0 else 0
        
        # Calculate expenses for profit margin
        if start_date and end_date:
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) as total_expenses
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s
            """, (current_start, current_end))
        else:
            cursor.execute(f"""
                SELECT COALESCE(SUM(amount), 0) as total_expenses
                FROM expenses
                WHERE expense_date >= {current_start}
            """)
        expenses_result = cursor.fetchone()
        total_expenses = float(expenses_result['total_expenses'])
        profit_margin = ((current_revenue - total_expenses) / current_revenue * 100) if current_revenue > 0 else 0
        
        # Previous period expenses for margin trend
        if start_date and end_date:
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) as total_expenses
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s
            """, (prev_start, prev_end))
        else:
            cursor.execute(f"""
                SELECT COALESCE(SUM(amount), 0) as total_expenses
                FROM expenses
                WHERE expense_date >= {prev_start} AND expense_date < {prev_end}
            """)
        prev_expenses_result = cursor.fetchone()
        prev_total_expenses = float(prev_expenses_result['total_expenses'])
        prev_profit_margin = ((previous_revenue - prev_total_expenses) / previous_revenue * 100) if previous_revenue > 0 else 0
        margin_trend = profit_margin - prev_profit_margin
        
        # Top selling items
        if start_date and end_date:
            cursor.execute("""
                SELECT oi.menu_item_name, 
                       COALESCE(oi.menu_item_arabic_name, mi.arabic_name) as menu_item_arabic_name,
                       SUM(oi.quantity) as total_quantity, 
                       SUM(oi.subtotal) as total_revenue, COUNT(DISTINCT oi.order_id) as order_count
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.id
                LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                WHERE DATE(o.created_at) BETWEEN %s AND %s
                AND o.status IN ('completed', 'delivered')
                GROUP BY oi.menu_item_id, oi.menu_item_name, COALESCE(oi.menu_item_arabic_name, mi.arabic_name)
                ORDER BY total_quantity DESC
                LIMIT 10
            """, (current_start, current_end))
        else:
            cursor.execute(f"""
                SELECT oi.menu_item_name,
                       COALESCE(oi.menu_item_arabic_name, mi.arabic_name) as menu_item_arabic_name,
                       SUM(oi.quantity) as total_quantity, 
                       SUM(oi.subtotal) as total_revenue, COUNT(DISTINCT oi.order_id) as order_count
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.id
                LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                WHERE o.created_at >= {current_start}
                AND o.status IN ('completed', 'delivered')
                GROUP BY oi.menu_item_id, oi.menu_item_name, COALESCE(oi.menu_item_arabic_name, mi.arabic_name)
                ORDER BY total_quantity DESC
                LIMIT 10
            """)
        top_items = cursor.fetchall()
        
        # Orders by status
        if start_date and end_date:
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM orders
                WHERE DATE(created_at) BETWEEN %s AND %s
                GROUP BY status
            """, (current_start, current_end))
        else:
            cursor.execute(f"""
                SELECT status, COUNT(*) as count
                FROM orders
                WHERE created_at >= {current_start}
                GROUP BY status
            """)
        orders_by_status = cursor.fetchall()
        
        # Sales trend (last 7 days) for chart
        cursor.execute("""
            SELECT DATE(created_at) as sale_date, COUNT(*) as order_count, 
                   COALESCE(SUM(total_amount), 0) as daily_revenue
            FROM orders
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            AND status IN ('completed', 'delivered')
            GROUP BY DATE(created_at)
            ORDER BY sale_date
        """)
        sales_trend = cursor.fetchall()
        
        # Prepare chart data
        revenue_trend_labels = [trend['sale_date'].strftime('%m/%d') for trend in sales_trend]
        revenue_trend_data = [float(trend['daily_revenue']) for trend in sales_trend]
        
        # Category performance (for pie chart)
        if start_date and end_date:
            cursor.execute("""
                SELECT COALESCE(mc.name, 'Uncategorized') as category_name, 
                       SUM(oi.subtotal) as total_revenue
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.id
                LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                LEFT JOIN menu_categories mc ON mi.category_id = mc.id
                WHERE DATE(o.created_at) BETWEEN %s AND %s
                AND o.status IN ('completed', 'delivered')
                GROUP BY mc.id, mc.name
                ORDER BY total_revenue DESC
            """, (current_start, current_end))
        else:
            cursor.execute(f"""
                SELECT COALESCE(mc.name, 'Uncategorized') as category_name, 
                       SUM(oi.subtotal) as total_revenue
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.id
                LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                LEFT JOIN menu_categories mc ON mi.category_id = mc.id
                WHERE o.created_at >= {current_start}
                AND o.status IN ('completed', 'delivered')
                GROUP BY mc.id, mc.name
                ORDER BY total_revenue DESC
            """)
        category_performance = cursor.fetchall()
        
        category_labels = [cat['category_name'] for cat in category_performance]
        category_data = [float(cat['total_revenue']) for cat in category_performance]
        
        # Monthly comparison
        cursor.execute("""
            SELECT MONTH(created_at) as month, YEAR(created_at) as year,
                   COUNT(*) as order_count, COALESCE(SUM(total_amount), 0) as monthly_revenue
            FROM orders
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            AND status IN ('completed', 'delivered')
            GROUP BY YEAR(created_at), MONTH(created_at)
            ORDER BY year DESC, month DESC
            LIMIT 12
        """)
        monthly_data = cursor.fetchall()
        
        analytics_data = {
            'total_revenue': current_revenue,
            'revenue_trend': revenue_trend,
            'total_orders': current_orders,
            'orders_trend': orders_trend,
            'avg_order_value': avg_order_value,
            'avg_trend': avg_trend,
            'profit_margin': profit_margin,
            'margin_trend': margin_trend,
            'top_items': top_items,
            'orders_by_status': orders_by_status,
            'sales_trend': sales_trend,
            'monthly_data': monthly_data,
            'revenue_trend_labels': revenue_trend_labels,
            'revenue_trend_data': revenue_trend_data,
            'category_labels': category_labels,
            'category_data': category_data
        };
        
        # Return JSON for AJAX requests
        if request.is_json or request.args.get('period') or request.args.get('start_date'):
            return jsonify(analytics_data)
        
        return render_template('analytics/dashboard.html', analytics_data=analytics_data)
        
    except Error as e:
        logger.error(f"Analytics error: {e}")
        flash('Error loading analytics data.', 'danger')
        return render_template('analytics/dashboard.html')
    finally:
        cursor.close()
        connection.close()

# User management routes (Admin only)
@app.route('/users')
@admin_required
def user_management():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('users/list.html', users=[], user_stats={'total': 0, 'admin': 0, 'staff': 0, 'active': 0})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get all users with their branch assignments
        cursor.execute("""
            SELECT u.*, u.name as full_name, GROUP_CONCAT(b.name SEPARATOR ', ') as branch_names
            FROM users u
            LEFT JOIN user_branches ub ON u.id = ub.user_id
            LEFT JOIN branches b ON ub.branch_id = b.id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        users = cursor.fetchall()
        
        # Calculate user statistics
        total_users = len(users)
        admin_count = len([u for u in users if u['role'] == 'admin'])
        staff_count = len([u for u in users if u['role'] == 'staff'])
        active_count = len([u for u in users if u.get('is_active', True)])
        
        user_stats = {
            'total': total_users,
            'admin': admin_count,
            'staff': staff_count,
            'active': active_count
        }
        
        return render_template('users/list.html', users=users, user_stats=user_stats)
        
    except Error as e:
        logger.error(f"User management error: {e}")
        flash('Error loading users.', 'danger')
        return render_template('users/list.html', users=[], user_stats={'total': 0, 'admin': 0, 'staff': 0, 'active': 0})
    finally:
        cursor.close()
        connection.close()

@app.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        name = request.form.get('full_name')
        email = request.form.get('email')
        national_id = request.form.get('national_id')
        address = request.form.get('address')
        age = request.form.get('age')
        employed_date = request.form.get('employed_date')
        title = request.form.get('title')
        description = request.form.get('description')
        mobile = request.form.get('phone')
        branch_ids = request.form.getlist('branch_ids')
        
        if not username or not password or not role or not email:
            flash('Username, password, email, and role are required.', 'danger')
            return render_template('users/add.html')
        
        if role not in ['admin', 'staff']:
            flash('Invalid role.', 'danger')
            return render_template('users/add.html')
        
        # Handle profile picture upload
        profile_picture = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                profile_dir = os.path.join(UPLOAD_DIR, 'profile')
                os.makedirs(profile_dir, exist_ok=True)
                
                file_path = safe_join(profile_dir, filename)
                if file_path:
                    file.save(file_path)
                    profile_picture = filename
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'danger')
            return render_template('users/add.html')
        
        try:
            cursor = connection.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    flash('Username already exists.', 'danger')
                else:
                    flash('Email already exists.', 'danger')
                return render_template('users/add.html')
            
            # Create user
            password_hash = generate_password_hash(password)
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, name, email, national_id, address, 
                                 age, employed_date, title, description, mobile, profile_picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, password_hash, role, name, email, national_id, address, 
                  int(age) if age else None, employed_date if employed_date else None, 
                  title, description, mobile, profile_picture))
            
            user_id = cursor.lastrowid
            
            # Assign branches
            if branch_ids:
                for branch_id in branch_ids:
                    cursor.execute("""
                        INSERT INTO user_branches (user_id, branch_id) VALUES (%s, %s)
                    """, (user_id, branch_id))
            
            # Handle document uploads
            if 'documents' in request.files:
                files = request.files.getlist('documents')
                for file in files:
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{filename}"
                        
                        docs_dir = os.path.join(UPLOAD_DIR, 'docs', str(user_id))
                        os.makedirs(docs_dir, exist_ok=True)
                        
                        file_path = safe_join(docs_dir, filename)
                        if file_path:
                            file.save(file_path)
                            cursor.execute("""
                                INSERT INTO user_documents (user_id, document_name, file_path)
                                VALUES (%s, %s, %s)
                            """, (user_id, file.filename, filename))
            
            connection.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('user_management'))
            
        except Error as e:
            logger.error(f"Add user error: {e}")
            flash('Error creating user.', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    # Get branches for dropdown
    connection = get_db_connection()
    branches = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM branches WHERE is_active = TRUE ORDER BY name")
            branches = cursor.fetchall()
        except Error as e:
            logger.error(f"Get branches error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('users/add.html', branches=branches)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('user_management'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if request.method == 'POST':
            username = request.form.get('username')
            role = request.form.get('role')
            name = request.form.get('full_name')
            email = request.form.get('email')
            national_id = request.form.get('national_id')
            address = request.form.get('address')
            age = request.form.get('age')
            employed_date = request.form.get('employed_date')
            title = request.form.get('title')
            description = request.form.get('description')
            mobile = request.form.get('phone')
            password = request.form.get('password')
            
            if not username or not role:
                flash('Username and role are required.', 'danger')
                return redirect(url_for('edit_user', user_id=user_id))
            
            if role not in ['admin', 'staff']:
                flash('Invalid role.', 'danger')
                return redirect(url_for('edit_user', user_id=user_id))
            
            # Check if username or email already exists (excluding current user)
            if email:
                cursor.execute("SELECT id FROM users WHERE (username = %s OR email = %s) AND id != %s", (username, email, user_id))
            else:
                cursor.execute("SELECT id FROM users WHERE username = %s AND id != %s", (username, user_id))
            
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username or email already exists for another user.', 'danger')
                return redirect(url_for('edit_user', user_id=user_id))
            
            # Handle profile picture upload
            profile_picture = None
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    
                    profile_dir = os.path.join(UPLOAD_DIR, 'profile')
                    os.makedirs(profile_dir, exist_ok=True)
                    
                    file_path = safe_join(profile_dir, filename)
                    if file_path:
                        file.save(file_path)
                        profile_picture = filename
            
            # Update user
            update_fields = []
            update_values = []
            
            update_fields.extend(['username = %s', 'role = %s', 'name = %s'])
            update_values.extend([username, role, name])
            
            if email:
                update_fields.append('email = %s')
                update_values.append(email)
            
            if national_id:
                update_fields.append('national_id = %s')
                update_values.append(national_id)
            
            if address:
                update_fields.append('address = %s')
                update_values.append(address)
            
            if age:
                update_fields.append('age = %s')
                update_values.append(int(age))
            
            if employed_date:
                update_fields.append('employed_date = %s')
                update_values.append(employed_date)
            
            if title:
                update_fields.append('title = %s')
                update_values.append(title)
            
            if description:
                update_fields.append('description = %s')
                update_values.append(description)
            
            if mobile:
                update_fields.append('mobile = %s')
                update_values.append(mobile)
            
            if profile_picture:
                update_fields.append('profile_picture = %s')
                update_values.append(profile_picture)
            
            if password:
                password_hash = generate_password_hash(password)
                update_fields.append('password_hash = %s')
                update_values.append(password_hash)
            
            update_values.append(user_id)
            
            cursor.execute(f"""
                UPDATE users SET {', '.join(update_fields)}
                WHERE id = %s
            """, update_values)
            
            connection.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('user_management'))
        
        # GET request - show edit form
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('user_management'))
        
        # Get branches for dropdown
        cursor.execute("SELECT * FROM branches WHERE is_active = TRUE ORDER BY name")
        branches = cursor.fetchall()
        
        return render_template('users/edit.html', user=user, branches=branches)
        
    except Error as e:
        logger.error(f"Edit user error: {e}")
        flash('Error updating user.', 'danger')
        return redirect(url_for('user_management'))
    finally:
        cursor.close()
        connection.close()

@app.route('/users/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status():
    """Toggle user active status"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'message': 'User ID is required'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get current user status
        cursor.execute("SELECT is_active FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Toggle status
        new_status = not user['is_active']
        cursor.execute("UPDATE users SET is_active = %s WHERE id = %s", (new_status, user_id))
        
        connection.commit()
        
        status_text = 'activated' if new_status else 'deactivated'
        return jsonify({'success': True, 'message': f'User {status_text} successfully'})
        
    except Error as e:
        logger.error(f"Toggle user status error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/users/delete', methods=['POST'])
@admin_required
def delete_user():
    """Delete a user"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'message': 'User ID is required'})
    
    # Prevent admin from deleting themselves
    if str(user_id) == str(session.get('user_id')):
        return jsonify({'success': False, 'message': 'You cannot delete your own account'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Delete user (CASCADE will handle related records)
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        connection.commit()
        
        return jsonify({'success': True, 'message': f'User {user["username"]} deleted successfully'})
        
    except Error as e:
        logger.error(f"Delete user error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/users/bulk-action', methods=['POST'])
@admin_required
def bulk_user_action():
    """Perform bulk actions on multiple users"""
    data = request.get_json()
    user_ids = data.get('user_ids', [])
    action = data.get('action')
    
    if not user_ids or not action:
        return jsonify({'success': False, 'message': 'User IDs and action are required'})
    
    if action not in ['activate', 'deactivate', 'delete']:
        return jsonify({'success': False, 'message': 'Invalid action'})
    
    # Prevent admin from performing actions on themselves
    current_user_id = str(session.get('user_id'))
    if current_user_id in [str(uid) for uid in user_ids]:
        return jsonify({'success': False, 'message': 'You cannot perform bulk actions on your own account'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        success_count = 0
        errors = []
        
        for user_id in user_ids:
            try:
                # Check if user exists
                cursor.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                
                if not user:
                    errors.append(f"User ID {user_id} not found")
                    continue
                
                if action == 'delete':
                    # Delete user (CASCADE will handle related records)
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                elif action == 'activate':
                    # Activate user
                    cursor.execute("UPDATE users SET is_active = TRUE WHERE id = %s", (user_id,))
                elif action == 'deactivate':
                    # Deactivate user
                    cursor.execute("UPDATE users SET is_active = FALSE WHERE id = %s", (user_id,))
                
                if cursor.rowcount > 0:
                    success_count += 1
                else:
                    errors.append(f"Failed to {action} user {user['username']}")
                    
            except Error as e:
                logger.error(f"Bulk action error for user {user_id}: {e}")
                errors.append(f"Database error for user ID {user_id}")
        
        connection.commit()
        
        # Prepare response message
        if success_count > 0:
            action_past_tense = {
                'activate': 'activated',
                'deactivate': 'deactivated', 
                'delete': 'deleted'
            }[action]
            
            message = f"Successfully {action_past_tense} {success_count} user(s)"
            if errors:
                message += f". {len(errors)} error(s) occurred."
            
            return jsonify({'success': True, 'message': message, 'errors': errors})
        else:
            return jsonify({'success': False, 'message': 'No users were processed', 'errors': errors})
        
    except Error as e:
        logger.error(f"Bulk user action error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/users/export')
@admin_required
def export_users():
    """Export users data to CSV"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('user_management'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get all users with their branch assignments
        cursor.execute("""
            SELECT u.id, u.username, u.name as full_name, u.email, u.role, 
                   u.mobile, u.national_id, u.address, u.age, u.employed_date,
                   u.title, u.description, u.is_active, u.created_at,
                   GROUP_CONCAT(b.name SEPARATOR ', ') as branch_names
            FROM users u
            LEFT JOIN user_branches ub ON u.id = ub.user_id
            LEFT JOIN branches b ON ub.branch_id = b.id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        users = cursor.fetchall()
        
        # Create CSV content
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        headers = [
            'ID', 'Username', 'Full Name', 'Email', 'Role', 'Mobile', 
            'National ID', 'Address', 'Age', 'Employed Date', 'Title', 
            'Description', 'Status', 'Branches', 'Created Date'
        ]
        writer.writerow(headers)
        
        # Write user data
        for user in users:
            status = 'Active' if user.get('is_active', True) else 'Inactive'
            created_date = user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else ''
            employed_date = user['employed_date'].strftime('%Y-%m-%d') if user['employed_date'] else ''
            
            row = [
                user['id'],
                user['username'],
                user['full_name'] or '',
                user['email'] or '',
                user['role'].title(),
                user['mobile'] or '',
                user['national_id'] or '',
                user['address'] or '',
                user['age'] or '',
                employed_date,
                user['title'] or '',
                user['description'] or '',
                status,
                user['branch_names'] or 'No branches assigned',
                created_date
            ]
            writer.writerow(row)
        
        # Prepare response
        from flask import make_response
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'users_export_{timestamp}.csv'
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
        
    except Error as e:
        logger.error(f"Export users error: {e}")
        flash('Error exporting users data.', 'danger')
        return redirect(url_for('user_management'))
    finally:
        cursor.close()
        connection.close()

# Notifications routes
@app.route('/notifications')
@login_required
def notifications():
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('notifications/list.html')
    
    try:
        cursor = connection.cursor(dictionary=True)
        user_id = session['user_id']
        
        # Get notifications for current user (specific to user or broadcast)
        cursor.execute("""
            SELECT n.*, u.name as sent_by_name
            FROM notifications n
            LEFT JOIN users u ON n.created_by = u.id
            WHERE (n.user_id = %s OR n.user_id IS NULL)
            ORDER BY n.created_at DESC
        """, (user_id,))
        
        notifications = cursor.fetchall()
        
        # Calculate notification counts
        notification_counts = {
            'total': len(notifications),
            'unread': len([n for n in notifications if not n['is_read']]),
            'system': len([n for n in notifications if n.get('message', '').lower().find('system') != -1]),
            'orders': len([n for n in notifications if n.get('message', '').lower().find('order') != -1]),
            'inventory': len([n for n in notifications if n.get('message', '').lower().find('inventory') != -1 or n.get('message', '').lower().find('stock') != -1])
        }
        
        # Get important unread notifications (assuming we add a priority field later)
        unread_important = [n for n in notifications if not n['is_read'] and n.get('message', '').lower().find('important') != -1]
        
        # Default user settings (since we don't have a settings table yet)
        user_settings = ['low_stock', 'daily_reports', 'system_errors', 'new_orders', 'large_orders', 'staff_updates']
        
        return render_template('notifications/list.html', 
                             notifications=notifications,
                             notification_counts=notification_counts,
                             unread_important=unread_important,
                             user_settings=user_settings)
        
    except Error as e:
        logger.error(f"Notifications error: {e}")
        flash('Error loading notifications.', 'danger')
        return render_template('notifications/list.html')
    finally:
        cursor.close()
        connection.close()

@app.route('/notifications/send', methods=['GET', 'POST'])
@admin_required
def send_notification():
    if request.method == 'POST':
        message = request.form.get('message')
        recipient_type = request.form.get('recipient_type')  # 'all' or 'specific'
        user_id = request.form.get('user_id') if recipient_type == 'specific' else None
        
        if not message:
            flash('Message is required.', 'danger')
            return render_template('notifications/send.html')
        
        connection = get_db_connection()
        if not connection:
            flash('Database connection error.', 'danger')
            return render_template('notifications/send.html')
        
        try:
            cursor = connection.cursor()
            
            if recipient_type == 'all':
                # Send to all users (broadcast)
                cursor.execute("""
                    INSERT INTO notifications (user_id, message, created_by)
                    VALUES (NULL, %s, %s)
                """, (message, session['user_id']))
            else:
                # Send to specific user
                cursor.execute("""
                    INSERT INTO notifications (user_id, message, created_by)
                    VALUES (%s, %s, %s)
                """, (user_id, message, session['user_id']))
            
            connection.commit()
            flash('Notification sent successfully!', 'success')
            return redirect(url_for('notifications'))
            
        except Error as e:
            logger.error(f"Send notification error: {e}")
            flash('Error sending notification.', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    # Get staff users for specific notifications
    connection = get_db_connection()
    staff_users = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, username FROM users 
                WHERE role = 'staff' AND is_active = TRUE 
                ORDER BY name
            """)
            staff_users = cursor.fetchall()
        except Error as e:
            logger.error(f"Get staff users error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('notifications/send.html', staff_users=staff_users)

@app.route('/notifications/mark_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        user_id = session['user_id']
        
        # Mark notification as read (only if it belongs to current user or is broadcast)
        cursor.execute("""
            UPDATE notifications 
            SET is_read = TRUE 
            WHERE id = %s AND (user_id = %s OR user_id IS NULL)
        """, (notification_id, user_id))
        
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Notification not found'})
            
    except Error as e:
        logger.error(f"Mark notification read error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/notifications/mark_all_read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        user_id = session['user_id']
        
        # Mark all notifications as read for current user
        cursor.execute("""
            UPDATE notifications 
            SET is_read = TRUE 
            WHERE (user_id = %s OR user_id IS NULL) AND is_read = FALSE
        """, (user_id,))
        
        connection.commit()
        return jsonify({'success': True, 'message': f'{cursor.rowcount} notifications marked as read'})
            
    except Error as e:
        logger.error(f"Mark all notifications read error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/notifications/delete', methods=['POST'])
@login_required
def delete_notification():
    if request.is_json:
        data = request.get_json()
        notification_id = data.get('notification_id')
    else:
        notification_id = request.form.get('notification_id')
    
    if not notification_id:
        return jsonify({'success': False, 'message': 'Notification ID required'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        user_id = session['user_id']
        
        # Delete notification (only if it belongs to current user or user is admin)
        if session.get('role') == 'admin':
            cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
        else:
            cursor.execute("""
                DELETE FROM notifications 
                WHERE id = %s AND (user_id = %s OR user_id IS NULL)
            """, (notification_id, user_id))
        
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Notification not found or access denied'})
            
    except Error as e:
        logger.error(f"Delete notification error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/notifications/settings', methods=['POST'])
@login_required
def update_notification_settings():
    # For now, just return success since we don't have a settings table
    # This can be implemented later when user settings are needed
    flash('Notification settings updated successfully!', 'success')
    return redirect(url_for('notifications'))

# File upload and serving routes
@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    """Serve uploaded files securely"""
    # Basic security check
    if '..' in filename or filename.startswith('/'):
        flash('Invalid file path.', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_from_directory(UPLOAD_DIR, filename)

# Clients management routes
@app.route('/clients')
@login_required
def clients():
    """Clients management page with analytics"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return render_template('clients/list.html', clients=[], stats={})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get all clients with order statistics
        cursor.execute("""
            SELECT c.*, 
                   COUNT(DISTINCT o.id) as total_orders,
                   COALESCE(SUM(o.total_amount), 0) as total_spent,
                   COALESCE(MAX(o.created_at), c.created_at) as last_order_date,
                   COALESCE(AVG(o.total_amount), 0) as avg_order_value
            FROM clients c
            LEFT JOIN orders o ON c.id = o.client_id
            GROUP BY c.id
            ORDER BY total_spent DESC, c.created_at DESC
        """)
        clients = cursor.fetchall()
        
        # Calculate client statistics
        total_clients = len(clients)
        active_clients = len([c for c in clients if c['total_orders'] > 0])
        total_revenue = sum(float(c['total_spent']) for c in clients)
        avg_client_value = total_revenue / total_clients if total_clients > 0 else 0
        
        # Get top clients by orders
        top_by_orders = sorted(clients, key=lambda x: x['total_orders'], reverse=True)[:5]
        
        # Get recent clients (last 30 days)
        cursor.execute("""
            SELECT COUNT(*) as new_clients
            FROM clients 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)
        new_clients_month = cursor.fetchone()['new_clients']
        
        stats = {
            'total_clients': total_clients,
            'active_clients': active_clients,
            'total_revenue': total_revenue,
            'avg_client_value': avg_client_value,
            'new_clients_month': new_clients_month,
            'top_clients': top_by_orders
        }
        
        return render_template('clients/list.html', clients=clients, stats=stats)
        
    except Error as e:
        logger.error(f"Clients error: {e}")
        flash('Error loading clients.', 'danger')
        return render_template('clients/list.html', clients=[], stats={})
    finally:
        cursor.close()
        connection.close()

@app.route('/clients/<int:client_id>')
@login_required
def client_details(client_id):
    """Client details page with order history and analytics"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('clients'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get client information
        cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        client = cursor.fetchone()
        
        if not client:
            flash('Client not found.', 'danger')
            return redirect(url_for('clients'))
        
        # Get client order statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_orders,
                COALESCE(SUM(total_amount), 0) as total_spent,
                COALESCE(AVG(total_amount), 0) as avg_order_value,
                MAX(created_at) as last_order_date,
                MIN(created_at) as first_order_date,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_orders,
                COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_orders,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders
            FROM orders 
            WHERE client_id = %s
        """, (client_id,))
        order_stats = cursor.fetchone()
        
        # Get recent orders
        cursor.execute("""
            SELECT o.*, u.name as created_by_name
            FROM orders o
            LEFT JOIN users u ON o.created_by = u.id
            WHERE o.client_id = %s
            ORDER BY o.created_at DESC
            LIMIT 20
        """, (client_id,))
        recent_orders = cursor.fetchall()
        
        # Get monthly order trend (last 12 months)
        cursor.execute("""
            SELECT 
                YEAR(created_at) as year,
                MONTH(created_at) as month,
                COUNT(*) as order_count,
                SUM(total_amount) as monthly_total
            FROM orders
            WHERE client_id = %s 
            AND created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY YEAR(created_at), MONTH(created_at)
            ORDER BY year DESC, month DESC
        """, (client_id,))
        monthly_trends = cursor.fetchall()
        
        # Get favorite items
        cursor.execute("""
            SELECT 
                oi.menu_item_name,
                COALESCE(oi.menu_item_arabic_name, mi.arabic_name) as menu_item_arabic_name,
                SUM(oi.quantity) as total_quantity,
                COUNT(DISTINCT oi.order_id) as order_frequency,
                SUM(oi.subtotal) as total_spent_on_item
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE o.client_id = %s
            GROUP BY oi.menu_item_id, oi.menu_item_name, COALESCE(oi.menu_item_arabic_name, mi.arabic_name)
            ORDER BY total_quantity DESC
            LIMIT 10
        """, (client_id,))
        favorite_items = cursor.fetchall()
        
        return render_template('clients/details.html', 
                             client=client, 
                             order_stats=order_stats,
                             recent_orders=recent_orders,
                             monthly_trends=monthly_trends,
                             favorite_items=favorite_items)
        
    except Error as e:
        logger.error(f"Client details error: {e}")
        flash('Error loading client details.', 'danger')
        return redirect(url_for('clients'))
    finally:
        cursor.close()
        connection.close()

@app.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    """Edit client information"""
    connection = get_db_connection()
    if not connection:
        flash('Database connection error.', 'danger')
        return redirect(url_for('clients'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if request.method == 'POST':
            name = request.form.get('name')
            mobile = request.form.get('mobile')
            email = request.form.get('email')
            address = request.form.get('address')
            
            if not name or not mobile:
                flash('Name and mobile are required.', 'danger')
                return redirect(url_for('edit_client', client_id=client_id))
            
            # Update client
            cursor.execute("""
                UPDATE clients 
                SET name = %s, mobile = %s, email = %s, address = %s, updated_at = NOW()
                WHERE id = %s
            """, (name, mobile, email, address, client_id))
            
            connection.commit()
            flash('Client updated successfully!', 'success')
            return redirect(url_for('client_details', client_id=client_id))
        
        # GET request - show edit form
        cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        client = cursor.fetchone()
        
        if not client:
            flash('Client not found.', 'danger')
            return redirect(url_for('clients'))
        
        return render_template('clients/edit.html', client=client)
        
    except Error as e:
        logger.error(f"Edit client error: {e}")
        flash('Error updating client.', 'danger')
        return redirect(url_for('clients'))
    finally:
        cursor.close()
        connection.close()

@app.route('/api/clients/analytics')
@login_required
def api_client_analytics():
    """API endpoint for client analytics data"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get client growth over time (last 12 months)
        cursor.execute("""
            SELECT 
                YEAR(created_at) as year,
                MONTH(created_at) as month,
                COUNT(*) as new_clients
            FROM clients
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY YEAR(created_at), MONTH(created_at)
            ORDER BY year, month
        """)
        client_growth = cursor.fetchall()
        
        # Get client distribution by order frequency
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN order_count = 0 THEN 'No Orders'
                    WHEN order_count BETWEEN 1 AND 5 THEN '1-5 Orders'
                    WHEN order_count BETWEEN 6 AND 15 THEN '6-15 Orders'
                    WHEN order_count BETWEEN 16 AND 30 THEN '16-30 Orders'
                    ELSE '30+ Orders'
                END as frequency_range,
                COUNT(*) as client_count
            FROM (
                SELECT c.id, COUNT(o.id) as order_count
                FROM clients c
                LEFT JOIN orders o ON c.id = o.client_id
                GROUP BY c.id
            ) as client_orders
            GROUP BY frequency_range
        """)
        frequency_distribution = cursor.fetchall()
        
        # Get top spending clients
        cursor.execute("""
            SELECT c.name, c.mobile, COALESCE(SUM(o.total_amount), 0) as total_spent
            FROM clients c
            LEFT JOIN orders o ON c.id = o.client_id
            GROUP BY c.id, c.name, c.mobile
            ORDER BY total_spent DESC
            LIMIT 10
        """)
        top_spenders = cursor.fetchall()
        
        analytics_data = {
            'client_growth': client_growth,
            'frequency_distribution': frequency_distribution,
            'top_spenders': top_spenders
        }
        
        return jsonify(analytics_data)
        
    except Error as e:
        logger.error(f"Client analytics API error: {e}")
        return jsonify({'error': 'Database error'})
    finally:
        cursor.close()
        connection.close()

# API routes for AJAX functionality
@app.route('/api/menu_items')
@login_required
def api_menu_items():
    """API endpoint to get menu items for cart functionality"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT mi.*, mc.name as category_name 
            FROM menu_items mi
            LEFT JOIN menu_categories mc ON mi.category_id = mc.id
            WHERE mi.is_available = TRUE
            ORDER BY mc.name, mi.name
        """)
        menu_items = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for item in menu_items:
            item['price'] = float(item['price'])
        
        return jsonify({'success': True, 'menu_items': menu_items})
        
    except Error as e:
        logger.error(f"API menu items error: {e}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/api/customers/search')
@login_required
def api_customer_search():
    """API endpoint to search customers for autocomplete"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    connection = get_db_connection()
    if not connection:
        return jsonify([])
    
    try:
        cursor = connection.cursor(dictionary=True)
        search_pattern = f"%{query}%"
        
        # Search in clients table first
        cursor.execute("""
            SELECT DISTINCT id, name, mobile, email, address
            FROM clients 
            WHERE name LIKE %s OR mobile LIKE %s OR (email IS NOT NULL AND email LIKE %s)
            ORDER BY name
            LIMIT 10
        """, (search_pattern, search_pattern, search_pattern))
        
        clients = cursor.fetchall()
        
        # If no clients found, search in orders for unique customer combinations
        if not clients:
            cursor.execute("""
                SELECT DISTINCT 
                    NULL as id, 
                    client_name as name, 
                    client_mobile as mobile,
                    NULL as email,
                    NULL as address
                FROM orders 
                WHERE client_name LIKE %s OR client_mobile LIKE %s
                ORDER BY client_name
                LIMIT 10
            """, (search_pattern, search_pattern))
            
            clients = cursor.fetchall()
        
        return jsonify(clients)
        
    except Error as e:
        logger.error(f"Customer search API error: {e}")
        return jsonify([])
    finally:
        cursor.close()
        connection.close()

@app.route('/api/check-username')
@login_required
def check_username():
    """API endpoint to check if username is available"""
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({'available': False, 'message': 'Username is required'})
    
    if len(username) < 3:
        return jsonify({'available': False, 'message': 'Username must be at least 3 characters'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'available': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        
        if cursor.fetchone():
            return jsonify({'available': False, 'message': 'Username is already taken'})
        else:
            return jsonify({'available': True, 'message': 'Username is available'})
            
    except Error as e:
        logger.error(f"Check username API error: {e}")
        return jsonify({'available': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/api/check-email')
@login_required  
def check_email():
    """API endpoint to check if email is available"""
    email = request.args.get('email', '').strip()
    
    if not email:
        return jsonify({'available': False, 'message': 'Email is required'})
    
    if '@' not in email:
        return jsonify({'available': False, 'message': 'Invalid email format'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'available': False, 'message': 'Database connection error'})
    
    try:
        cursor = connection.cursor()
        # Check if email column exists, if not we'll skip this check
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'email'
        """, (DB_CONFIG['database'],))
        
        if cursor.fetchone():
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({'available': False, 'message': 'Email is already registered'})
            else:
                return jsonify({'available': True, 'message': 'Email is available'})
        else:
            # Email column doesn't exist, so it's always available
            return jsonify({'available': True, 'message': 'Email is available'})
            
    except Error as e:
        logger.error(f"Check email API error: {e}")
        return jsonify({'available': False, 'message': 'Database error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/api/get-user-details')
@login_required  
def get_user_details():
    """API endpoint to get user details for modal display"""
    user_id = request.args.get('id', '').strip()
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, u.name as full_name, GROUP_CONCAT(b.name SEPARATOR ', ') as branch_names
            FROM users u
            LEFT JOIN user_branches ub ON u.id = ub.user_id
            LEFT JOIN branches b ON ub.branch_id = b.id
            WHERE u.id = %s
            GROUP BY u.id
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Convert datetime objects to strings for JSON serialization
        if user.get('created_at'):
            user['created_at'] = user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        if user.get('employed_date'):
            user['employed_date'] = user['employed_date'].strftime('%Y-%m-%d')
            
        return jsonify(user)
        
    except Error as e:
        logger.error(f"Get user details API error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        connection.close()

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>The requested page was not found.</p>
        <a href="/" style="color: #007bff;">Return to Home</a>
    </body>
    </html>
    ''', 404

@app.errorhandler(500)
def internal_error(error):
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>500 - Internal Server Error</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>500 - Internal Server Error</h1>
        <p>An internal server error occurred.</p>
        <a href="/" style="color: #007bff;">Return to Home</a>
    </body>
    </html>
    ''', 500

# Refund Management Routes
@app.route('/refunds')
@login_required
def refunds():
    """Display refund management page"""
    connection = None
    try:
        connection = get_db_connection()
        if not connection:
            flash(get_translations()['error_occurred'], 'error')
            return redirect(url_for('dashboard'))
            
        cursor = connection.cursor(dictionary=True)
        
        # Get all refunds with order and user details
        cursor.execute("""
            SELECT r.*, o.id as order_number, o.total_amount as order_total,
                   o.client_name as customer_name, req_u.name as requested_by_name,
                   app_u.name as approved_by_name, proc_u.name as processed_by_name
            FROM refunds r
            JOIN orders o ON r.order_id = o.id
            LEFT JOIN users req_u ON r.requested_by = req_u.id
            LEFT JOIN users app_u ON r.approved_by = app_u.id
            LEFT JOIN users proc_u ON r.processed_by = proc_u.id
            ORDER BY r.request_date DESC
        """)
        refunds = cursor.fetchall()
        
        return render_template('refunds/list.html', 
                               refunds=refunds,
                               t=get_translations(),
                               lang=session.get('language', 'en'))
        
    except Exception as e:
        logger.error(f"Error in refunds page: {e}")
        flash(get_translations()['error_occurred'], 'error')
        return redirect(url_for('dashboard'))
    finally:
        if connection:
            connection.close()

@app.route('/request_refund/<int:order_id>', methods=['GET', 'POST'])
@login_required
def request_refund(order_id):
    """Request a refund for an order"""
    connection = None
    if request.method == 'GET':
        # Display refund request form
        try:
            connection = get_db_connection()
            if not connection:
                flash(get_translations()['error_occurred'], 'error')
                return redirect(url_for('orders'))
                
            cursor = connection.cursor(dictionary=True)
            
            # Get order details
            cursor.execute("""
                SELECT o.*, o.client_name as customer_name
                FROM orders o
                WHERE o.id = %s
            """, (order_id,))
            order = cursor.fetchone()
            
            if not order:
                flash(get_translations()['order_not_found'], 'error')
                return redirect(url_for('orders'))
            
            return render_template('refunds/request.html', 
                                   order=order,
                                   t=get_translations(),
                                   lang=session.get('language', 'en'))
            
        except Exception as e:
            logger.error(f"Error displaying refund request form: {e}")
            flash(get_translations()['error_occurred'], 'error')
            return redirect(url_for('orders'))
        finally:
            if connection:
                connection.close()
    
    else:
        # Process refund request
        try:
            refund_type = request.form.get('refund_type')
            refund_amount = float(request.form.get('refund_amount', 0))
            refund_reason = request.form.get('refund_reason', '')
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Validate order exists and get details
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return jsonify({'success': False, 'message': get_translations()['order_not_found']})
            
            # Validate refund amount
            if refund_type == 'full':
                refund_amount = order['total_amount']
            elif refund_amount <= 0 or refund_amount > order['total_amount']:
                return jsonify({'success': False, 'message': get_translations()['invalid_refund_amount']})
            
            # Insert refund request
            cursor.execute("""
                INSERT INTO refunds (order_id, refund_amount, refund_type, refund_reason, 
                                   requested_by, request_date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (order_id, refund_amount, refund_type, refund_reason, session['user_id']))
            
            # Update order refund status
            cursor.execute("""
                UPDATE orders 
                SET refund_status = 'requested' 
                WHERE id = %s
            """, (order_id,))
            
            connection.commit()
            
            return jsonify({'success': True, 'message': get_translations()['refund_requested']})
            
        except Exception as e:
            logger.error(f"Error requesting refund: {e}")
            return jsonify({'success': False, 'message': get_translations()['error_occurred']})
        finally:
            if connection:
                connection.close()

@app.route('/approve_refund/<int:refund_id>', methods=['POST'])
@login_required
def approve_refund(refund_id):
    """Approve a refund request"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Update refund status to approved
        cursor.execute("""
            UPDATE refunds 
            SET refund_status = 'approved', approved_by = %s, approval_date = NOW()
            WHERE id = %s AND refund_status = 'pending'
        """, (session['user_id'], refund_id))
        
        if cursor.rowcount > 0:
            # Update order refund status
            cursor.execute("""
                UPDATE orders o
                JOIN refunds r ON o.id = r.order_id
                SET o.refund_status = 'approved'
                WHERE r.id = %s
            """, (refund_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': get_translations()['refund_approved']})
        else:
            return jsonify({'success': False, 'message': get_translations()['refund_not_found']})
            
    except Exception as e:
        logger.error(f"Error approving refund: {e}")
        return jsonify({'success': False, 'message': get_translations()['error_occurred']})
    finally:
        if connection:
            connection.close()

@app.route('/reject_refund/<int:refund_id>', methods=['POST'])
@login_required
def reject_refund(refund_id):
    """Reject a refund request"""
    try:
        notes = request.form.get('notes', '')
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Update refund status to rejected
        cursor.execute("""
            UPDATE refunds 
            SET refund_status = 'rejected', approved_by = %s, approval_date = NOW(), notes = %s
            WHERE id = %s AND refund_status = 'pending'
        """, (session['user_id'], notes, refund_id))
        
        if cursor.rowcount > 0:
            # Reset order refund status
            cursor.execute("""
                UPDATE orders o
                JOIN refunds r ON o.id = r.order_id
                SET o.refund_status = 'none'
                WHERE r.id = %s
            """, (refund_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': get_translations()['refund_rejected']})
        else:
            return jsonify({'success': False, 'message': get_translations()['refund_not_found']})
            
    except Exception as e:
        logger.error(f"Error rejecting refund: {e}")
        return jsonify({'success': False, 'message': get_translations()['error_occurred']})
    finally:
        if connection:
            connection.close()

@app.route('/process_refund/<int:refund_id>', methods=['POST'])
@login_required
def process_refund(refund_id):
    """Process an approved refund"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get refund details
        cursor.execute("""
            SELECT r.*, o.total_amount as order_total
            FROM refunds r
            JOIN orders o ON r.order_id = o.id
            WHERE r.id = %s AND r.refund_status = 'approved'
        """, (refund_id,))
        refund = cursor.fetchone()
        
        if not refund:
            return jsonify({'success': False, 'message': get_translations()['refund_not_found']})
        
        # Update refund status to processed
        cursor.execute("""
            UPDATE refunds 
            SET refund_status = 'processed', processed_by = %s, processed_date = NOW()
            WHERE id = %s
        """, (session['user_id'], refund_id))
        
        # Update order status based on refund type
        if refund['refund_type'] == 'full' or refund['refund_amount'] >= refund['order_total']:
            new_status = 'refunded'
        else:
            new_status = 'partially_refunded'
        
        cursor.execute("""
            UPDATE orders 
            SET status = %s, refund_status = 'processed'
            WHERE id = %s
        """, (new_status, refund['order_id']))
        
        connection.commit()
        return jsonify({'success': True, 'message': get_translations()['refund_processed']})
        
    except Exception as e:
        logger.error(f"Error processing refund: {e}")
        return jsonify({'success': False, 'message': get_translations()['error_occurred']})
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    init_database()
    
    # SSL Configuration
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    # Check if SSL certificates exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        
        print("🔒 Starting Flask app with HTTPS support...")
        print("🌐 Access the application at: https://localhost:4009")
        print("⚠️  Note: You may see a security warning due to self-signed certificate")
        
        # Run with SSL
        app.run(debug=True, host='0.0.0.0', port=4009, ssl_context=context)
    else:
        print("⚠️  SSL certificates not found. Running HTTP server...")
        print("🌐 Access the application at: http://localhost:4009")
        print("💡 To enable HTTPS, ensure cert.pem and key.pem are in the project directory")
        
        # Run without SSL
        app.run(debug=True, host='0.0.0.0', port=4009)
