from flask import request, redirect, render_template
import datetime


def create_member(conn):
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        email = request.form["email"]
        password = request.form["password"]
        contact = request.form["contact"]
        joining_date = datetime.datetime.now().date()

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER (FNAME, LNAME, GENDER, DOB, EMAIL, PASS, CONTACT, JOININGDATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (fname, lname, gender, dob, email, password, contact, joining_date))
        conn.commit()
        return redirect("/admin")
    return render_template("create_member.html")