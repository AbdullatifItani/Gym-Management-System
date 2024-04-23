from flask import request, redirect, render_template


def delete_review(conn):
    if request.method == "POST":
        review_id = request.form["review_id"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM REVIEW WHERE RID = %s", (review_id,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT RID, DESCRIPTION FROM REVIEW")
    review_data = cursor.fetchall()
    return render_template("delete_review.html", reviews=review_data)