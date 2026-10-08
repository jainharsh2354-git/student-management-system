import re
import sqlite3
from flask import Flask, jsonify, request, g, send_from_directory

DB = "students.db"
app = Flask(__name__, static_folder="static")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            class_name TEXT NOT NULL,
            marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100),
            contact TEXT NOT NULL)""")


def validate(d):
    errors = []
    name = str(d.get("name", "")).strip()
    roll = str(d.get("roll_no", "")).strip()
    cls = str(d.get("class_name", "")).strip()
    contact = str(d.get("contact", "")).strip()
    if not name:
        errors.append("Name is required.")
    if not roll:
        errors.append("Roll number is required.")
    if not cls:
        errors.append("Class is required.")
    try:
        marks = float(d.get("marks"))
        if not 0 <= marks <= 100:
            errors.append("Marks must be between 0 and 100.")
    except (TypeError, ValueError):
        marks = None
        errors.append("Marks must be a number.")
    if not re.fullmatch(r"\d{10}", contact):
        errors.append("Contact must be a 10-digit number.")
    return errors, (name, roll, cls, marks, contact)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/students")
def list_students():
    q = request.args.get("q", "").strip()
    db = get_db()
    if q:
        like = f"%{q}%"
        rows = db.execute("SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ? ORDER BY id DESC", (like, like)).fetchall()
    else:
        rows = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/students")
def add_student():
    errors, v = validate(request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400
    db = get_db()
    try:
        cur = db.execute("INSERT INTO students (name, roll_no, class_name, marks, contact) VALUES (?,?,?,?,?)", v)
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"errors": ["Roll number already exists."]}), 409
    return jsonify({"id": cur.lastrowid, "message": "Student added."}), 201


@app.put("/api/students/<int:sid>")
def update_student(sid):
    errors, v = validate(request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400
    db = get_db()
    try:
        cur = db.execute("UPDATE students SET name=?, roll_no=?, class_name=?, marks=?, contact=? WHERE id=?", (*v, sid))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"errors": ["Roll number already exists."]}), 409
    if cur.rowcount == 0:
        return jsonify({"errors": ["Student not found."]}), 404
    return jsonify({"message": "Student updated."})


@app.delete("/api/students/<int:sid>")
def delete_student(sid):
    db = get_db()
    cur = db.execute("DELETE FROM students WHERE id=?", (sid,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"errors": ["Student not found."]}), 404
    return jsonify({"message": "Student deleted."})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
