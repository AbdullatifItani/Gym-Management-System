from flask import request, redirect, render_template


def create_gym_session(conn):
    if request.method == "POST":
        date_time = request.form["date_time"]

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO GYM_SESSION (DATE_TIME)
                        VALUES (%s)""",
                       (date_time,))
        conn.commit()
        return redirect("/admin")
    return render_template("create_gym_session.html")