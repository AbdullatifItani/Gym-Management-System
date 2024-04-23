from flask import request, redirect, render_template


def create_equipment(conn):
    if request.method == "POST":
        name = request.form["name"]
        purchase_date = request.form["purchase_date"]
        condition = request.form["condition"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO EQUIPMENT (NAME, PURCHASE_DATE, CONDITION)
                        VALUES (%s, %s, %s)""",
                       (name, purchase_date, condition))
        conn.commit()
        return redirect("/admin")
    return render_template("create_equipment.html")