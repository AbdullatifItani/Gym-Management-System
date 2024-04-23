from flask import request, redirect, render_template


def assign_logs(conn):
    if request.method == "POST":
        leid = request.form["leid"]
        lsid = request.form["lsid"]
        ldate = request.form["ldate"]
        details = request.form["details"]
        cost = request.form["cost"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO LOGS (LEID, LSID, LDATE, DETAILS, COST)
                          VALUES (%s, %s, %s, %s, %s)""",
                       (leid, lsid, ldate, details, cost))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EQUIPMENT")
    equipment_data = cursor.fetchall()
    cursor.execute("SELECT * FROM STAFF")
    staff_data = cursor.fetchall()
    return render_template("assign_logs.html", equipment=equipment_data, staff=staff_data)