import os
from flask import Flask, request, render_template
import fitz  # PyMuPDF

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# アップロードフォルダがなければ作成
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(temp_path)

            # PDF からテキストを抽出
            text = extract_text_from_pdf(temp_path)
            return render_template("index.html", text=text)

    return render_template("index.html")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n\n"
    return text

if __name__ == "__main__":
    app.run(debug=True)
