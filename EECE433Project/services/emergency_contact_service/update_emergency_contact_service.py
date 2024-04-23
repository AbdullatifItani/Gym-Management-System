from flask import request, redirect, render_template


def update_emergency_contact(conn):
    if request.method == "POST":
        # Get the form data
        selected_contact = request.form.get('emid_name')

        if selected_contact:
            emid, ename = selected_contact.split('|')
        new_contact = request.form["new_contact"]

        # Update emergency contact information in the database
        cursor = conn.cursor()
        cursor.execute("UPDATE EMERGENCY_CONTACT SET CONTACT = %s WHERE EMID = %s AND ENAME = %s", (new_contact, emid, ename))
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/admin")

    # Fetch emergency contact data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT EMID, ENAME, CONTACT FROM EMERGENCY_CONTACT")
    emergency_contacts = cursor.fetchall()

    return render_template("update_emergency_contact.html", emergency_contacts=emergency_contacts)
