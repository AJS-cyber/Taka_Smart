
import os
import json
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

try:
    from .database import (
        init_db, get_stats, create_report, get_reports,
        create_buyer, get_buyers, create_authority, get_authorities, get_authority_by_email,
        create_user, get_users, update_user, delete_user, update_report, delete_report,
        get_user_by_username
    )
    from .classifier import classify_waste
    from .chatbot import get_chat_reply
except ImportError:
    from database import (
        init_db, get_stats, create_report, get_reports,
        create_buyer, get_buyers, create_authority, get_authorities, get_authority_by_email,
        create_user, get_users, update_user, delete_user, update_report, delete_report,
        get_user_by_username
    )
    from classifier import classify_waste
    from chatbot import get_chat_reply

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "takasmart-development-key")
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

@app.get("/admin")
def admin_portal():
    return render_template("admin.html")

@app.get("/authority")
def authority_portal():
    return render_template("authority.html")


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
        authority_aliases = {
            "municipal": "municipal",
            "environment": "environment",
            "health": "health",
            "waste": "waste",
            "waste_company": "waste",
        }
        authority = authority_aliases.get(authority, authority)

        uploaded_photo = request.files.get("photo")
        photo_type = None
        photo_meaning = None
        if uploaded_photo and uploaded_photo.filename:
            analysis = classify_waste(uploaded_photo)
            if analysis.get("accepted"):
                waste = analysis["waste"]
                photo_type = waste.get("type")
                photo_meaning = waste.get("desc", {}).get("sw", "")
            else:
                photo_meaning = "Picha ya eneo/ripoti imehifadhiwa kwa ukaguzi wa mamlaka; YOLO haikuthibitisha aina moja ya taka."
            uploaded_photo.stream.seek(0)
        photo = save_photo(uploaded_photo)
        report_id = create_report(description, authority, location, photo, lat, lng, photo_type, photo_meaning)
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

@app.post("/api/authorities")
def add_authority():
    data = request.get_json(silent=True) or {}
    required = ["name", "authority_type", "email", "phone", "location", "password"]
    if any(not str(data.get(key, "")).strip() for key in required):
        return jsonify({"error": "Jaza taarifa zote za mamlaka."}), 400
    try:
        authority_id = create_authority(
            data["name"].strip(), data["authority_type"].strip(),
            data["email"].strip(), data["phone"].strip(),
            data["location"].strip(), data.get("description", "").strip(), generate_password_hash(data["password"])
        )
        return jsonify({"message": "Authority registered", "id": authority_id}), 201
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Imeshindikana kusajili mamlaka."}), 500

@app.post("/api/authority/login")
def authority_login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or data.get("email") or "").strip()
    authority = get_authority_by_email(username)
    if not authority or not check_password_hash(authority["password_hash"], data.get("password", "")):
        return jsonify({"error": "Email au password ya mamlaka si sahihi."}), 401
    session["authority_id"] = authority["id"]
    session["authority_type"] = authority["authority_type"]
    session["authority_name"] = authority["name"]
    return jsonify({"message": "Authority login successful", "name": authority["name"]})

@app.get("/api/authority/dashboard")
def authority_dashboard():
    if not session.get("authority_id"):
        return jsonify({"error": "Authority login inahitajika."}), 401
    authority_type = session.get("authority_type")
    authority_aliases = {
        "municipal": {"municipal", "council", "halmashauri"},
        "environment": {"environment", "environment_department", "ministry_environment", "wizara_environment"},
        "health": {"health", "health_department", "idara_afya"},
        "waste": {"waste", "waste_company", "waste_authority", "shirika_taka"},
    }
    accepted_types = authority_aliases.get(authority_type, {authority_type})
    reports = [r for r in get_reports() if str(r["authority"]).strip().lower() in accepted_types]
    return jsonify({
        "authority_name": session.get("authority_name", "Mamlaka"),
        "authority_type": authority_type,
        "reports": reports,
        "pending_count": sum(1 for report in reports if report["status"] == "pending"),
        "tasks": ["auth_task_receive", "auth_task_status", "auth_task_feedback", "auth_task_report"],
    })

def authority_report_ids():
    authority_type = session.get("authority_type")
    accepted_types = {
        "municipal": {"municipal", "council", "halmashauri"},
        "environment": {"environment", "environment_department", "ministry_environment", "wizara_environment"},
        "health": {"health", "health_department", "idara_afya"},
        "waste": {"waste", "waste_company", "waste_authority", "shirika_taka"},
    }.get(authority_type, {authority_type})
    return {report["id"] for report in get_reports() if str(report["authority"]).strip().lower() in accepted_types}

@app.put("/api/authority/reports/<int:report_id>")
def edit_authority_report(report_id):
    if not session.get("authority_id"):
        return jsonify({"error": "Authority login inahitajika."}), 401
    if report_id not in authority_report_ids():
        return jsonify({"error": "Ripoti hii si ya idara yako."}), 403
    data = request.get_json(silent=True) or {}
    status = data.get("status", "pending")
    if status not in {"pending", "in_progress", "resolved"}:
        return jsonify({"error": "Status ya ripoti si sahihi."}), 400
    changed = update_report(report_id, str(data.get("description", "")).strip(), str(data.get("location", "")).strip(), status)
    return jsonify({"message": "Report updated", "changed": changed})

@app.delete("/api/authority/reports/<int:report_id>")
def remove_authority_report(report_id):
    if not session.get("authority_id"):
        return jsonify({"error": "Authority login inahitajika."}), 401
    if report_id not in authority_report_ids():
        return jsonify({"error": "Ripoti hii si ya idara yako."}), 403
    changed = delete_report(report_id)
    return jsonify({"message": "Report deleted", "changed": changed})

@app.post("/api/admin/login")
def admin_login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or data.get("email") or "").strip()
    password = data.get("password", "")
    expected_username = os.getenv("ADMIN_USERNAME", os.getenv("ADMIN_EMAIL", "admin"))
    expected_password = os.getenv("ADMIN_PASSWORD", "change-me-now")
    if username != expected_username or password != expected_password:
        return jsonify({"error": "Taarifa za admin si sahihi."}), 401
    session["is_admin"] = True
    return jsonify({"message": "Admin login successful"})

@app.post("/api/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return jsonify({"message": "Admin logged out"})


# ── User login (for users created via the admin panel) ────────────────────────

@app.post("/api/user/login")
def user_login():
    """Authenticate a user from the `users` table (admin-created accounts)."""
    data = request.get_json(silent=True) or {}
    identifier = (data.get("username") or data.get("email") or "").strip()
    password   = data.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "Jaza username/email na password."}), 400

    user = get_user_by_username(identifier)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Username/email au password si sahihi. Jaribu tena."}), 401

    # Store user info in session
    session["user_id"]   = user["id"]
    session["user_role"] = user["role"]
    session["user_name"] = user["username"]

    import json as _json
    permissions = user.get("permissions", [])
    if isinstance(permissions, str):
        try:
            permissions = _json.loads(permissions)
        except Exception:
            permissions = []

    return jsonify({
        "message":     "Login successful",
        "user_id":     user["id"],
        "username":    user["username"],
        "email":       user["email"],
        "role":        user["role"],
        "permissions": permissions,
    })


@app.post("/api/user/logout")
def user_logout():
    session.pop("user_id",   None)
    session.pop("user_role", None)
    session.pop("user_name", None)
    return jsonify({"message": "Logged out"})


@app.get("/api/user/dashboard")
def user_dashboard():
    """Return dashboard data for the currently logged-in user."""
    if not session.get("user_id"):
        return jsonify({"error": "Tafadhali ingia kwanza."}), 401

    stats = get_stats()
    role  = session.get("user_role", "reporter")

    # Admin users get the full admin dashboard data
    if role == "admin":
        return jsonify({
            "role":         role,
            "username":     session.get("user_name"),
            "stats":        stats,
            "reports":      get_reports(),
            "users":        get_users(),
            "authorities":  get_authorities(),
            "capabilities": [
                "manage_users", "manage_reports", "manage_buyers",
                "manage_authorities", "view_stats", "system_config", "security"
            ],
        })

    # All other roles get a minimal dashboard
    return jsonify({
        "role":     role,
        "username": session.get("user_name"),
        "stats":    stats,
        "reports":  get_reports(),
    })

@app.get("/api/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return jsonify({"error": "Admin login inahitajika."}), 401
    return jsonify({
        "stats": get_stats(),
        "authorities": get_authorities(),
        "users": get_users(),
        "reports": get_reports(),
        "capabilities": [
            "manage_users",
            "manage_reports",
            "manage_buyers",
            "manage_authorities",
            "view_stats",
            "system_config",
            "security"
        ]
    })

def admin_required():
    return session.get("is_admin")

@app.post("/api/admin/users")
def add_admin_user():
    if not admin_required(): return jsonify({"error": "Admin login inahitajika."}), 401
    data = request.get_json(silent=True) or {}
    required = ["username", "email", "password", "role"]
    if any(not str(data.get(key, "")).strip() for key in required):
        return jsonify({"error": "Jaza username, email, password na role."}), 400
    valid_roles = {"admin", "reporter", "buyer", "authority", "support"}
    if data.get("role", "").strip() not in valid_roles:
        return jsonify({"error": "Wadhifa si sahihi."}), 400
    try:
        user_id = create_user(data["username"].strip(), data["email"].strip(), generate_password_hash(data["password"]), data["role"].strip(), data.get("permissions", []))
        return jsonify({"id": user_id}), 201
    except Exception as e:
        app.logger.exception(e); return jsonify({"error": "Username inaweza kuwa tayari imetumika."}), 400

@app.put("/api/admin/users/<int:user_id>")
def edit_admin_user(user_id):
    if not admin_required(): return jsonify({"error": "Admin login inahitajika."}), 401
    data = request.get_json(silent=True) or {}
    if any(not str(data.get(key, "")).strip() for key in ("username", "email", "role")):
        return jsonify({"error": "Username, email na role vinahitajika."}), 400
    valid_roles = {"admin", "reporter", "buyer", "authority", "support"}
    if data.get("role", "").strip() not in valid_roles:
        return jsonify({"error": "Wadhifa si sahihi."}), 400
    password_hash = generate_password_hash(data["password"]) if data.get("password") else None
    update_user(user_id, data["username"].strip(), data["email"].strip(), data["role"].strip(), data.get("permissions", []), password_hash)
    return jsonify({"message": "User updated"})

@app.delete("/api/admin/users/<int:user_id>")
def remove_admin_user(user_id):
    if not admin_required(): return jsonify({"error": "Admin login inahitajika."}), 401
    delete_user(user_id); return jsonify({"message": "User deleted"})


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
