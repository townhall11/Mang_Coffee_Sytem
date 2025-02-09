from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import check_admin_login, check_customer_login, create_admin, create_customer
from db import get_db_connection  # ✅ Import database connection from db.py
from werkzeug.security import generate_password_hash
from flask import request, jsonify
from werkzeug.utils import secure_filename
import pymysql  # Ensure you're using the right MySQL connector
import os


app = Flask(__name__)

#secretkey
app.secret_key = "AB_Is_Officially_Out"

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure directory exists


# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Admin Login

@app.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        admin = check_admin_login(email, password)
        if admin:
            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["firstname"]
            session["ad_lastname"] = admin["lastname"]
          

            flash("Admin Login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin email or password", "danger")

    return render_template("login_admin.html")


# Customer Login
@app.route("/login_customer", methods=["GET", "POST"])
def login_customer():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        customer = check_customer_login(email, password)
        if customer:
            session["customer_id"] = customer["id"]
            session["customer_name"] = customer["firstname"]
            session["cus_lastname"] = customer["lastname"]

            flash("Customer Login successful!", "success")
            return redirect(url_for("customer_dashboard"))
        else:
            flash("Invalid customer email or password", "danger")

    return render_template("login_customer.html")

# Admin Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_id" in session:
        return render_template("dashboard_admin.html", admin_name=session["admin_name"])
    return redirect(url_for("login_admin"))

# Customer Dashboard
@app.route("/customer_dashboard")
def customer_dashboard():
    if "customer_id" in session:
        return render_template("dashboard_customer.html", customer_name=session["customer_name"])
    return redirect(url_for("login_customer"))

# client Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login_customer"))

# admin Logout
@app.route("/logout_admin")
def logout_admin():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login_admin"))


# Register Admin
@app.route("/register_admin", methods=["GET", "POST"])
def register_admin():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        message = create_admin(firstname, lastname, email, password, role)
        flash(message, "success" if "successfully" in message else "danger")
        
        if "successfully" in message:
            return redirect(url_for("login_admin"))

    return render_template("register_admin.html")

# Register Customer
@app.route("/register_customer", methods=["GET", "POST"])
def register_customer():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        mobilenumber = request.form["mobilenumber"]

        message = create_customer(firstname, lastname, email, password, address, mobilenumber)
        flash(message, "success" if "successfully" in message else "danger")
        
        if "successfully" in message:
            return redirect(url_for("login_customer"))

    return render_template("register_customer.html")

# View All Admin Accounts
@app.route("/admin_accounts")
def admin_accounts():
    if "admin_id" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("login_admin"))

    # Fetch all admin accounts from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin")
    all_acc = cursor.fetchall()
    conn.close()

    return render_template("admin_acc.html", all_acc=all_acc, admin_name=session["admin_name"])

# Edit Admin Accounts
@app.route("/edit_admin", methods=["POST"])
def edit_admin():
    try:
        admin_id = request.form.get("admin_id")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        new_password = request.form.get("new_password")

        # Debugging: Print received data
        print(f"Admin ID: {admin_id}, Firstname: {firstname}, Lastname: {lastname}, Email: {email}, Password: {new_password}")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if new_password is provided
        if new_password and new_password.strip():
            hashed_password = generate_password_hash(new_password)
            cursor.execute("""
                UPDATE admin 
                SET firstname = %s, lastname = %s, email = %s, password = %s
                WHERE id = %s
            """, (firstname, lastname, email, hashed_password, admin_id))
        else:
            cursor.execute("""
                UPDATE admin 
                SET firstname = %s, lastname = %s, email = %s 
                WHERE id = %s
            """, (firstname, lastname, email, admin_id))

        conn.commit()

        # Debugging: Check if update was successful
        if cursor.rowcount > 0:
            print("Update successful")
            response = {"success": True, "message": "Admin details updated successfully!"}
        else:
            print("No rows affected")
            response = {"success": False, "message": "No changes detected or incorrect admin ID."}

    except Exception as e:
        print("Error:", e)
        response = {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()

    return jsonify(response)


# Delete Admin Accounts
@app.route("/delete_admin/<int:admin_id>", methods=["POST"])
def delete_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin WHERE id = %s", (admin_id,))
    conn.commit()
    conn.close()

    flash("Admin account deleted successfully!", "success")
    return redirect(url_for("admin_accounts"))


# View All Customer Accounts
@app.route("/customer_account")
def customer_account():
    if "admin_id" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("login_admin"))

    # Fetch all customers accounts from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    all_acc = cursor.fetchall()
    conn.close()

    return render_template("customer_acc.html", all_acc=all_acc,admin_name=session["admin_name"])

# Edit Customer Accounts
@app.route("/edit_customer", methods=["POST"])
def edit_customer():
    try:
        customer_id = request.form.get("customer_id")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        mobilenumber = request.form.get("mobilenumber")
        address = request.form.get("address")
        new_password = request.form.get("new_password")

        # Debugging: Print received data
        print(f"Customer ID: {customer_id}, Firstname: {firstname}, Lastname: {lastname}, Email: {email}, Mobilenumber: {mobilenumber}, Address: {address}, Password: {new_password}")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if new_password is provided
        if new_password and new_password.strip():
            hashed_password = generate_password_hash(new_password)
            cursor.execute("""
                UPDATE customers 
                SET firstname = %s, lastname = %s, email = %s, mobilenumber = %s, address = %s, password = %s
                WHERE id = %s
            """, (firstname, lastname, email, mobilenumber, address, hashed_password, customer_id))
        else:
            cursor.execute("""
                UPDATE customers 
                SET firstname = %s, lastname = %s, email = %s 
                WHERE id = %s
            """, (firstname, lastname, email, customer_id))

        conn.commit()

        # Debugging: Check if update was successful
        if cursor.rowcount > 0:
            print("Update successful")
            response = {"success": True, "message": "Customer details updated successfully!"}
        else:
            print("No rows affected")
            response = {"success": False, "message": "No changes detected or incorrect Customer ID."}

    except Exception as e:
        print("Error:", e)
        response = {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()

    return jsonify(response)

# Delete Customer Accounts
@app.route("/delete_customer/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()
        flash("Customer account deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting customer: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("customer_account"))


# View All Categories
@app.route("/view_category")
def view_category():
    if "admin_id" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("login_admin"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM category")
    all_acc = cursor.fetchall()
    conn.close()

    return render_template("category.html", all_acc=all_acc, admin_name=session["admin_name"])

# Add Category
@app.route("/add_category", methods=["POST"])
def add_category():
    category_name = request.form.get("categoryname", "").strip()

    if not category_name:
        return jsonify({"success": False, "message": "Category name cannot be empty!"})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if category already exists
        cursor.execute("SELECT id FROM category WHERE categoryname = %s", (category_name,))
        existing_category = cursor.fetchone()

        if existing_category:
            return jsonify({"success": False, "message": "Category already exists!"})

        # Insert new category
        cursor.execute("INSERT INTO category (categoryname) VALUES (%s)", (category_name,))
        conn.commit()
        new_category_id = cursor.lastrowid  # Get the inserted ID
        
        return jsonify({"success": True, "message": "Category added successfully!", "id": new_category_id})

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

    finally:
        cursor.close()
        conn.close()

# Edit Category
@app.route("/edit_category", methods=["POST"])
def edit_category():
    try:
        category_id = request.form.get("category_id")
        categoryname = request.form.get("categoryname")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE category SET categoryname = %s WHERE id = %s", (categoryname, category_id))
        conn.commit()

        if cursor.rowcount > 0:
            response = {"success": True, "message": "Category updated successfully!"}
        else:
            response = {"success": False, "message": "No changes made or invalid category ID."}

    except Exception as e:
        response = {"success": False, "message": str(e)}

    finally:
        cursor.close()
        conn.close()

    return jsonify(response)

# Delete Category
@app.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM category WHERE id = %s", (category_id,))
        conn.commit()
        flash("Category deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting category: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("view_category"))

# View all products
@app.route('/products')
def products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries

    # Fetch products along with category names
    cursor.execute("""
        SELECT products.id, products.prod_name, products.prod_desc, products.stock, 
               products.prod_price, products.prod_img, category.categoryname AS category_name
        FROM products
        JOIN category ON products.category = category.id
    """)
    products = cursor.fetchall()

    # Fetch all categories
    cursor.execute("SELECT id, categoryname FROM category")
    categories = cursor.fetchall()
   
    conn.close()
    
    return render_template('products.html', products=products,categories=categories, admin_name=session["admin_name"])

# Add Product
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        category = request.form.get('category')
        prod_name = request.form.get('prod_name')
        prod_desc = request.form.get('prod_desc')
        prod_price = request.form.get('prod_price')
        stock = request.form.get('stock')
        file = request.files.get('prod_img')

        # Validate category
        if not category or not category.isdigit():
            return jsonify({'success': False, 'message': 'Invalid category selection'}), 400
        category = int(category)

        # Convert price and stock to correct types
        try:
            prod_price = float(prod_price)
            stock = int(stock)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid price or stock format'}), 400

        # Handle file upload
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = "logo_mangjuan.png"

        # Save product to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (category, prod_name, prod_img, prod_desc, prod_price, stock) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (category, prod_name, filename, prod_desc, prod_price, stock))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Product added successfully!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': 'Error adding product', 'error': str(e)}), 500


# Edit Product
@app.route('/edit_product', methods=['POST'])
def edit_product():
    try:
        product_id = request.form.get('product_id')
        category = request.form.get('category')
        prod_name = request.form.get('prod_name')
        prod_desc = request.form.get('prod_desc')
        prod_price = request.form.get('prod_price')
        stock = request.form.get('stock')
        file = request.files.get('prod_img')

        # Ensure category is an integer
        if category is not None and category.isdigit():
            category = int(category)
        else:
            return jsonify({'success': False, 'message': 'Invalid category selection'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if new image was uploaded
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            cursor.execute("""
                UPDATE products SET category=%s, prod_name=%s, prod_img=%s, prod_desc=%s, prod_price=%s, stock=%s
                WHERE id=%s
            """, (category, prod_name, filename, prod_desc, prod_price, stock, product_id))
        else:
            cursor.execute("""
                UPDATE products SET category=%s, prod_name=%s, prod_desc=%s, prod_price=%s, stock=%s
                WHERE id=%s
            """, (category, prod_name, prod_desc, prod_price, stock, product_id))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Product updated successfully!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': 'Error updating product', 'error': str(e)}), 500



# Delete Product
@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Product deleted successfully!'})


#Add Stock Product
@app.route('/update_stock', methods=['POST'])
def update_stock():
    try:
        data = request.json
        product_id = data.get("product_id")
        new_stock = data.get("new_stock")

        if not product_id or not new_stock:
            return jsonify({"success": False, "message": "Invalid product ID or stock value"}), 400

        try:
            new_stock = int(new_stock)
            if new_stock < 1:
                return jsonify({"success": False, "message": "Stock must be at least 1"}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Invalid stock value"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if product exists
        cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"success": False, "message": "Product not found"}), 404

        # Update stock
        cursor.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (new_stock, product_id))
        conn.commit()

        # Get updated stock value
        cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
        updated_stock = cursor.fetchone()[0]

        conn.close()

        return jsonify({"success": True, "updated_stock": updated_stock})

    except Exception as e:
        print("Error:", str(e))  # Log the error to console
        return jsonify({"success": False, "message": "Something went wrong while updating stock.", "error": str(e)}), 500


# View All Manage Order
@app.route('/ManageOrder')
def ManageOrder():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor

    cursor.execute("SELECT * FROM products")  # Fetch all products
    order_products = cursor.fetchall()  # Use a different variable name

    cursor.close()
    conn.close()

    return render_template("add_to_cart.html", order_products=order_products, admin_name=session.get("admin_name", "Admin"))




# Fetch products from the database
@app.route('/get_products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE stock > 0")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

#Check Stock
@app.route('/check_stock/<int:product_id>/<int:quantity>', methods=['GET'])
def check_stock(product_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    if product['stock'] < quantity:
        return jsonify({"success": False, "remaining": product['stock'], "message": "Not enough stock"}), 400

    return jsonify({"success": True, "remaining": product['stock']})


#Show Customer
@app.route("/get_customers")
def get_customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # ✅ Ensure dictionary format

        cursor.execute("SELECT id, firstname, lastname FROM customers")  # ✅ Fetch only needed columns
        customers = cursor.fetchall()
        conn.close()

        print("Customers data:", customers)  # ✅ Debugging: Check what is being returned
        return jsonify(customers)

    except Exception as e:
        print("Database error:", str(e))  
        return jsonify({"error": "Database error"}), 500



# Place an order
@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    customer_id = data.get('customer_id')  # Get customer_id
    orders = data.get('orders', [])
    payment_method = data.get('payment')
    delivery_option = data.get('delivery')

    if not customer_id:
        return jsonify({"success": False, "message": "Customer selection is required."}), 400

    if not orders:
        return jsonify({"success": False, "message": "No items in cart"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    for order in orders:
        product_id = order.get('product_id')
        quantity = int(order.get('quantity', 0))

        cursor.execute("SELECT stock, prod_price FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        if not product or int(product['stock']) < quantity:
            return jsonify({"success": False, "message": "Not enough stock"}), 400

        total_price = float(product['prod_price']) * quantity

        cursor.execute("""
            INSERT INTO orders (customer_id, product_id, quantity, total_price, payments, delivery)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (customer_id, product_id, quantity, total_price, payment_method, delivery_option))

        new_stock = int(product['stock']) - quantity
        cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, product_id))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Order placed successfully!"})




if __name__ == '__main__':
    app.run(debug=True)
