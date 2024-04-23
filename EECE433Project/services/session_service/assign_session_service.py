from flask import request, redirect, render_template


def assign_session(conn):
    if request.method == "POST":
        scid = request.form["scid"]
        ssid = request.form["ssid"]
        sdate = request.form["sdate"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO SESSION (SCID, SSID, SDATE)
                          VALUES (%s, %s, %s)""",
                       (scid, ssid, sdate))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLASS")
    class_data = cursor.fetchall()
    cursor.execute("SELECT * FROM STAFF")
    staff_data = cursor.fetchall()
    return render_template("assign_session.html", classes=class_data, staff=staff_data)