from flask import request, redirect, render_template


def assign_emergency_contact(conn):
    if request.method == "POST":
        emid = request.form["emid"]
        ename = request.form["ename"]
        contact = request.form["contact"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO EMERGENCY_CONTACT (EMID, ENAME, CONTACT)
                        VALUES (%s, %s, %s)""",
                       (emid, ename, contact))
        conn.commit()
        return redirect("/admin")
    # Fetch member data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    return render_template("assign_emergency_contact.html", members=member_data)