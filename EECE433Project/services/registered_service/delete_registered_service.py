from flask import request, redirect, render_template


def delete_registered(conn):
    if request.method == "POST":
        regmid = request.form["regmid"]
        regsid = request.form["regsid"]
        regcid = request.form["regcid"]
        regdate = request.form["regdate"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM REGISTERED WHERE REGMID = %s AND REGSID = %s AND REGCID = %s AND REGDATE = %s",
                       (regmid, regsid, regcid, regdate))
        conn.commit()
        return redirect("/admin")

    # Fetch registered data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT REGMID, REGSID, REGCID, REGDATE FROM REGISTERED")
    registered_data = cursor.fetchall()

    return render_template("delete_registered.html", registered=registered_data)