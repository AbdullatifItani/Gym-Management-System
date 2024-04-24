from flask import request, render_template, redirect


def update_equipment(conn):
    if request.method == "POST":
        # Get the form data
        eid = request.form["eid"]
        condition = request.form["condition"]

        # Construct the UPDATE query based on the provided form data
        update_query = "UPDATE EQUIPMENT SET"
        update_values = []

        if condition:
            update_query += " CONDITION = %s,"
            update_values.append(condition)

        # If no fields are provided for update, return an error
        if not update_values:
            # Fetch equipment data from the database
            cursor = conn.cursor()
            cursor.execute("SELECT EID, NAME, CONDITION FROM EQUIPMENT")
            equipment = cursor.fetchall()
            return render_template("update_equipment.html", equipment=equipment,
                                   error="At least one field must be provided for update")

        # Remove the trailing comma and space from the query
        update_query = update_query.rstrip(",") + " WHERE EID = %s"
        update_values.append(eid)

        # Execute the UPDATE query
        cursor = conn.cursor()
        cursor.execute(update_query, update_values)
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/admin")

    # Fetch equipment data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT EID, NAME, CONDITION FROM EQUIPMENT")
    equipment = cursor.fetchall()

    # Render the form for updating equipment details and pass equipment data to the template
    return render_template("update_equipment.html", equipment=equipment)