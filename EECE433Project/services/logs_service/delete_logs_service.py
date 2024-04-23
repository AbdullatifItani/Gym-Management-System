from flask import request, redirect, render_template


def delete_logs(conn):
    if request.method == "POST":
        lid = request.form["lid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM LOGS WHERE LID = %s", (lid,))
        conn.commit()
        return redirect("/admin")

    # Fetch logs data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT LID, LEID, LSID, LDATE, Details FROM LOGS")
    logs_data = cursor.fetchall()

    return render_template("delete_logs.html", logs=logs_data)