from flask import render_template

def display_classes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLASS")
    classes = cursor.fetchall()
    return render_template("display_classes.html", classes=classes)