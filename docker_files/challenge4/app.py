from flask import Flask, request, jsonify, make_response
import jwt
import datetime
import os
from flask import render_template

app = Flask(__name__)


SECRET_KEY = "jwt123"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', 'guest')
    payload = {
        'username': username,
        'role': 'user',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({"token": token})

@app.route('/admin')
def admin():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return make_response("Token mancante", 401)

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if decoded.get('role') == 'admin':
            with open("flag.txt") as f:
                return f"<h3>Flag:</h3><code>{f.read()}</code>"
        else:
            return make_response("Accesso negato: ruolo insufficiente", 403)
    except Exception as e:
        return make_response(f"Token non valido: {str(e)}", 401)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
