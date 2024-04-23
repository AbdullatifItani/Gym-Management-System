from flask import request, render_template, session, redirect
from EECE433Project.helper_functions import create_token


def login(conn):
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        staff = request.form.get("staff")
        cursor = conn.cursor()
        if staff:
            cursor.execute("select sid, pass from staff where email =%s", (email,))
        else:
            cursor.execute("select mid, pass from member where email =%s", (email,))
        data = cursor.fetchone()
        if data is None:
            return render_template("login.html", error="Incorrect Login Information")
        if data[1] == password:
            if email == "admin@gmail.com" and staff:
                session['admin'] = True
            if staff:
                session['staff'] = True
            session['token'] = create_token(data[0])
            return redirect("/")
    return render_template("login.html")
