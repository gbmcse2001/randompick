import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "gbmcse2001"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global variable to store student names
student_names = []

@app.route("/", methods=["GET", "POST"])
def index():
    global student_names
    student_names = []  # Reset list

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        print(f"Received file: {file.filename}")

        if file and file.filename.endswith(".txt"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Read file and store names
            with open(filepath, "r", encoding="utf-8") as f:
                student_names = [line.strip() for line in f.readlines() if line.strip()]

    return render_template("index.html", students=student_names, selected_student=None)


@app.route("/pick", methods=["POST"])
def pick_student():
    if student_names:
        selected_student = random.choice(student_names)
    else:
        selected_student = "No students available. Upload a file first."

    return render_template("index.html", students=student_names, selected_student=selected_student)

@app.route("/reset", methods=["POST"])
def reset():
    global student_names
    student_names = []  # Clear the list
    return redirect(url_for("index"))  # Redirect back to the homepage

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
