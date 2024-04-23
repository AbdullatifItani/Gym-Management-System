from flask import request, redirect, render_template


def update_class(conn):
    if request.method == "POST":
        # Get the form data
        cid = request.form["cid"]
        max_cap = request.form["max_cap"]
        description = request.form["description"]

        # Construct the UPDATE query based on provided form data
        update_query = "UPDATE CLASS SET"
        update_values = []

        if max_cap:
            update_query += " MAX_CAP = %s,"
            update_values.append(max_cap)

        if description:
            update_query += " DESCRIPTION = %s,"
            update_values.append(description)

        # Fetch class data from the database
        cursor = conn.cursor()
        cursor.execute("SELECT CID, CNAME FROM CLASS")
        classes = cursor.fetchall()

        # If no fields are provided for update, return an error
        if not update_values:
            return render_template("update_class.html", classes=classes,
                                   error="At least one field must be provided for the update to occur")

        # Remove the trailing comma and space from the query
        update_query = update_query.rstrip(",") + " WHERE CID = %s"
        update_values.append(cid)

        # Execute the UPDATE query
        cursor = conn.cursor()
        cursor.execute(update_query, update_values)
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/admin")

    # Fetch class data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT CID, CNAME FROM CLASS")
    classes = cursor.fetchall()

    # Render the form for updating class details and pass class data to the template
    return render_template("update_class.html", classes=classes)