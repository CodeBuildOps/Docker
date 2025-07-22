from flask import Flask, render_template, jsonify, request
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

ReaderPort = 5001
DBPort = 5432

# DB config
DB_NAME = 'messagedb'
TABLE_NAME = 'message'

DB_CONFIG = {
    'dbname': DB_NAME,
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db-app',    # Update to localhost if running locally, othwise use the service name
    'port': DBPort
}

def query_db(query, args=None, fetch=False):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL(query).format(sql.Identifier(TABLE_NAME)), args or ())
            if fetch:
                return cur.fetchall()

@app.route('/')
def index():
    try:
        # Check DB connection and table presence
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Check if table exists
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    )
                """, (TABLE_NAME,))
                table_exists = cur.fetchone()[0]

                if not table_exists:
                    return "❌ Table does not exist in the database. Please contact the administrator.", 500
        
        return render_template('index.html')
    
    except Exception as e:
        return f"❌ Error connecting to database or checking table: {e}", 500

@app.route('/api/messages', methods=['GET'])
def get_messages():
    rows = query_db("SELECT id, content FROM {} ORDER BY id DESC", fetch=True)
    return jsonify([{'id': r[0], 'content': r[1]} for r in rows])

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    query_db("DELETE FROM {} WHERE id = %s", (message_id,))
    return '', 204

@app.route('/delete_all', methods=['POST'])
def delete_all():
    query_db("DELETE FROM {}")
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ReaderPort)