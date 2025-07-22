from flask import Flask, request, redirect, render_template
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

DB_CONFIG = {
    'dbname': os.environ['DATABASE_NAME'],
    'user': os.environ['DATABASE_USER'],
    'password': os.environ['DATABASE_PASSWORD'],
    'host': os.environ['DATABASE_HOST'], # Use the service name defined in docker-compose
    'port': os.environ['DATABASE_PORT']
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
                """, (os.environ['DATABASE_TABLE_NAME'],))
                table_exists = cur.fetchone()[0]

                if not table_exists:
                    return "❌ Table does not exist in the database. Please contact the administrator.", 500

        if request.method == 'POST':
            msg = request.form['message']
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql.SQL("INSERT INTO {} (content) VALUES (%s)").format(
                        sql.Identifier(os.environ['DATABASE_TABLE_NAME'])
                    ), [msg])
                    conn.commit()
            return redirect('/')

        return render_template('index.html')

    except Exception as e:
        return f"❌ Error connecting to database or checking table: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['WRITER_PORT'])