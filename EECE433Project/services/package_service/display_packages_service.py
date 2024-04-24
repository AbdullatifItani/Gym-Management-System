from flask import render_template

def display_packages(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PACKAGE")
    packages = cursor.fetchall()
    return render_template("display_packages.html", packages=packages)