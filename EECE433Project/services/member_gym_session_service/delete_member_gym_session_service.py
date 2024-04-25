from flask import request, redirect, render_template, session
from EECE433Project.helper_functions import decode_token

def delete_member_gym_session(conn):
    if request.method == "POST":
        gdate_time = request.form["gdate_time"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM MEMBER_GYM_SESSION WHERE GDATE_TIME = %s", (gdate_time,))
        conn.commit()
        return redirect("/")

    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("SELECT GMID, GDATE_TIME FROM MEMBER_GYM_SESSION")
        
    else:
        gmid = decode_token(session['token'])
        cursor.execute("SELECT GMID, GDATE_TIME FROM MEMBER_GYM_SESSION WHERE GMID = %s", (gmid,))
    gym_sessions = cursor.fetchall()

    return render_template("delete_member_gym_session.html", gym_sessions=gym_sessions)