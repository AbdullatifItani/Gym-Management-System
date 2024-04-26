from flask import session, render_template

from EECE433Project.helper_functions import decode_token


def view_member(conn):
    mid = decode_token(session['token'])
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM MEMBER WHERE MID = %s""", (mid, ))
    member_data = cursor.fetchall()
    return render_template("view_member.html", member_data=member_data)
