from flask import render_template

def display_staff(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM STAFF")
    staff = cursor.fetchall()
    return render_template("display_staff.html", staff=staff)