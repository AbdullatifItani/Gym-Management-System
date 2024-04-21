import datetime
from functools import wraps

import jwt

from flask import Flask, render_template, request, session, redirect
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = psycopg2.connect( 
    database="Gym Management", user="postgres", 
    password="Abed12345", host="127.0.0.1", port="5432" 
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
        cursor.execute("select mid, pass from member where email =%s", (email,))
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
    if request.method == "POST":
        if request.form.get("action") == "create_staff":
            return redirect("/create_staff")
        elif request.form.get("action") == "create_class":
            return redirect("/create_class")
    return render_template('admin_panel.html')

@app.route('/create_staff', methods=["GET", "POST"])
@admin_required
def create_staff():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        email = request.form["email"]
        password = request.form["password"]
        contact = request.form["contact"]
        salary = request.form["salary"]
        position = request.form["position"]
        employment_date = request.form["employment_date"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO STAFF (FNAME, LNAME, GENDER, DOB, EMAIL, PASS, CONTACT, SALARY, POSITION, EMPLOYMENTDATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (fname, lname, gender, dob, email, password, contact, salary, position, employment_date))
        conn.commit()
        return redirect("/admin")
    return render_template("create_staff.html")


@app.route('/create_class', methods=["GET", "POST"])
@admin_required
def create_class():
    if request.method == "POST":
        cname = request.form["cname"]
        max_cap = request.form["max_cap"]
        description = request.form["description"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO CLASS (CNAME, MAX_CAP, DESCRIPTION)
                        VALUES (%s, %s, %s)""",
                       (cname, max_cap, description))
        conn.commit()
        return redirect("/admin")
    return render_template("create_class.html")


if __name__ == '__main__':
    app.run()
