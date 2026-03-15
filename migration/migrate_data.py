import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import get_connection

conn = get_connection()
cursor = conn.cursor()

# ── users.json ──────────────────────────────────────────
with open('data/users.json', 'r') as f:
    users = json.load(f)

for user in users:
    cursor.execute("""
        INSERT IGNORE INTO appuser (username, email, password_hash, created_at)
        VALUES (%s, %s, %s, %s)
    """, (
        user['username'],
        user['email'],
        user['password_hash'],
        user['created_at']
    ))

print("Users migrated")

conn.commit()
cursor.close()
conn.close()
print("Completed!")