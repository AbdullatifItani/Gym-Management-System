from flask import request, redirect, render_template


def assign_member_package(conn):
    if request.method == "POST":
        ppid = request.form["ppid"]
        pmid = request.form["pmid"]

        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM MEMBER_PACKAGE
                    WHERE PMID = %s AND END_DATE >= CURRENT_DATE""",
                       (pmid,))

        existing_package = cursor.fetchone()

        if existing_package:
            return "Member already has an active package."

        cursor.execute("""INSERT INTO MEMBER_PACKAGE (PPID, PMID)
                        VALUES (%s, %s)""",
                       (ppid, pmid))
        conn.commit()
        return redirect("/admin")
    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM PACKAGE")
    package_data = cursor.fetchall()
    return render_template("assign_member_package.html", members=member_data, packages=package_data)