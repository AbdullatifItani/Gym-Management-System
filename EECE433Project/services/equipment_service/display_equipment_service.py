from flask import render_template

def display_equipment(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EQUIPMENT")
    equipment = cursor.fetchall()
    return render_template("display_equipment.html", equipment=equipment)