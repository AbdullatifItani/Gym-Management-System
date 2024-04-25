from flask import render_template, request

def display_member_gym_sessions(conn):
    member_id = request.args.get('member_id')
    cursor = conn.cursor()
    
    if member_id:
        if member_id == '':  # If 'All Members' option is selected
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME")
        else:
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME WHERE MEMBER_GYM_SESSION.GMID = %s", (member_id,))
    else:
        cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, GYM_SESSION.DATE_TIME FROM MEMBER INNER JOIN MEMBER_GYM_SESSION ON MEMBER.MID = MEMBER_GYM_SESSION.GMID INNER JOIN GYM_SESSION ON MEMBER_GYM_SESSION.GDATE_TIME = GYM_SESSION.DATE_TIME")
    
    member_gym_sessions = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    
    return render_template("display_member_gym_sessions.html", member_gym_sessions=member_gym_sessions, members=members)
