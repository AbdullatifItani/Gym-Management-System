from flask import request, redirect, render_template


def assign_class_equipment(conn):
    if request.method == "POST":
        ueid = request.form["ueid"]
        ucid = request.form["ucid"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO CLASS_EQUIPMENT (UEID, UCID)
                        VALUES (%s, %s)""",
                       (ueid, ucid))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and class data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EQUIPMENT")
    equipment_data = cursor.fetchall()
    cursor.execute("SELECT * FROM CLASS")
    class_data = cursor.fetchall()
    return render_template("assign_class_equipment.html", equipment=equipment_data, classes=class_data)