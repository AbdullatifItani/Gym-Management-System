from flask import request, redirect, render_template


def delete_member(conn):
    if request.method == "POST":
        mid = request.form["mid"]

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MEMBER")
        existing_members = cursor.fetchall()

        cursor.execute("DELETE FROM MEMBER WHERE MID = %s", (mid,))
        conn.commit()

        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    existing_members = cursor.fetchall()
    return render_template("delete_member.html", members=existing_members)