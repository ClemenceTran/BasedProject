import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import get_connection

conn = get_connection()
cursor = conn.cursor()

# users.json
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
# reset_tokens.json
with open('data/reset_tokens.json', 'r') as f:
    tokens = json.load(f)

conn = get_connection()
cursor = conn.cursor()

for t in tokens:
    cursor.execute("""
        INSERT IGNORE INTO reset_tokens (token, username, created_at, used)
        VALUES (%s, %s, %s, %s)
    """, (
        t['token'],
        t['username'],
        t['created_at'],
        1 if t['used'] else 0
    ))

conn.commit()
cursor.close()
conn.close()
print("Reset tokens updated.")

# results.json
with open('data/results.json', 'r') as f:
    results = json.load(f)

conn = get_connection()
cursor = conn.cursor()
for r in results:
    cursor.execute("""
        INSERT INTO interviews (user_id, type, job_description, resume_file)
        VALUES (%s, %s, %s, %s)
    """, (1, 'HR', 'Test interview', 'test.pdf'))
    interview_id = cursor.lastrowid

    # scores avg calculation
    scores = r.get("scores", {})
    overall_score = int(sum(scores.values()) / len(scores)) if scores else 0

    cursor.execute("""
        INSERT INTO results (interview_id, overall_score, strengths, weaknesses, final_feedback)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        interview_id,
        overall_score,
        'Migrated from JSON',# Will be replaced by AI-generated strengths after AI integration
        'Migrated from JSON',  # Will be replaced by AI-generated weaknesses after AI integration
        'Migrated from JSON'   # Will be replaced by AI-generated overall feedback after AI integration
    ))

conn.commit()
cursor.close()
conn.close()
print("Results migrated.")