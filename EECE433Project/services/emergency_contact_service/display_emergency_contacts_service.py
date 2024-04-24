from flask import render_template, request

def display_emergency_contacts(conn):
    member_id = request.args.get('member_id')
    cursor = conn.cursor()
    
    if member_id:
        if member_id == '':
            cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
        else:
            cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s", (member_id,))
    else:
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
    
    emergency_contacts = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_emergency_contacts.html", emergency_contacts=emergency_contacts, members=members)