from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        ip = request.form.get("ip", "")
        try:
            output = os.popen(f"ping -c 1 {ip}").read()
        except Exception as e:
            output = str(e)
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PingMe Diagnostic Tool</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    color: #333;
                }

                .container {
                    background-color: #fff;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 500px;
                }

                h2 {
                    text-align: center;
                    color: #5a2a7a;
                    font-size: 26px;
                    margin-bottom: 20px;
                }

                form {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }

                input[type="text"] {
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                    font-size: 16px;
                    width: 100%;
                }

                input[type="text"]:focus {
                    border-color: #3f84f0;
                    outline: none;
                }

                button {
                    background-color: #3f84f0;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-size: 18px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #3579e6;
                }

                pre {
                    background-color: #e8f1ff;
                    padding: 20px;
                    border-radius: 5px;
                    font-size: 14px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }

                footer {
                    text-align: center;
                    margin-top: 20px;
                    font-size: 14px;
                    color: #777;
                }

                footer a {
                    color: #5a2a7a;
                    text-decoration: none;
                }

                footer a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>PingMe Diagnostic Tool</h2>
                <form method="POST">
                    <label for="ip">IP Address:</label>
                    <input type="text" name="ip" id="ip" placeholder="Inserisci l'indirizzo IP" required>
                    <button type="submit">Ping</button>
                </form>
                <pre>{{ output }}</pre>
            </div>
            
            <a href="http://127.0.0.1:5000/dashboard">
            <button type="button">Torna alla Dashboard</button>
        </a>
        
        </body>
        </html>
    """, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
