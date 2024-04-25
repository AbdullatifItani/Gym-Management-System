from flask import request, redirect, render_template, session

from EECE433Project.helper_functions import decode_token


def assign_member_package(conn):
    if request.method == "POST":
        ppid = request.form["ppid"]
        if 'admin' in session:
            pmid = request.form["pmid"]
        else:
            pmid = decode_token(session['token'])

        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM MEMBER_PACKAGE
                    WHERE PMID = %s AND END_DATE >= CURRENT_DATE""",
                       (pmid,))

        existing_package = cursor.fetchone()

        if existing_package:
            cursor.execute("SELECT * FROM PACKAGE")
            package_data = cursor.fetchall()
            return render_template("assign_member_package.html", packages=package_data, error="You already has an "
                                                                                              "existing package!")

        cursor.execute("""INSERT INTO MEMBER_PACKAGE (PPID, PMID)
                        VALUES (%s, %s)""",
                       (ppid, pmid))
        conn.commit()
        return redirect("/")
    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("SELECT * FROM MEMBER")
        member_data = cursor.fetchall()
        cursor.execute("SELECT * FROM PACKAGE")
        package_data = cursor.fetchall()
        return render_template("assign_member_package.html", members=member_data, packages=package_data)
    else:
        cursor.execute("SELECT * FROM PACKAGE")
        package_data = cursor.fetchall()
        return render_template("assign_member_package.html", packages=package_data)
