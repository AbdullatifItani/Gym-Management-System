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
            ppid = request.form["ppid"]
            pmid
            cursor = conn.cursor()
            cursor.execute()

    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("SELECT * FROM MEMBER_PACKAGE")
        member_packages = cursor.fetchall()
    else:
        pmid = decode_token(session['token'])
        cursor.execute("""SELECT * FROM MEMBER_PACKAGE
                            WHERE PMID = %s AND END_DATE >= CURRENT_DATE""",
                       (pmid,))

        member_packages = cursor.fetchone()

    return render_template("delete_member_package.html", member_packages=member_packages)
