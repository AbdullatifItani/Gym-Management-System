from flask import render_template, request

def display_package_members(conn):
    package_id = request.args.get('package_id')
    
    cursor = conn.cursor()
    cursor.execute("SELECT MEMBER.MID, MEMBER.FNAME, MEMBER.LNAME, MEMBER_PACKAGE.START_DATE, MEMBER_PACKAGE.END_DATE FROM MEMBER INNER JOIN MEMBER_PACKAGE ON MEMBER.MID = MEMBER_PACKAGE.PMID WHERE MEMBER_PACKAGE.PPID = %s", (package_id,))
    package_members = cursor.fetchall()
    
    cursor.execute("SELECT PID, PNAME FROM PACKAGE")
    packages = cursor.fetchall() 
    return render_template("display_package_members.html", package_members=package_members, packages=packages)
