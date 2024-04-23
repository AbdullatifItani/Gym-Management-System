from flask import request, redirect, render_template


def delete_member_gym_session(conn):
    if request.method == "POST":
        gdate_time = request.form["gdate_time"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM MEMBER_GYM_SESSION WHERE GDATE_TIME = %s", (gdate_time,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT GMID, GDATE_TIME FROM MEMBER_GYM_SESSION")
    gym_sessions = cursor.fetchall()

    return render_template("delete_member_gym_session.html", gym_sessions=gym_sessions)