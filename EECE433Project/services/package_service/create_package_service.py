from flask import request, redirect, render_template


def create_package(conn):
    if request.method == "POST":
        pname = request.form["pname"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO PACKAGE (PNAME, DESCRIPTION, PRICE, DURATION)
                        VALUES (%s, %s, %s, %s)""",
                       (pname, description, price, duration))
        conn.commit()
        return redirect("/admin")
    return render_template("create_package.html")