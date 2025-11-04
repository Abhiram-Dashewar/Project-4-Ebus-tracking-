from flask import Flask, render_template, redirect, url_for, request, g, flash, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production
DATABASE = "userdata.db"

# -------------------- DATABASE SETUP --------------------

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                bus_number TEXT NOT NULL,
                bus_type TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                start_location TEXT NOT NULL,
                end_location TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        """)   
        db.commit()
        
        # Check if 'role' column exists; if not, add it
        cursor = db.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'role' not in columns:
            db.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
            db.commit()

@app.route('/')
def home():
    db = get_db()

    # Get unique start and end locations (no duplicates)
    unique_starts = [row["start_location"] for row in db.execute("SELECT DISTINCT start_location FROM drivers").fetchall()]
    unique_ends = [row["end_location"] for row in db.execute("SELECT DISTINCT end_location FROM drivers").fetchall()]

    # Fetch all drivers (for full list or display)
    drivers = db.execute("SELECT * FROM drivers").fetchall()

    return render_template('home.html', drivers=drivers, unique_starts=unique_starts, unique_ends=unique_ends)


@app.route("/register", methods=["POST"])
def register():
    username = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    try:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (username, email, password, role)
                VALUES (?, ?, ?, ?)
            """, (username, email, password, role))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            if role == "user":
                return redirect(url_for('user'))
    except sqlite3.IntegrityError:
        flash("Email already registered. Try logging in.", "danger")
        return redirect(url_for("home"))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if email == "admin@ebus.com" and password == 'password':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))
    
@app.route("/admin")
def admin():
    db = get_db()
    drivers = db.execute("SELECT * FROM drivers").fetchall()
    return render_template("admin.html", drivers=drivers)

@app.route("/add_driver", methods=["POST"])
def add_driver():
    name = request.form["name"]
    bus_number = request.form["bus_number"]
    bus_type = request.form["bus_type"]
    capacity = request.form["capacity"]
    start_location = request.form["start_location"]
    end_location = request.form["end_location"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]

    db = get_db()
    db.execute("""
        INSERT INTO drivers (name, bus_number, bus_type, capacity, start_location, end_location, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, bus_number, bus_type, capacity, start_location, end_location, start_time, end_time))
    db.commit()

    flash("Driver added successfully!", "success")
    return redirect(url_for("admin"))

# -------------------- USER PAGE --------------------
@app.route("/user")
def user():
    db = get_db()
    drivers = db.execute("SELECT * FROM drivers").fetchall()

    # Get the most recently registered user
    user = db.execute("SELECT username, email FROM users ORDER BY id DESC LIMIT 1").fetchone()

    return render_template("user.html", drivers=drivers, user_info=user)


@app.route("/user_email/<email>")
def user_by_email(email):
    db = get_db()
    drivers = db.execute("SELECT * FROM drivers").fetchall()
    user = db.execute("SELECT username, email FROM users WHERE email = ?", (email,)).fetchone()
    return render_template("user.html", drivers=drivers, user_info=user)



@app.route("/search_buses", methods=["POST"])
def search_buses():
    data = request.get_json()
    start = data.get("start_location")
    end = data.get("end_location")
    bus_type = data.get("bus_type")

    db = get_db()
    buses = db.execute("""
        SELECT * FROM drivers
        WHERE start_location = ? AND end_location = ? AND bus_type = ?
    """, (start, end, bus_type)).fetchall()

    results = [dict(row) for row in buses]
    return {"buses": results}

@app.route("/track_buses", methods=["POST"])
def track_buses():
    data = request.get_json()
    start_location = data.get("start_location")
    end_location = data.get("end_location")

    db = get_db()
    cursor = db.cursor()

    # Get current time in HH:MM format
    current_time = datetime.now().strftime("%H:%M")

    # Fetch only buses whose start_time is greater than or equal to current time
    buses = cursor.execute("""
        SELECT * FROM drivers
        WHERE start_location = ? 
          AND end_location = ? 
          AND start_time >= ?
        ORDER BY start_time ASC
    """, (start_location, end_location, current_time)).fetchall()

    result = [dict(row) for row in buses]
    return jsonify({"buses": result})



@app.route("/logout")
def logout():
    return redirect(url_for('home'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
