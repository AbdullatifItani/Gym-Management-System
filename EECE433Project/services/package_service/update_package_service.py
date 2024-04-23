from flask import request, redirect, render_template


def update_package(conn):
    if request.method == "POST":
        # Get the form data
        pid = request.form["pid"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]

        # Construct the UPDATE query based on provided form data
        update_query = "UPDATE PACKAGE SET"
        update_values = []

        if description:
            update_query += " DESCRIPTION = %s,"
            update_values.append(description)

        if price:
            update_query += " PRICE = %s,"
            update_values.append(price)

        if duration:
            update_query += " DURATION = %s,"
            update_values.append(duration)

        # Fetch package data from the database
        cursor = conn.cursor()
        cursor.execute("SELECT PID, PNAME FROM PACKAGE")
        packages = cursor.fetchall()

        # If no fields are provided for update, return an error
        if not update_values:
            return render_template("update_package.html", packages=packages,
                                   error="At least one field must be provided for the update to occur")

        # Remove the trailing comma and space from the query
        update_query = update_query.rstrip(",") + " WHERE PID = %s"
        update_values.append(pid)

        # Execute the UPDATE query
        cursor = conn.cursor()
        cursor.execute(update_query, update_values)
        conn.commit()

        # Redirect to a confirmation page or back to the admin panel
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT PID, PNAME FROM PACKAGE")
    packages = cursor.fetchall()
    # Render the form for updating package details and pass package data to the template
    return render_template("update_package.html", packages=packages)