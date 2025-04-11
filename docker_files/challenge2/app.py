from flask import Flask, request, render_template, redirect, make_response, send_file

app = Flask(__name__)


@app.route('/')
def index():
    user = request.cookies.get('user', 'guest')
    if user == 'admin':
        return render_template('admin.html')
    return render_template('index.html')


@app.route('/flag')
def flag():
    user = request.cookies.get('user', 'guest')
    if user == 'admin':
            return render_template('flag.html')
    return "Access denied. You must be admin to see this.", 403



@app.route('/setcookie/<value>')
def setcookie(value):
    resp = make_response(redirect('/'))
    resp.set_cookie('user', value, max_age=30)  # scade dopo 30 secondi
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user')
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
