from flask import request, redirect, render_template


def delete_staff(conn):
    if request.method == "POST":
        sid = request.form["sid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM STAFF WHERE SID = %s", (sid,))
        conn.commit()
        return redirect("/admin")

    # Fetch staff data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT SID, FNAME, LNAME FROM STAFF")
    staff_data = cursor.fetchall()

    return render_template("delete_staff.html", staff=staff_data)