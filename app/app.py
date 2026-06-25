from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>devenv-project</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        h1 { color: #333; }
        input { padding: 8px; margin: 4px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #45a049; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #f2f2f2; }
        .status { padding: 8px; border-radius: 4px; margin: 10px 0; }
        .ok { background: #dff0d8; color: #3c763d; }
        .error { background: #f2dede; color: #a94442; }
    </style>
</head>
<body>
    <h1>User Manager</h1>

    <div id="status" class="status ok">Checking database...</div>

    <h2>Add User</h2>
    <input id="name" placeholder="Name" />
    <input id="email" placeholder="Email" />
    <button onclick="addUser()">Add</button>

    <h2>Users</h2>
    <button onclick="loadUsers()">Refresh</button>
    <table>
        <thead><tr><th>ID</th><th>Name</th><th>Email</th></tr></thead>
        <tbody id="users"></tbody>
    </table>

    <script>
        async function checkHealth() {
            const res = await fetch('/health');
            const data = await res.json();
            const el = document.getElementById('status');
            el.textContent = 'Database: ' + data.database;
            el.className = 'status ' + (data.status === 'healthy' ? 'ok' : 'error');
        }

        async function loadUsers() {
            const res = await fetch('/users');
            const users = await res.json();
            const tbody = document.getElementById('users');
            tbody.innerHTML = users.map(u =>
                `<tr><td>${u.id}</td><td>${u.name}</td><td>${u.email}</td></tr>`
            ).join('');
        }

        async function addUser() {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            if (!name || !email) return alert('Fill in both fields');
            await fetch('/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, email})
            });
            document.getElementById('name').value = '';
            document.getElementById('email').value = '';
            loadUsers();
        }

        checkHealth();
        loadUsers();
    </script>
</body>
</html>
"""

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "devenv"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "admin")
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/health")
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": str(e)}), 500

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": user_id, "name": name, "email": email}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)