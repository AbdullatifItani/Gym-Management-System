from flask import request, redirect, render_template


def delete_member_package(conn):
    if request.method == "POST":
        member_package_id = request.form["member_package_id"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM MEMBER_PACKAGE WHERE MEMBER_PACKAGE_ID = %s", (member_package_id,))
        conn.commit()
        return redirect("/admin")

    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER_PACKAGE")
    member_packages = cursor.fetchall()

    return render_template("delete_member_package.html", member_packages=member_packages)