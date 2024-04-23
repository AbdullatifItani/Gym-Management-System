from flask import request, redirect, render_template


def assign_registered(conn):
    if request.method == "POST":
        regmid = request.form["regmid"]
        regsid = request.form["regsid"]
        regcid = request.form["regcid"]
        regdate = request.form["regdate"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO REGISTERED (REGMID, REGSID, REGCID, REGDATE)
                          VALUES (%s, %s, %s, %s)""",
                       (regmid, regsid, regcid, regdate))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM SESSION")
    session_data = cursor.fetchall()
    return render_template("assign_registered.html", members=member_data, sessions=session_data)