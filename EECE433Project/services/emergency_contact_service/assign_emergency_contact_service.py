from flask import request, redirect, render_template, session

from EECE433Project.helper_functions import decode_token


def assign_emergency_contact(conn):
    if request.method == "POST":
        if 'admin' in session:
            emid = request.form["emid"]
        else:
            emid = decode_token(session['token'])
        ename = request.form["ename"]
        contact = request.form["contact"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO EMERGENCY_CONTACT (EMID, ENAME, CONTACT)
                        VALUES (%s, %s, %s)""",
                       (emid, ename, contact))
        conn.commit()
        return redirect("/")
    # Fetch member data to populate dropdowns
    if 'admin' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MEMBER")
        member_data = cursor.fetchall()
        return render_template("assign_emergency_contact.html", members=member_data)
    return render_template("assign_emergency_contact.html")
