from database import get_connection

try:
    conn = get_connection()
    print("✅ Connected successfully!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities;")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} rows:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)