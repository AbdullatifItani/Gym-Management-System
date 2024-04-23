from flask import request, redirect, render_template


def delete_gym_session(conn):
    if request.method == "POST":
        date_time = request.form["date_time"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM GYM_SESSION WHERE DATE_TIME = %s", (date_time,))
        conn.commit()
        return redirect("/admin")

    # Fetch gym session data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT DATE_TIME FROM GYM_SESSION")
    gym_sessions = cursor.fetchall()

    return render_template("delete_gym_session.html", gym_sessions=gym_sessions)