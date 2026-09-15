
import os
import json
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

try:
    from .database import (
        init_db, get_stats, create_report, get_reports,
        create_buyer, get_buyers
    )
    from .classifier import classify_waste
    from .chatbot import get_chat_reply
except ImportError:
    from database import (
        init_db, get_stats, create_report, get_reports,
        create_buyer, get_buyers
    )
    from classifier import classify_waste
    from chatbot import get_chat_reply

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_photo(file):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        raise ValueError("Aina ya picha hairuhusiwi. Tumia JPG, PNG, GIF au WEBP.")
    filename = secure_filename(file.filename)
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    final_name = f"{stamp}_{filename}"
    file.save(UPLOAD_DIR / final_name)
    return f"/static/uploads/{final_name}"


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/stats")
def stats():
    return jsonify(get_stats())


@app.get("/api/reports")
def reports():
    return jsonify({"reports": get_reports()})


@app.post("/api/reports")
def add_report():
    try:
        description = request.form.get("description", "").strip()
        authority = request.form.get("authority", "").strip()
        location = request.form.get("location", "").strip()
        lat = request.form.get("lat", "").strip() or None
        lng = request.form.get("lng", "").strip() or None
        if not description or not authority:
            return jsonify({"error": "Maelezo na mamlaka vinahitajika."}), 400

        photo = save_photo(request.files.get("photo"))
        report_id = create_report(description, authority, location, photo, lat, lng)
        return jsonify({"message": "Report saved", "id": report_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Imeshindikana kuhifadhi ripoti."}), 500


@app.get("/api/buyers")
def buyers():
    buyer_type = request.args.get("type", "all")
    search = request.args.get("search", "")
    return jsonify({"buyers": get_buyers(buyer_type, search)})


@app.post("/api/buyers")
def add_buyer():
    data = request.get_json(silent=True) or {}
    required = ["name", "email", "phone", "location", "types"]
    if any(not data.get(k) for k in required):
        return jsonify({"error": "Jaza taarifa zote muhimu na chagua aina za taka."}), 400
    try:
        buyer_id = create_buyer(
            data["name"], data["email"], data["phone"],
            data["location"], data.get("description", ""),
            data["types"], data.get("lat"), data.get("lng")
        )
        return jsonify({"message": "Buyer registered", "id": buyer_id}), 201
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Imeshindikana kusajili mnunuzi. Hakikisha database imeanzishwa."}), 500


@app.post("/api/identify")
def identify():
    try:
        file = request.files.get("photo")
        if not file or not file.filename:
            return jsonify({"error": "Tafadhali chagua picha."}), 400
        # Starter/demo classifier. See classifier.py for where to plug in a real model.
        result = classify_waste(file)
        return jsonify(result)
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Imeshindikana kuchambua picha."}), 500


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    lang = data.get("lang", "sw")
    if not message:
        return jsonify({"error": "Andika swali."}), 400
    return jsonify({"reply": get_chat_reply(message, lang)})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
