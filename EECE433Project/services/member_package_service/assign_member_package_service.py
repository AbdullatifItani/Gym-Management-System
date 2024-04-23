from flask import request, redirect, render_template


def assign_member_package(conn):
    if request.method == "POST":
        ppid = request.form["ppid"]
        pmid = request.form["pmid"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER_PACKAGE (PPID, PMID, START_DATE, END_DATE)
                        VALUES (%s, %s, %s, %s)""",
                       (ppid, pmid, start_date, end_date))
        conn.commit()
        return redirect("/admin")
    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM PACKAGE")
    package_data = cursor.fetchall()
    return render_template("assign_member_package.html", members=member_data, packages=package_data)