from flask import request, redirect, render_template


def assign_member_gym_session(conn):
    if request.method == "POST":
        gmid = request.form["gmid"]
        gdate_time = request.form["gdate_time"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER_GYM_SESSION (GMID, GDATE_TIME)
                        VALUES (%s, %s)""",
                       (gmid, gdate_time))
        conn.commit()
        return redirect("/admin")
    # Fetch member and gym session data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM GYM_SESSION")
    gym_session_data = cursor.fetchall()
    return render_template("assign_member_gym_session.html", members=member_data, gym_sessions=gym_session_data)