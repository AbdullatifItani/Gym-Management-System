from flask import request, redirect, render_template, session

from EECE433Project.helper_functions import decode_token


def delete_review(conn):
    if request.method == "POST":
        review_id = request.form["review_id"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM REVIEW WHERE RID = %s", (review_id,))
        conn.commit()
        return redirect("/")

    cursor = conn.cursor()
    if 'admin' in session:
        cursor.execute("""SELECT RMID, RID, DESCRIPTION FROM REVIEW
                        JOIN MEMBER_REVIEW ON REVIEW.RID = MEMBER_REVIEW.RRID""")
        review_data = cursor.fetchall()
    else:
        mid = decode_token(session['token'])
        cursor.execute("""SELECT RMID, RID, DESCRIPTION FROM REVIEW
                        JOIN MEMBER_REVIEW ON REVIEW.RID = MEMBER_REVIEW.RRID
                        WHERE RMID = %s""", (mid,))
        review_data = cursor.fetchall()
    return render_template("delete_review.html", reviews=review_data)
