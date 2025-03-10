from flask import request, redirect, render_template, session
from EECE433Project.helper_functions import decode_token


def delete_registered(conn):
    if request.method == "POST":
        regvalues = request.form["reg"]
        reg_values_list = regvalues.split("|")
        if 'admin' in session:
            regmid = reg_values_list[0]
        else:
            regmid = decode_token(session['token'])
        regcid = reg_values_list[1]
        regsid = reg_values_list[2]
        regdate = reg_values_list[3]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM REGISTERED WHERE REGMID = %s AND REGCID = %s AND REGSID = %s AND REGDATE = %s",
                       (regmid,regcid,regsid,regdate))
        conn.commit()
        return redirect("/")

    # Fetch registered data to populate dropdown
    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME, STAFF.SID FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
        
    else:
        #cursor.execute("SELECT REGMID, REGSID, REGCID, REGDATE FROM REGISTERED")
        regmid = decode_token(session['token'])
        cursor.execute("SELECT SESSION.SDATE, CLASS.CID, CLASS.CNAME, MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, STAFF.FNAME, STAFF.LNAME, STAFF.SID FROM SESSION INNER JOIN CLASS ON SESSION.SCID = CLASS.CID INNER JOIN REGISTERED ON SESSION.SSID = REGISTERED.REGSID INNER JOIN MEMBER ON REGISTERED.REGMID = MEMBER.MID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID WHERE MEMBER.MID = %s", (regmid,))
    registered_data = cursor.fetchall()
    
    return render_template("delete_registered.html", registered=registered_data)