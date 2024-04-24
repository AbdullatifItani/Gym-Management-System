from flask import render_template


def display_members(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_members.html", members=members)
