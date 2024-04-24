from flask import render_template, request, session

from EECE433Project.helper_functions import decode_token


def display_emergency_contacts(conn):
    cursor = conn.cursor()
    if 'admin' in session:
        member_id = request.args.get('member_id')

        if member_id:
            if member_id == '':
                cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
            else:
                cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s", (member_id,))
        else:
            cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
    else:
        member_id = decode_token(session['token'])
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s", (member_id,))

    emergency_contacts = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_emergency_contacts.html", emergency_contacts=emergency_contacts, members=members)
