from flask import request, redirect, render_template, session

from EECE433Project.helper_functions import decode_token


def delete_member_package(conn):
    if request.method == "POST":
        if 'admin' in session:
            member_package_id = request.form["member_package_id"]

            cursor = conn.cursor()
            cursor.execute("DELETE FROM MEMBER_PACKAGE WHERE PMID = %s", (member_package_id,))
            conn.commit()
            return redirect("/admin")
        else:
            selected_package = request.form.get('selected_package')

            if selected_package:
                ppid, pdate = selected_package.split('|')
            pmid = decode_token(session['token'])
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MEMBER_PACKAGE WHERE PMID = %s and ppid = %s and start_date=%s", (pmid, ppid, pdate))
            conn.commit()
            return redirect("/")

    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("SELECT * FROM MEMBER_PACKAGE")
        member_packages = cursor.fetchall()
    else:
        member_id = decode_token(session['token'])
        cursor.execute(
            "SELECT PACKAGE.PID, PACKAGE.PNAME, PACKAGE.DESCRIPTION, MEMBER_PACKAGE.START_DATE, MEMBER_PACKAGE.END_DATE FROM PACKAGE INNER JOIN MEMBER_PACKAGE ON PACKAGE.PID = MEMBER_PACKAGE.PPID WHERE MEMBER_PACKAGE.PMID = %s",
            (member_id,))
        member_packages = cursor.fetchall()

    return render_template("delete_member_package.html", member_packages=member_packages)
