from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import check_admin_login, check_customer_login, create_admin, create_customer

app = Flask(__name__)
app.secret_key = "AB_Is_Officially_Out"

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
            flash("Customer Login successful!", "success")
            return redirect(url_for("customer_dashboard"))
        else:
            flash("Invalid customer email or password", "danger")

    return render_template("login_customer.html")

# Admin Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_id" in session:
        return f"Welcome, {session['admin_name']}! <a href='/logout_admin'>Logout</a>"
    return redirect(url_for("login_admin"))

# Customer Dashboard
@app.route("/customer_dashboard")
def customer_dashboard():
    if "customer_id" in session:
        return f"Welcome, {session['customer_name']}! <a href='/logout'>Logout</a>"
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
      
        message = create_customer(firstname, lastname, email, password, address)
        flash(message, "success" if "successfully" in message else "danger")
        
        if "successfully" in message:
            return redirect(url_for("login_customer"))

    return render_template("register_customer.html")

if __name__ == "__main__":
    app.run(debug=True)
