from flask import request, redirect, render_template


def delete_class_equipment(conn):
    if request.method == "POST":
        ceid = request.form["ceid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM CLASS_EQUIPMENT WHERE UEID = %s", (ceid,))
        conn.commit()
        return redirect("/admin")

    # Fetch class equipment data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT UEID, UCID FROM CLASS_EQUIPMENT")
    class_equipment_data = cursor.fetchall()

    return render_template("delete_class_equipment.html", class_equipment=class_equipment_data)