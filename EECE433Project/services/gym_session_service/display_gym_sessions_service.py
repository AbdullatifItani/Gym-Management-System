from flask import render_template

def display_gym_sessions(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GYM_SESSION")
    gym_sessions = cursor.fetchall()
    return render_template("display_gym_sessions.html", gym_sessions=gym_sessions)