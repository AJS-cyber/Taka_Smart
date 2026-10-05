
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
    for column, definition in (("photo_type", "VARCHAR(80) NULL"), ("photo_meaning", "TEXT NULL")):
        try:
            cur.execute(f"ALTER TABLE reports ADD COLUMN {column} {definition}")
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authorities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(180) NOT NULL,
            authority_type VARCHAR(80) NOT NULL,
            email VARCHAR(150) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            location VARCHAR(255) NOT NULL,
            description TEXT,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        cur.execute("ALTER TABLE authorities ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT ''")
    except Error:
        pass
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(120) NOT NULL UNIQUE,
            email VARCHAR(180) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL DEFAULT 'reporter',
            permissions JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Migrate older installations that already have a users table.
    existing_user_columns = set()
    cur.execute("SHOW COLUMNS FROM users")
    existing_user_columns.update(row[0] for row in cur.fetchall())
    if "username" not in existing_user_columns:
        cur.execute("ALTER TABLE users ADD COLUMN username VARCHAR(120) NULL")
        cur.execute("UPDATE users SET username=COALESCE(NULLIF(name, ''), NULLIF(email, ''), CONCAT('user_', id)) WHERE username IS NULL")
    if "permissions" not in existing_user_columns:
        cur.execute("ALTER TABLE users ADD COLUMN permissions TEXT NOT NULL")
        cur.execute("UPDATE users SET permissions='[]' WHERE permissions IS NULL OR permissions='' ")
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

def create_report(description, authority, location, photo, lat=None, lng=None, photo_type=None, photo_meaning=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reports(description,authority,location,photo,lat,lng,photo_type,photo_meaning) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
        (description, authority, location, photo, lat, lng, photo_type, photo_meaning)
    )
    conn.commit()
    report_id = cur.lastrowid
    cur.close(); conn.close()
    return report_id

def get_reports():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT id, description, authority, location, photo, lat, lng, status, photo_type, photo_meaning, created_at
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

def update_report(report_id, description, location, status):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE reports SET description=%s, location=%s, status=%s WHERE id=%s", (description, location, status, report_id))
    conn.commit(); changed = cur.rowcount; cur.close(); conn.close()
    return changed

def delete_report(report_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM reports WHERE id=%s", (report_id,)); conn.commit(); changed = cur.rowcount; cur.close(); conn.close()
    return changed

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

def create_authority(name, authority_type, email, phone, location, description="", password_hash=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO authorities(name,authority_type,email,phone,location,description,password_hash) VALUES(%s,%s,%s,%s,%s,%s,%s)",
        (name, authority_type, email, phone, location, description, password_hash)
    )
    conn.commit()
    authority_id = cur.lastrowid
    cur.close(); conn.close()
    return authority_id

def get_authority_by_email(email):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM authorities WHERE email=%s LIMIT 1", (email,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

def get_authorities():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM authorities ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close(); conn.close()
    for row in rows:
        if row["created_at"]:
            row["created_at"] = row["created_at"].isoformat()
    return rows

def create_user(username, email, password_hash, role, permissions):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO users(username,email,password_hash,role,permissions) VALUES(%s,%s,%s,%s,%s)", (username, email, password_hash, role, json.dumps(permissions)))
    conn.commit(); user_id = cur.lastrowid; cur.close(); conn.close()
    return user_id

def get_users():
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id,username,email,role,permissions,created_at FROM users ORDER BY id DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    for row in rows:
        if isinstance(row["permissions"], str):
            row["permissions"] = json.loads(row["permissions"])
        if row["created_at"]:
            row["created_at"] = row["created_at"].isoformat()
    return rows

def get_user_by_username(username):
    """Lookup a user by username OR email (for flexible login)."""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM users WHERE username=%s OR email=%s LIMIT 1",
        (username, username)
    )
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def update_user(user_id, username, email, role, permissions, password_hash=None):
    conn = get_connection(); cur = conn.cursor()
    if password_hash:
        cur.execute("UPDATE users SET username=%s,email=%s,role=%s,permissions=%s,password_hash=%s WHERE id=%s", (username, email, role, json.dumps(permissions), password_hash, user_id))
    else:
        cur.execute("UPDATE users SET username=%s,email=%s,role=%s,permissions=%s WHERE id=%s", (username, email, role, json.dumps(permissions), user_id))
    conn.commit(); cur.close(); conn.close()

def delete_user(user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,)); conn.commit(); cur.close(); conn.close()
