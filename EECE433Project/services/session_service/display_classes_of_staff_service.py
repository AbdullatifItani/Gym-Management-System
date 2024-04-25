from flask import render_template, request

def display_classes_of_staff(conn):
    staff_id = request.args.get('staff_id')
    cursor = conn.cursor()
    
    if staff_id:
        if staff_id == '':  # If 'All Staff' option is selected
            cursor.execute("SELECT CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME FROM CLASS INNER JOIN SESSION ON CLASS.CID = SESSION.SCID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
        else:
            cursor.execute("SELECT CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME FROM CLASS INNER JOIN SESSION ON CLASS.CID = SESSION.SCID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID WHERE SESSION.SSID = %s", (staff_id,))
    else:
        cursor.execute("SELECT CLASS.CID, CLASS.CNAME, SESSION.SDATE, STAFF.FNAME, STAFF.LNAME FROM CLASS INNER JOIN SESSION ON CLASS.CID = SESSION.SCID INNER JOIN STAFF ON SESSION.SSID = STAFF.SID")
    
    staff_classes = cursor.fetchall()
    cursor.execute("SELECT SID, FNAME, LNAME FROM STAFF")
    staff_members = cursor.fetchall()
    return render_template("display_classes_of_staff.html", staff_members=staff_members, staff_classes=staff_classes)
