from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import smart_chat

# ---------------- APP CONFIG ----------------
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "generated_pdfs")


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return "✅ FastSewa Backend is Running"


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user_message = data.get("message", "")
    user_id = data.get("user_id", "default")

    res_text = smart_chat.get_response(user_message, user_id)

    pdf_gen = False
    pdf_file = ""

    # Check if PDF generated
    if "PDF generated successfully" in res_text:
        pdf_gen = True

    return jsonify({
        "success": True,
        "response": res_text,
        "pdf_generated": pdf_gen,
        "pdf_file": pdf_file
    })


@app.route("/api/download-pdf/<filename>")
def download_file(filename):
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
