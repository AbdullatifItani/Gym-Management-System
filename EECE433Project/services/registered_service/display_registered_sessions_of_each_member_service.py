from flask import render_template, request

def display_registered_sessions_of_each_member(conn):
    member_id = request.args.get('member_id')
    cursor = conn.cursor()
    
    if member_id:
        if member_id == '':  # If 'All Members' option is selected
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME FROM MEMBER INNER JOIN REGISTERED ON MEMBER.MID = REGISTERED.REGMID INNER JOIN SESSION ON REGISTERED.REGSID = SESSION.SCID INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
        else:
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME FROM MEMBER INNER JOIN REGISTERED ON MEMBER.MID = REGISTERED.REGMID INNER JOIN SESSION ON REGISTERED.REGSID = SESSION.SCID INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID WHERE MEMBER.MID = %s", (member_id,))
    else:
        cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME FROM MEMBER INNER JOIN REGISTERED ON MEMBER.MID = REGISTERED.REGMID INNER JOIN SESSION ON REGISTERED.REGSID = SESSION.SCID INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
    
    member_registered_sessions = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_registered_sessions_of_each_member.html", members=members, member_registered_sessions=member_registered_sessions)
