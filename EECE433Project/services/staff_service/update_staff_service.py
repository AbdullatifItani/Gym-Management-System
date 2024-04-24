from flask import request, redirect, render_template


def update_staff(conn):
    if request.method == "POST":
        # Get the form data
        sid = request.form["sid"]
        contact = request.form["contact"]
        salary = request.form["salary"]
        position = request.form["position"]

        # Construct the UPDATE query based on provided form data
        update_query = "UPDATE STAFF SET"
        update_values = []

        if contact:
            update_query += " CONTACT = %s,"
            update_values.append(contact)

        if salary:
            update_query += " SALARY = %s,"
            update_values.append(salary)

        if position:
            update_query += " POSITION = %s,"
            update_values.append(position)

        # If no fields are provided for update, return an error
        if not update_values:
            # Fetch staff data from the database
            cursor = conn.cursor()
            cursor.execute("SELECT SID, FNAME, LNAME, CONTACT, SALARY, POSITION FROM STAFF")
            staff = cursor.fetchall()
            return render_template("update_staff.html", staff=staff,
                                   error="At least one field must be provided for update")

        # Remove the trailing comma and space from the query
        update_query = update_query.rstrip(",") + " WHERE SID = %s"
        update_values.append(sid)

        # Execute the UPDATE query
        cursor = conn.cursor()
        cursor.execute(update_query, update_values)
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/admin")

    # Fetch staff data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT SID, FNAME, LNAME, CONTACT, SALARY, POSITION FROM STAFF")
    staff = cursor.fetchall()

    # Render the form for updating staff details and pass staff data to the template
    return render_template("update_staff.html", staff=staff)