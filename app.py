from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["UPLOAD_FOLDER"] = "static/uploads"


# ---------------- DATABASE INIT ----------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            category TEXT,
            location_link TEXT,
            photo TEXT,
            status TEXT DEFAULT 'Open',
            upvotes INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    """)

    # Default admin
    try:
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )
    except:
        pass

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME ----------------

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM issues ORDER BY upvotes DESC")
    issues = c.fetchall()
    conn.close()
    return render_template("index.html", issues=issues)


# ---------------- REGISTER (AUTO LOGIN FIXED) ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "user")
            )
            conn.commit()

            # AUTO LOGIN AFTER REGISTER
            session["user"] = username
            session["role"] = "user"

            conn.close()
            return redirect("/")

        except:
            error = "Username already exists."

        conn.close()

    return render_template("register.html", error=error)


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            session["role"] = user[3]
            return redirect("/")
        else:
            error = "Invalid Credentials"

    return render_template("login.html", error=error)


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- REPORT ISSUE ----------------

@app.route("/report", methods=["GET", "POST"])
def report():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        location_link = request.form["location_link"]

        photo = request.files["photo"]
        filename = ""

        if photo and photo.filename != "":
            filename = photo.filename
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
            INSERT INTO issues (title, description, category, location_link, photo)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, category, location_link, filename))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("report.html")


# ---------------- UPVOTE ----------------

@app.route("/upvote/<int:id>", methods=["GET", "POST"])
def upvote(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE issues SET upvotes = upvotes + 1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# ---------------- UPDATE STATUS ----------------

@app.route("/update_status/<int:id>")
def update_status(id):
    if session.get("role") != "admin":
        return "Only admin can update status"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT status FROM issues WHERE id=?", (id,))
    current_status = c.fetchone()[0]

    if current_status == "Open":
        new_status = "In Progress"
    else:
        new_status = "Resolved"

    c.execute("UPDATE issues SET status=? WHERE id=?", (new_status, id))
    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- ANNOUNCEMENTS ----------------

@app.route("/announcements", methods=["GET", "POST"])
def announcements():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        if session.get("role") != "admin":
            return "Only admin can post announcements"

        title = request.form["title"]
        content = request.form["content"]

        c.execute(
            "INSERT INTO announcements (title, content) VALUES (?, ?)",
            (title, content)
        )
        conn.commit()

    c.execute("SELECT * FROM announcements")
    data = c.fetchall()
    conn.close()

    return render_template("announcements.html", announcements=data)


if __name__ == "__main__":
    app.run(debug=True)