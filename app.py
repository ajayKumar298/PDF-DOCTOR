from flask import Flask, render_template, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress_pdf():
    uploaded_file = request.files["pdf_file"]
    target_size_kb = request.form.get("target_size")
    if uploaded_file.filename == "":
        return "No selected file"
    filename = secure_filename(uploaded_file.filename)
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    output_path = os.path.join(COMPRESSED_FOLDER, f"compressed_{filename}")
    uploaded_file.save(input_path)

    # Ghostscript command for compression
    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    subprocess.run(command, check=True)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
