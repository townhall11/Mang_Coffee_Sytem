import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="coffee_db"
    )

# Check if admin exists
def admin_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT 1 FROM admin WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result is not None

# Register Admin
def create_admin(firstname, lastname, email, password, role):
    if admin_exists(email):
        return "Admin already registered."

    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    query = "INSERT INTO admin (firstname, lastname, email, password, role) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, email, hashed_password, role))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return "Admin registered successfully."

# Check if customer exists
def customer_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT 1 FROM customers WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result is not None

# Register Customer
def create_customer(firstname, lastname, email, password, address):
    if customer_exists(email):
        return "Customer already registered."

    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    query = "INSERT INTO customers (firstname, lastname, email, password, address) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, email, hashed_password, address))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return "Customer registered successfully."

# Admin Login
def check_admin_login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM admin WHERE email = %s"
    cursor.execute(query, (email,))
    admin = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if admin and check_password_hash(admin["password"], password):
        return admin
    return None

# Customer Login
def check_customer_login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM customers WHERE email = %s"
    cursor.execute(query, (email,))
    customer = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if customer and check_password_hash(customer["password"], password):
        return customer
    return None
