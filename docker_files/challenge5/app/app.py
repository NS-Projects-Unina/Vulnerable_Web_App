from flask import Flask, request, render_template_string, redirect, make_response

app = Flask(__name__)
messages = []

ADMIN_COOKIE = "admin_secret_cookie_123"
FLAG = open("flag.txt").read()

@app.route("/", methods=["GET", "POST"])
def index():
    global messages
    if request.method == "POST":
        content = request.form.get("content", "")
        messages.append(content)
        return redirect("/")
    message_html = "<br>".join(messages)
    return render_template_string("""
        <h2>WormBlog</h2>
        <form method='POST'>
            <textarea name='content'></textarea><br>
            <button type='submit'>Post</button>
        </form>
        <hr>
        <h3>Messages:</h3>
        {{ messages|safe }}
    """, messages=message_html)

@app.route("/admin")
def admin():
    resp = make_response("Admin is viewing posts...")
    resp.set_cookie("auth", ADMIN_COOKIE)
    return resp

@app.route("/steal")
def steal():
    stolen = request.args.get("cookie")
    if ADMIN_COOKIE in (stolen or ""):
        return f"Nice! The flag is: {FLAG}"
    return "Invalid cookie."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
