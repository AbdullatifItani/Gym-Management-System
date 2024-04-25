from flask import render_template, request, session
from EECE433Project.helper_functions import decode_token

def display_member_gym_sessions(conn):
    cursor = conn.cursor()
    
    if 'admin' in session:
        member_id = request.args.get('member_id')
        if member_id:
            if member_id == '':  # If 'All Members' option is selected
                cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME")
            else:
                cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME WHERE MEMBER_GYM_SESSION.GMID = %s", (member_id,))
        else:
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME")
    else:
        member_id = decode_token(session['token'])
        cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME WHERE MEMBER_GYM_SESSION.GMID = %s", (member_id,))
    member_gym_sessions = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_member_gym_sessions.html", member_gym_sessions=member_gym_sessions, members=members)
