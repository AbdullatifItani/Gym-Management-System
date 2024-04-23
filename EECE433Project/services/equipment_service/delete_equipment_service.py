from flask import request, redirect, render_template


def delete_equipment(conn):
    if request.method == "POST":
        eid = request.form["eid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM EQUIPMENT WHERE EID = %s", (eid,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT EID, NAME FROM EQUIPMENT")
    equipments = cursor.fetchall()

    return render_template("delete_equipment.html", equipments=equipments)