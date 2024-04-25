from flask import render_template, request

def display_gym_session_members(conn):
    session_id = request.args.get('session_id')
    cursor = conn.cursor()
    
    if session_id:
        if session_id == '':  # If 'All Sessions' option is selected
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME")
        else:
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME WHERE MEMBER_GYM_SESSION.GDATE_TIME = %s", (session_id,))
    else:
        cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME")
    
    session_members = cursor.fetchall()
    cursor.execute("SELECT DATE_TIME FROM GYM_SESSION")
    sessions = cursor.fetchall()
    return render_template("display_gym_session_members.html", session_members=session_members, sessions=sessions)
