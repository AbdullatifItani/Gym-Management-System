from flask import render_template, request, session
from EECE433Project.helper_functions import decode_token


def display_member_packages(conn):
    if 'admin' in session:
        member_id = request.args.get('member_id')
    else:
        member_id = decode_token(session['token'])
    
    cursor = conn.cursor()
    cursor.execute("SELECT PACKAGE.PID, PACKAGE.PNAME, MEMBER_PACKAGE.START_DATE, MEMBER_PACKAGE.END_DATE FROM PACKAGE INNER JOIN MEMBER_PACKAGE ON PACKAGE.PID = MEMBER_PACKAGE.PPID WHERE MEMBER_PACKAGE.PMID = %s", (member_id,))
    member_packages = cursor.fetchall()
    
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_member_packages.html", member_packages=member_packages, members=members)
