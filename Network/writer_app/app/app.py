from flask import Flask, request, redirect, render_template
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

WriterPort = 5000
DBPort = 5432

# DB config
DB_NAME = 'messagedb'
TABLE_NAME = 'message'

DB_CONFIG = {
    'dbname': DB_NAME,
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db-app',    # Update to localhost if running locally, otherwise use the service name
    'port': DBPort
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        # Check DB connection and table presence
        with get_db_connection() as conn:
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

        if request.method == 'POST':
            msg = request.form['message']
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql.SQL("INSERT INTO {} (content) VALUES (%s)").format(
                        sql.Identifier(TABLE_NAME)
                    ), [msg])
                    conn.commit()
            return redirect('/')

        return render_template('index.html')

    except Exception as e:
        return f"❌ Error connecting to database or checking table: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=WriterPort)