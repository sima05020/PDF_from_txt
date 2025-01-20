import os

import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


def extract_text_from_pdf(pdf_path):
    """PDF からテキストを抽出"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n\n"
    return text


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "ファイルがアップロードされていません"

        file = request.files["file"]
        if file.filename == "":
            return "ファイルが選択されていません"

        # 一時ファイルとして保存
        temp_path = os.path.join("uploads", file.filename)
        file.save(temp_path)

        # テキスト抽出
        extracted_text = extract_text_from_pdf(temp_path)

        # テキストファイルに保存
        output_path = temp_path.replace(".pdf", ".txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
