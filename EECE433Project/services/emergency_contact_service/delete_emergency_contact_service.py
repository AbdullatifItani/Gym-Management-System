from flask import request, redirect, render_template


def delete_emergency_contact(conn):
    if request.method == "POST":
        emid = request.form["emid"]

        cursor = conn.cursor()
        # Check if the emergency contact exists
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s", (emid,))
        contact_data = cursor.fetchone()
        if contact_data is None:
            return "Emergency contact not found."

        # Delete the emergency contact
        cursor.execute("DELETE FROM EMERGENCY_CONTACT WHERE EMID = %s", (emid,))
        conn.commit()

        return redirect("/admin")

    # Fetch emergency contact data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
    contact_data = cursor.fetchall()

    return render_template("delete_emergency_contact.html", contacts=contact_data)