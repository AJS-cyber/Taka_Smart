
import os
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "taka_smart"),
    }

def server_config():
    cfg = db_config().copy()
    cfg.pop("database")
    return cfg

def get_connection():
    return mysql.connector.connect(**db_config())

def init_db():
    # Create database first.
    conn = mysql.connector.connect(**server_config())
    cur = conn.cursor()
    db_name = db_config()["database"].replace("`", "")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.close()
    conn.close()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            description TEXT NOT NULL,
            authority VARCHAR(100) NOT NULL,
            location VARCHAR(255),
            photo VARCHAR(500),
            lat DECIMAL(10,7) NULL,
            lng DECIMAL(10,7) NULL,
            status ENUM('pending','in_progress','resolved') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for column in ("lat", "lng"):
        try:
            cur.execute(f"ALTER TABLE reports ADD COLUMN {column} DECIMAL(10,7) NULL")
        except Error:
            pass
    cur.execute("""
        CREATE TABLE IF NOT EXISTS buyers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            email VARCHAR(150) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            location VARCHAR(255) NOT NULL,
            description TEXT,
            types JSON NOT NULL,
            lat DECIMAL(10,7) NULL,
            lng DECIMAL(10,7) NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reports")
    reports = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM reports WHERE status='resolved'")
    resolved = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM buyers")
    buyers = cur.fetchone()[0]
    cur.close(); conn.close()
    return {"reports": reports, "resolved": resolved, "buyers": buyers, "recycled": 0}

def create_report(description, authority, location, photo, lat=None, lng=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reports(description,authority,location,photo,lat,lng) VALUES(%s,%s,%s,%s,%s,%s)",
        (description, authority, location, photo, lat, lng)
    )
    conn.commit()
    report_id = cur.lastrowid
    cur.close(); conn.close()
    return report_id

def get_reports():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT id, description, authority, location, photo, lat, lng, status, created_at
        FROM reports ORDER BY id DESC LIMIT 50
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    for r in rows:
        if r["created_at"]:
            r["created_at"] = r["created_at"].isoformat()
        if r["lat"] is not None:
            r["lat"] = float(r["lat"])
        if r["lng"] is not None:
            r["lng"] = float(r["lng"])
    return rows

def create_buyer(name, email, phone, location, description, types, lat=None, lng=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO buyers(name,email,phone,location,description,types,lat,lng) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
        (name, email, phone, location, description, json.dumps(types), lat, lng)
    )
    conn.commit()
    buyer_id = cur.lastrowid
    cur.close(); conn.close()
    return buyer_id

def get_buyers(buyer_type="all", search=""):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    query = "SELECT * FROM buyers WHERE 1=1"
    params = []
    if search:
        query += " AND (name LIKE %s OR location LIKE %s)"
        params += [f"%{search}%", f"%{search}%"]
    query += " ORDER BY id DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close(); conn.close()

    result = []
    for r in rows:
        try:
            types = json.loads(r["types"]) if isinstance(r["types"], str) else r["types"]
        except Exception:
            types = []
        if buyer_type != "all" and buyer_type not in types:
            continue
        result.append({
            "id": r["id"],
            "name": r["name"],
            "email": r["email"],
            "phone": r["phone"],
            "location": r["location"],
            "description": r["description"] or "",
            "types": types,
            "lat": float(r["lat"]) if r["lat"] is not None else None,
            "lng": float(r["lng"]) if r["lng"] is not None else None
        })
    return result
