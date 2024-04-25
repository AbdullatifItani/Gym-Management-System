from flask import request, redirect, render_template, session
from EECE433Project.helper_functions import decode_token

def assign_member_gym_session(conn):
    if request.method == "POST":
        if 'admin' in session:
            gmid = request.form["gmid"]
        else:
            gmid = decode_token(session['token'])
        gdate_time = request.form["gdate_time"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER_GYM_SESSION (GMID, GDATE_TIME)
                        VALUES (%s, %s)""",
                       (gmid, gdate_time))
        conn.commit()
        return redirect("/")
    # Fetch member and gym session data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM GYM_SESSION")
    gym_session_data = cursor.fetchall()
    return render_template("assign_member_gym_session.html", members=member_data, gym_sessions=gym_session_data)