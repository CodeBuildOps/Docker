from flask import Flask, request, redirect, render_template
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

WriterPort = 5000
DBPort = 5432

DB_NAME = 'messagedb'
TABLE_NAME = 'message'

DB_CONFIG = {
    'dbname': DB_NAME,
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': DBPort
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def check_db_status():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    )
                """, (TABLE_NAME,))
                return cur.fetchone()[0]
    except Exception as e:
        raise RuntimeError(f"❌ DB error: {e}")

@app.route('/health')
def health():
    return "OK", 200

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if not check_db_status():
            return f"❌ Table '{TABLE_NAME}' does not exist in database.", 500

        if request.method == 'POST':
            msg = request.form['message']
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql.SQL("INSERT INTO {} (content) VALUES (%s)").format(
                        sql.Identifier(TABLE_NAME)
                    ), [msg])
                    conn.commit()
            return redirect('/')

         # Get pod or container ID (in Kubernetes, HOSTNAME is typically the pod name)
        return render_template('index.html', container_id=os.environ.get('HOSTNAME', 'Unknown'))

    except Exception as e:
        return f"❌ Route: index(): {e}", 500

if __name__ == '__main__':
    # ⚠️ No DB check here — app will start regardless of DB state
    app.run(host='0.0.0.0', port=WriterPort)
