from flask import request, redirect, render_template


def delete_class(conn):
    if request.method == "POST":
        cid = request.form["cid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM CLASS WHERE CID = %s", (cid,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT CID, CNAME FROM CLASS")
    classes = cursor.fetchall()

    return render_template("delete_class.html", classes=classes)