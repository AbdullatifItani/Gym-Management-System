import datetime
from functools import wraps

import jwt

from flask import Flask, render_template, request, session, redirect
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = psycopg2.connect(
    database="gym", user="postgres",
    password="mysql123", host="127.0.0.1", port="5432"
)

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor = conn.cursor()
        cursor.execute("select mid, pass from auth where email =%s", (email,))
        data = cursor.fetchone()
        if data is None:
            return "error"
        if data[1] == password:
            if email == "admin@gmail.com":
                session['admin'] = True
            session['token'] = create_token(data[0])
            return redirect("/")
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        contact = request.form["contact"]
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER (FNAME, LNAME, GENDER, DOB, EMAIL, PASS, CONTACT, JOININGDATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'now()')""",
                       (fname, lname, gender, dob, email, password, contact))
        conn.commit()
        cursor.execute("select mid from member where email =%s", (email,))
        data = cursor.fetchone()
        session['token'] = create_token(data[0])
        return redirect("/")
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/admin')
@admin_required
def admin_panel():
    # Admin functionalities
    return render_template('admin_panel.html')


if __name__ == '__main__':
    app.run()
