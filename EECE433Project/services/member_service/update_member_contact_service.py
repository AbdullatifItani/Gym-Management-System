from flask import request, redirect, render_template


def update_member_contact(conn):
    if request.method == "POST":
        # Get the form data
        mid = request.form["mid"]
        new_contact = request.form["new_contact"]

        # Update member contact information in the database
        cursor = conn.cursor()
        cursor.execute("UPDATE MEMBER SET CONTACT = %s WHERE MID = %s", (new_contact, mid))
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/admin")

    # Fetch member data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT MID, FNAME, LNAME, CONTACT FROM MEMBER")
    member_data = cursor.fetchall()
    return render_template("update_member_contact.html", members=member_data)