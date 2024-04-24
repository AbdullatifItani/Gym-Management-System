from flask import request, redirect, render_template, session
from EECE433Project.helper_functions import decode_token


def delete_emergency_contact(conn):
    if request.method == "POST":
        selected_contact = request.form.get('emid_name')

        if selected_contact:
            emid, ename = selected_contact.split('|')
        cursor = conn.cursor()
        # Check if the emergency contact exists
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s AND ENAME = %s", (emid, ename,))
        contact_data = cursor.fetchone()
        if contact_data is None:
            return "Emergency contact not found."

        # Delete the emergency contact
        cursor.execute("DELETE FROM EMERGENCY_CONTACT WHERE EMID = %s AND ENAME = %s", (emid, ename))
        conn.commit()

        return redirect("/admin")

    # Fetch emergency contact data to populate dropdowns
    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
        contact_data = cursor.fetchall()
    else:
        emid = decode_token(session['token'])
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s", (emid, ))
        contact_data = cursor.fetchall()

    return render_template("delete_emergency_contact.html", contacts=contact_data)
