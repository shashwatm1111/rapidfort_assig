import os
from flask import Flask, request, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
from fpdf import FPDF
from docx import Document  # Necessary for handling DOCX files
import pikepdf


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
            protected_pdf_filename = filename.rsplit(".", 1)[0] + "_protected.pdf"
            protected_pdf_filepath = os.path.join(app.config["UPLOAD_FOLDER"], protected_pdf_filename)

            # Get password from the form (optional)
            password = request.form.get("password")

            try:
                # Convert DOCX to PDF
                convert_docx_to_pdf(filepath, pdf_filepath)

                # Apply password protection if password is provided
                if password:
                    add_password_to_pdf(pdf_filepath, protected_pdf_filepath, password)
                    return render_template("download.html", pdf_filename=protected_pdf_filename)
                else:
                    return render_template("download.html", pdf_filename=pdf_filename)

            except Exception as e:
                return f"Error during processing: {str(e)}", 500

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

    # Adding UTF-8 support by setting an encoding
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for paragraph in doc.paragraphs:
        pdf.multi_cell(0, 10, paragraph.text.encode('latin-1', 'replace').decode('latin-1'))

    pdf.output(output_path)


# Function to add password protection to the PDF
def add_password_to_pdf(input_pdf_path, output_pdf_path, password):
    try:
        # Open the original PDF with pikepdf
        with pikepdf.open(input_pdf_path) as pdf:
            # Set the password protection
            pdf.save(output_pdf_path, encryption=pikepdf.Encryption(owner=password, user=password, R=4))
    except Exception as e:
        raise Exception(f"Error during password protection: {str(e)}")


# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
