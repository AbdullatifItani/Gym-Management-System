'''from flask import render_template, request

def display_reviews(conn):
    member_id = request.args.get('member_id')
    cursor = conn.cursor()
    
    if member_id:
        if member_id == '':  # If 'All Members' option is selected
            cursor.execute("SELECT * FROM MEMBER_REVIEW")
        else:
            cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, REVIEW.RID, REVIEW.DESCRIPTION FROM MEMBER INNER JOIN MEMBER_REVIEW ON MEMBER.MID = MEMBER_REVIEW.RMID INNER JOIN REVIEW ON MEMBER_REVIEW.RRID = REVIEW.RID WHERE MEMBER.MID = %s", (member_id,))
    else:
        cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, REVIEW.RID, REVIEW.DESCRIPTION FROM MEMBER INNER JOIN MEMBER_REVIEW ON MEMBER.MID = MEMBER_REVIEW.RMID INNER JOIN REVIEW ON MEMBER_REVIEW.RRID = REVIEW.RID")
    
    reviews = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()
    return render_template("display_reviews.html", reviews=reviews, members=members)
'''
from flask import render_template, request, session
from EECE433Project.helper_functions import decode_token


def display_reviews(conn):
    cursor = conn.cursor()
    if 'admin' in session:
        member_id = request.args.get('member_id')
        if member_id:
            if member_id == '':
                # cursor.execute("SELECT * FROM MEMBER_REVIEW")
                cursor.execute(
                    "SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, REVIEW.RID, REVIEW.DESCRIPTION FROM MEMBER INNER JOIN MEMBER_REVIEW ON MEMBER.MID = MEMBER_REVIEW.RMID INNER JOIN REVIEW ON MEMBER_REVIEW.RRID = REVIEW.RID")
            else:
                cursor.execute(
                    "SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, REVIEW.RID, REVIEW.DESCRIPTION FROM MEMBER INNER JOIN MEMBER_REVIEW ON MEMBER.MID = MEMBER_REVIEW.RMID INNER JOIN REVIEW ON MEMBER_REVIEW.RRID = REVIEW.RID WHERE MEMBER.MID = %s",
                    (member_id,))
        else:
            cursor.execute(
                "SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, REVIEW.RID, REVIEW.DESCRIPTION FROM MEMBER INNER JOIN MEMBER_REVIEW ON MEMBER.MID = MEMBER_REVIEW.RMID INNER JOIN REVIEW ON MEMBER_REVIEW.RRID = REVIEW.RID")
    else:
        cursor.execute(
            "SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, REVIEW.RID, REVIEW.DESCRIPTION FROM MEMBER INNER JOIN MEMBER_REVIEW ON MEMBER.MID = MEMBER_REVIEW.RMID INNER JOIN REVIEW ON MEMBER_REVIEW.RRID = REVIEW.RID")

    reviews = cursor.fetchall()
    cursor.execute("SELECT MID, FNAME, LNAME FROM MEMBER")
    members = cursor.fetchall()

    return render_template("display_reviews.html", reviews=reviews, members=members)
