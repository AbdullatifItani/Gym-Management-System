from flask import request, redirect, render_template, session
from EECE433Project.helper_functions import decode_token


def create_review(conn):
    if request.method == "POST":
        description = request.form["description"]
        token = session["token"]
        mid = decode_token(token)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO REVIEW (DESCRIPTION)
                        VALUES (%s)""",
                       (description,))
        conn.commit()
        cursor.execute("""SELECT RID FROM REVIEW""")
        rid = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO MEMBER_REVIEW (RMID, RRID)
                                VALUES (%s, %s)""",
                       (mid, rid))
        conn.commit()
        return redirect("/admin")
    return render_template("create_review.html")
