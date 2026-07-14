import os
import sqlite3
import zlib

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "travel_packing.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for concurrent reads/writes
    conn.execute("PRAGMA journal_mode=WAL;")
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def compress_data(text: str) -> bytes:
    if not text:
        return b""
    return zlib.compress(text.encode("utf-8"))

def decompress_data(data: bytes) -> str:
    if not data:
        return ""
    return zlib.decompress(data).decode("utf-8")

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Trips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id VARCHAR(50) PRIMARY KEY,
        trip_name VARCHAR(100) NOT NULL,
        start_date VARCHAR(10) NOT NULL,
        group_size INTEGER NOT NULL DEFAULT 1,
        activities TEXT,
        is_archived BOOLEAN DEFAULT 0,
        list_locked BOOLEAN DEFAULT 0,
        destinations TEXT,
        compressed_items BLOB,
        theme VARCHAR(20) DEFAULT 'sand',
        origin_country VARCHAR(100) DEFAULT 'United States',
        traveler_names TEXT DEFAULT '[]',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Onboarding and global states table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS onboarding_state (
        key VARCHAR(100) PRIMARY KEY,
        value TEXT
    );
    """)

    # Travelers profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS travelers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id VARCHAR(50) NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        name VARCHAR(100) NOT NULL,
        demographic_category VARCHAR(50) DEFAULT 'adult',
        preference_tags TEXT DEFAULT '[]',
        medications TEXT DEFAULT '[]'
    );
    """)

    # Packing items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS packing_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id VARCHAR(50) NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        parent_id INTEGER REFERENCES packing_items(id) ON DELETE CASCADE,
        item_name VARCHAR(150) NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        category VARCHAR(50) NOT NULL DEFAULT 'General',
        priority VARCHAR(20) NOT NULL DEFAULT 'Medium', -- 'Low', 'Medium', 'High'
        is_private BOOLEAN DEFAULT 1, -- 0 for public, 1 for private
        is_checked BOOLEAN DEFAULT 0,
        sort_order INTEGER DEFAULT 0,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Audit logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_type VARCHAR(50) NOT NULL, -- 'security', 'agent', 'audit'
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Migration: Add custom_sub_items to travelers if missing
    cursor.execute("PRAGMA table_info(travelers)")
    cols = [c[1] for c in cursor.fetchall()]
    if "custom_sub_items" not in cols:
        cursor.execute("ALTER TABLE travelers ADD COLUMN custom_sub_items TEXT DEFAULT '{}'")

    # Destination research cache table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS destination_research_cache (
        location VARCHAR(150) NOT NULL,
        month VARCHAR(50) NOT NULL,
        analysis_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(location, month)
    );
    """)

    # Copilot chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS copilot_chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id VARCHAR(50) NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        role VARCHAR(20) NOT NULL, -- 'user' or 'copilot'
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

init_db()

