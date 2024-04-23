from flask import request, redirect, render_template


def delete_session(conn):
    if request.method == "POST":
        scid = request.form["scid"]
        ssid = request.form["ssid"]
        sdate = request.form["sdate"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM SESSION WHERE SCID = %s AND SSID = %s AND SDATE = %s", (scid, ssid, sdate))
        conn.commit()
        return redirect("/admin")

    # Fetch session data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT SCID, SSID, SDATE FROM SESSION")
    session_data = cursor.fetchall()

    return render_template("delete_session.html", sessions=session_data)