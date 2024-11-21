import os
from flask import Flask, request, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
from docx import Document
from fpdf import FPDF

# Initialize Flask app
app = Flask(__name__)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"docx"}

# Helper function to check allowed files
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Route: Home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Check if file is present in the request
        if "file" not in request.files:
            return "No file part in the request", 400

        file = request.files["file"]

        # Check if the file is selected
        if file.filename == "":
            return "No file selected", 400

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Convert DOCX to PDF
            pdf_filename = filename.rsplit(".", 1)[0] + ".pdf"
            pdf_filepath = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)

            try:
                convert_docx_to_pdf(filepath, pdf_filepath)
            except Exception as e:
                return f"Error during conversion: {str(e)}", 500

            return render_template(
                "download.html",
                pdf_filename=pdf_filename,
            )
        else:
            return "Invalid file type. Only .docx files are allowed.", 400

    return render_template("index.html")


# Route: Download PDF
@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    try:
        # Serve the file from the upload folder
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)


# Function to convert DOCX to PDF
def convert_docx_to_pdf(input_path, output_path):
    doc = Document(input_path)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for paragraph in doc.paragraphs:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, paragraph.text)

    pdf.output(output_path)


# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
