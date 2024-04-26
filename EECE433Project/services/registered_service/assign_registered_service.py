from flask import request, redirect, render_template, session

from EECE433Project.helper_functions import decode_token


def assign_registered(conn):
    if request.method == "POST":
        if 'admin' in session:
            regmid = request.form["regmid"]
        else:
            regmid = decode_token(session['token'])
        regsid = request.form["regsid"]
        regcid = request.form["regcid"]
        regdate = request.form["regdate"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO REGISTERED (REGMID, REGSID, REGCID, REGDATE)
                          VALUES (%s, %s, %s, %s)""",
                       (regmid, regsid, regcid, regdate))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute(
        "SELECT CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME, STAFF.SID FROM CLASS INNER JOIN SESSION ON CLASS.CID = SESSION.SCID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
    session_data = cursor.fetchall()
    if 'admin' in session:
        cursor.execute("SELECT * FROM MEMBER")
        member_data = cursor.fetchall()
        return render_template("assign_registered.html", members=member_data, sessions=session_data)
    else:
        return render_template("assign_registered.html", sessions=session_data)
