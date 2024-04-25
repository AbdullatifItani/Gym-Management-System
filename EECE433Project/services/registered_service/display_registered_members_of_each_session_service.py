from flask import render_template, request

'''def display_registered_members_of_each_session(conn):
    session_id = request.args.get('session_id')
    cursor = conn.cursor()
    
    if session_id:
        if session_id == '':  # If 'All Sessions' option is selected
            cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
        else:
            cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID WHERE SESSION.SSID = %s", (session_id,))
    else:
        cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
    
    session_registered_members = cursor.fetchall()
    cursor.execute("SELECT SSID, SDATE FROM SESSION")
    sessions = cursor.fetchall()
    return render_template("display_registered_members_of_each_session.html", sessions=sessions, session_registered_members=session_registered_members)'''

def display_registered_members_of_each_session(conn):
    class_id = request.args.get('class_id')
    cursor = conn.cursor()
    
    if class_id:
        if class_id == '':  # If 'All Classes' option is selected
            cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
        else:
            cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID WHERE CLASS.CID = %s", (class_id,))
    else:
        cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
    
    session_registered_members = cursor.fetchall()
    cursor.execute("SELECT CID, CNAME FROM CLASS")
    classes = cursor.fetchall()
    return render_template("display_registered_members_of_each_session.html", classes=classes, session_registered_members=session_registered_members)
