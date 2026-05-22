"""
Task 1: CLI-Based Application → Flask Web App
Intern: Nikhil Singh | Application: NJ-KABGLTK
Student Manager with full CRUD operations.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "nikhil_nj_kabgltk"

DATA_FILE = "students_data.json"

# ─────────────────────────────────────────
#  Data Helpers
# ─────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# ─────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────

@app.route("/")
def index():
    students = load_data()
    query = request.args.get("q", "").strip().lower()
    if query:
        students = [s for s in students if query in s["name"].lower() or query == str(s["id"])]
    return render_template("index.html", students=students, query=query)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name   = request.form.get("name", "").strip()
        age    = request.form.get("age", "").strip()
        grade  = request.form.get("grade", "").strip()
        course = request.form.get("course", "").strip()

        if not all([name, age, grade, course]):
            flash("All fields are required!", "error")
            return redirect(url_for("add_student"))

        students = load_data()
        new_id = max((s["id"] for s in students), default=0) + 1
        students.append({"id": new_id, "name": name, "age": age, "grade": grade, "course": course})
        save_data(students)
        flash(f"Student '{name}' added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/edit/<int:sid>", methods=["GET", "POST"])
def edit_student(sid):
    students = load_data()
    student = next((s for s in students if s["id"] == sid), None)
    if not student:
        flash("Student not found!", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        student["name"]   = request.form.get("name", student["name"]).strip()
        student["age"]    = request.form.get("age", student["age"]).strip()
        student["grade"]  = request.form.get("grade", student["grade"]).strip()
        student["course"] = request.form.get("course", student["course"]).strip()
        save_data(students)
        flash("Student updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", student=student)

@app.route("/delete/<int:sid>")
def delete_student(sid):
    students = load_data()
    students = [s for s in students if s["id"] != sid]
    save_data(students)
    flash("Student deleted successfully!", "success")
    return redirect(url_for("index"))

@app.route("/summary")
def summary():
    students = load_data()
    courses = {}
    for s in students:
        courses[s["course"]] = courses.get(s["course"], 0) + 1
    return render_template("summary.html", students=students, courses=courses)

# ─────────────────────────────────────────
#  Run
# ─────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
