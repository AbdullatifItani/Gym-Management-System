from flask import request, redirect, render_template


def create_class(conn):
    if request.method == "POST":
        cname = request.form["cname"]
        max_cap = request.form["max_cap"]
        description = request.form["description"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO CLASS (CNAME, MAX_CAP, DESCRIPTION)
                        VALUES (%s, %s, %s)""",
                       (cname, max_cap, description))
        conn.commit()
        return redirect("/admin")
    return render_template("create_class.html")