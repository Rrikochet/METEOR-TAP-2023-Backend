from flask import Flask,redirect, url_for,render_template,send_from_directory, request, session
from datetime import timedelta
import secrets
import string

app = Flask(__name__)
key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.secret_key = key
app.permanent_session_lifetime = timedelta(hours=1)

@app.route("/")
def home():
    #return "<h1>Hello</h1>"
    return render_template("index.html")

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route("/pagenotfound")
def pagenotfound():
    return f"404 Error! Page Not Found"

@app.route("/admin")
def admin():
    return redirect(url_for("pagenotfound"))

if __name__ == "__main__":
    app.run()
    
    
