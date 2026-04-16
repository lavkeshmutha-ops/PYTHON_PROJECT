

import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Import our custom modules
from solver import solve_math_problem
from image_reader import extract_math_from_image
from formatter import format_result

# --- Flask App Setup ---
app = Flask(__name__)

# Folder where uploaded images will be stored temporarily
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed image file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp"}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
   
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    
    math_expression = ""
    source = ""

    # --- Handle Image Upload ---
    if "math_image" in request.files and request.files["math_image"].filename != "":
        image_file = request.files["math_image"]

        if allowed_file(image_file.filename):
            # Save the image securely to the uploads folder
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)

            # Extract math text from the image using OCR
            math_expression = extract_math_from_image(image_path)
            source = "image"

            # Clean up: remove the uploaded file after reading it
            if os.path.exists(image_path):
                os.remove(image_path)
        else:
            return render_template("index.html", error="Invalid file type. Please upload a PNG or JPG image.")

    # --- Handle Text Input ---
    elif "math_text" in request.form and request.form["math_text"].strip():
        math_expression = request.form["math_text"].strip()
        source = "text"

    else:
        # Neither input was provided
        return render_template("index.html", error="Please enter a math problem or upload an image.")

    # --- Solve the Math Problem ---
    if not math_expression:
        return render_template("index.html", error="Could not read any math expression. Try again.")

    # Solve the problem and get result with steps
    result_data = solve_math_problem(math_expression)

    # Format the result for display
    formatted = format_result(result_data, math_expression, source)

    return render_template("result.html", data=formatted)


@app.route("/back")
def back():
    """Go back to the home page."""
    return redirect(url_for("index"))


# --- Run the App ---
if __name__ == "__main__":
    print("Math Solver is running at: http://127.0.0.1:5000")
    app.run(debug=True)