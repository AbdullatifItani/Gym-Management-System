from flask import request, redirect, render_template


def delete_package(conn):
    if request.method == "POST":
        package_id = request.form["package_id"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM PACKAGE WHERE PID = %s", (package_id,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PACKAGE")
    package_data = cursor.fetchall()
    return render_template("delete_package.html", packages=package_data)
