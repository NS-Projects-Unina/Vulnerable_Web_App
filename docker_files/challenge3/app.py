from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# Funzione per inizializzare il database
def init_db():
    conn = sqlite3.connect('challenge.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                 )''')


    c.execute("DROP TABLE IF EXISTS profiles")
    c.execute('''
        CREATE TABLE profiles (
            user_id INTEGER PRIMARY KEY,
            nickname TEXT,
            email TEXT,
            address TEXT,
            phone TEXT,
            birth TEXT,
            ssn TEXT,
            salary INTEGER,
            flag TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')


    c.execute("SELECT * FROM users WHERE username = 'alice'")
    alice = c.fetchone()
    if not alice:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('alice', 'passwordalice'))


    c.execute("SELECT * FROM users WHERE username = 'bob'")
    bob = c.fetchone()
    if not bob:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('bob', 'passwordbob'))


    c.execute('''
        INSERT INTO profiles (
            user_id, nickname, email, address, phone, birth, ssn, salary, flag
        ) VALUES (
            (SELECT id FROM users WHERE username = 'alice'),
            'alice',
            'alice@attack.com',
            'Via delle Rose 1',
            '33333333',
            '9/20',
            '10211002',
            99999,
            NULL
        )
    ''')

    c.execute('''
        INSERT INTO profiles (
            user_id, nickname, email, address, phone, birth, ssn, salary, flag
        ) VALUES (
            (SELECT id FROM users WHERE username = 'bob'),
            'bob',
            'bob@securemail.com',
            'Via dei Gelsi 2',
            '44444444',
            '12/02',
            '99887766',
            75000,
            'CTF{flag_from_bob}'
        )
    ''')

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('challenge.db')
    conn.row_factory = sqlite3.Row
    return conn


def check_login(username, password):
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()
    conn.close()
    return user


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = check_login(username, password)
        
        if user:
            if user['username'] == 'bob' and user['password'] != 'passwordbob':
                return redirect(f"/flag/{user['id']}")
            return redirect(f"/profile/{user['id']}")
        else:
            message = "Credenziali errate."

    return render_template('login.html', message=message)


@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    profile = conn.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,)).fetchone()
    message = ""
    conn.close()
    return render_template('profile.html', user=user, profile=profile, message=message)


@app.route("/edit_profile/<int:user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    message = ""
    if request.method == "POST":
        nickname = request.form.get("nickname")
        email = request.form.get("email")
        address = request.form.get("address")
        phone = request.form.get("phone")
        password = request.form.get("password")
        # Query vulnerabile a SQLi
        query = f"UPDATE users SET password = '{password}' WHERE id = {user_id}"
        print('[DEBUG] QUERY COSTRUITA:', query)
        conn = get_db_connection()
        try:
            conn.execute(query)
            conn.commit()
            message = "Profilo aggiornato"
        except Exception as e:
            message = f"Errore durante l'aggiornamento: {e}"
        conn.close()
    return render_template("edit_profile.html", user=user, message=message)

@app.route("/flag/<int:user_id>")
def flag(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    profile = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    if user and user['username'] == 'bob' and user['password'] != 'passwordbob':
        return render_template("flag.html", flag=profile["flag"])
    return "Accesso non autorizzato."


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)