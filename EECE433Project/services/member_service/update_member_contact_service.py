from flask import request, redirect, render_template, session
from EECE433Project.helper_functions import decode_token


def update_member_contact(conn):
    if request.method == "POST":
        # Get the form data
        if 'admin' in session:
            mid = request.form["mid"]
        else:
            mid = decode_token(session['token'])
        new_contact = request.form["new_contact"]

        # Update member contact information in the database
        cursor = conn.cursor()
        cursor.execute("UPDATE MEMBER SET CONTACT = %s WHERE MID = %s", (new_contact, mid))
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/")

    # Fetch member data from the database
    if 'admin' in session and session['admin']:
        cursor = conn.cursor()
        cursor.execute("SELECT MID, FNAME, LNAME, CONTACT FROM MEMBER")
        member_data = cursor.fetchall()
        return render_template("update_member_contact.html", members=member_data)
    else:
        return render_template("update_member_contact.html")