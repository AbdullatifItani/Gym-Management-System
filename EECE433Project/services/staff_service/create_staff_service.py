from flask import request, redirect, render_template


def create_staff(conn):
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