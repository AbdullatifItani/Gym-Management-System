import datetime
from functools import wraps

import jwt

from flask import Flask, render_template, request, session, redirect
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = psycopg2.connect(
    database="Gym", user="postgres",
    password="pikacrafter", host="127.0.0.1", port="5432"
)

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        staff = request.form.get("staff")
        cursor = conn.cursor()
        if staff:
            cursor.execute("select sid, pass from staff where email =%s", (email,))
        else:
            cursor.execute("select mid, pass from member where email =%s", (email,))
        data = cursor.fetchone()
        if data is None:
            return render_template("login.html", error="Incorrect Login Information")
        if data[1] == password:
            if email == "admin@gmail.com" and staff:
                session['admin'] = True
            if staff:
                session['staff'] = True
            session['token'] = create_token(data[0])
            return redirect("/")
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        contact = request.form["contact"]
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER (FNAME, LNAME, GENDER, DOB, EMAIL, PASS, CONTACT, JOININGDATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'now()')""",
                       (fname, lname, gender, dob, email, password, contact))
        conn.commit()
        cursor.execute("select mid from member where email =%s", (email,))
        data = cursor.fetchone()
        session['token'] = create_token(data[0])
        return redirect("/")
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/admin')
@admin_required
def admin_panel():
    # Admin functionalities
    if request.method == "POST":
        if request.form.get("action") == "create_staff":
            return redirect("/create_staff")
        elif request.form.get("action") == "create_class":
            return redirect("/create_class")
    return render_template('admin_panel.html')

@app.route('/create_member', methods=["GET", "POST"])
@admin_required
def create_member():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        email = request.form["email"]
        password = request.form["password"]
        contact = request.form["contact"]
        joining_date = datetime.datetime.now().date()
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER (FNAME, LNAME, GENDER, DOB, EMAIL, PASS, CONTACT, JOININGDATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (fname, lname, gender, dob, email, password, contact, joining_date))
        conn.commit()
        return redirect("/admin")
    return render_template("create_member.html")

@app.route('/delete_member', methods=["GET", "POST"])
@admin_required
def delete_member():
    if request.method == "POST":
        mid = request.form["mid"]
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MEMBER")
        existing_members = cursor.fetchall()
        
        cursor.execute("DELETE FROM MEMBER WHERE MID = %s", (mid,))
        conn.commit()
        
        return redirect("/admin")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    existing_members = cursor.fetchall()
    return render_template("delete_member.html", members=existing_members)



@app.route('/assign_emergency_contact', methods=["GET", "POST"])
@admin_required
def create_emergency_contact():
    if request.method == "POST":
        emid = request.form["emid"]
        ename = request.form["ename"]
        contact = request.form["contact"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO EMERGENCY_CONTACT (EMID, ENAME, CONTACT)
                        VALUES (%s, %s, %s)""",
                       (emid, ename, contact))
        conn.commit()
        return redirect("/admin")
    # Fetch member data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    return render_template("assign_emergency_contact.html", members=member_data)

@app.route('/delete_emergency_contact', methods=["GET", "POST"])
@admin_required
def delete_emergency_contact():
    if request.method == "POST":
        emid = request.form["emid"]
        
        cursor = conn.cursor()
        # Check if the emergency contact exists
        cursor.execute("SELECT * FROM EMERGENCY_CONTACT WHERE EMID = %s", (emid,))
        contact_data = cursor.fetchone()
        if contact_data is None:
            return "Emergency contact not found."
        
        # Delete the emergency contact
        cursor.execute("DELETE FROM EMERGENCY_CONTACT WHERE EMID = %s", (emid,))
        conn.commit()
        
        return redirect("/admin")
    
    # Fetch emergency contact data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMERGENCY_CONTACT")
    contact_data = cursor.fetchall()
    
    return render_template("delete_emergency_contact.html", contacts=contact_data)


@app.route('/create_package', methods=["GET", "POST"])
@admin_required
def create_package():
    if request.method == "POST":
        pname = request.form["pname"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO PACKAGE (PNAME, DESCRIPTION, PRICE, DURATION)
                        VALUES (%s, %s, %s, %s)""",
                       (pname, description, price, duration))
        conn.commit()
        return redirect("/admin")
    return render_template("create_package.html")

@app.route('/delete_package', methods=["GET", "POST"])
@admin_required
def delete_package():
    if request.method == "POST":
        package_id = request.form["package_id"]
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PACKAGE WHERE PID = %s", (package_id,))
        conn.commit()
        return redirect("/admin")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PACKAGE")
    package_data = cursor.fetchall()
    return render_template("delete_package.html", packages=package_data)


@app.route('/assign_member_package', methods=["GET", "POST"])
@admin_required
def assign_member_package():
    if request.method == "POST":
        ppid = request.form["ppid"]
        pmid = request.form["pmid"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER_PACKAGE (PPID, PMID, START_DATE, END_DATE)
                        VALUES (%s, %s, %s, %s)""",
                       (ppid, pmid, start_date, end_date))
        conn.commit()
        return redirect("/admin")
    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM PACKAGE")
    package_data = cursor.fetchall()
    return render_template("assign_member_package.html", members=member_data, packages=package_data)

@app.route('/delete_member_package', methods=["GET", "POST"])
@admin_required
def delete_member_package():
    if request.method == "POST":
        member_package_id = request.form["member_package_id"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM MEMBER_PACKAGE WHERE MEMBER_PACKAGE_ID = %s", (member_package_id,))
        conn.commit()
        return redirect("/admin")

    # Fetch member and package data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER_PACKAGE")
    member_packages = cursor.fetchall()

    return render_template("delete_member_package.html", member_packages=member_packages)




@app.route('/create_review', methods=["GET", "POST"])
@admin_required
def create_review():
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

@app.route('/delete_review', methods=["GET","POST"])
@admin_required
def delete_review():
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


@app.route('/create_gym_session', methods=["GET", "POST"])
@admin_required
def create_gym_session():
    if request.method == "POST":
        date_time = request.form["date_time"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO GYM_SESSION (DATE_TIME)
                        VALUES (%s)""",
                       (date_time,))
        conn.commit()
        return redirect("/admin")
    return render_template("create_gym_session.html")

@app.route('/delete_gym_session', methods=["GET", "POST"])
@admin_required
def delete_gym_session():
    if request.method == "POST":
        date_time = request.form["date_time"]
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GYM_SESSION WHERE DATE_TIME = %s", (date_time,))
        conn.commit()
        return redirect("/admin")

    # Fetch gym session data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT DATE_TIME FROM GYM_SESSION")
    gym_sessions = cursor.fetchall()

    return render_template("delete_gym_session.html", gym_sessions=gym_sessions)



@app.route('/assign_member_gym_session', methods=["GET", "POST"])
@admin_required
def assign_member_gym_session():
    if request.method == "POST":
        gmid = request.form["gmid"]
        gdate_time = request.form["gdate_time"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO MEMBER_GYM_SESSION (GMID, GDATE_TIME)
                        VALUES (%s, %s)""",
                       (gmid, gdate_time))
        conn.commit()
        return redirect("/admin")
    # Fetch member and gym session data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM GYM_SESSION")
    gym_session_data = cursor.fetchall()
    return render_template("assign_member_gym_session.html",members=member_data, gym_sessions=gym_session_data)

@app.route('/delete_member_gym_session', methods=["GET", "POST"])
@admin_required
def delete_member_gym_session():
    if request.method == "POST":
        gdate_time = request.form["gdate_time"]
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MEMBER_GYM_SESSION WHERE GDATE_TIME = %s", (gdate_time,))
        conn.commit()
        return redirect("/admin")
    
    cursor = conn.cursor()
    cursor.execute("SELECT GMID, GDATE_TIME FROM MEMBER_GYM_SESSION")
    gym_sessions = cursor.fetchall()
    
    return render_template("delete_member_gym_session.html", gym_sessions=gym_sessions)

@app.route('/create_class', methods=["GET", "POST"])
@admin_required
def create_class():
    if request.method == "POST":
        cname = request.form["cname"]
        max_cap = request.form["max_cap"]
        description = request.form["description"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO CLASS (CNAME, MAX_CAP, DESCRIPTION)
                        VALUES (%s, %s, %s)""",
                       (cname, max_cap, description))
        conn.commit()
        return redirect("/admin")
    return render_template("create_class.html")

@app.route('/delete_class', methods=["GET", "POST"])
@admin_required
def delete_class():
    if request.method == "POST":
        cid = request.form["cid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM CLASS WHERE CID = %s", (cid,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT CID, CNAME FROM CLASS")
    classes = cursor.fetchall()

    return render_template("delete_class.html", classes=classes)


@app.route('/create_equipment', methods=["GET", "POST"])
@admin_required
def create_equipment():
    if request.method == "POST":
        name = request.form["name"]
        purchase_date = request.form["purchase_date"]
        condition = request.form["condition"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO EQUIPMENT (NAME, PURCHASE_DATE, CONDITION)
                        VALUES (%s, %s, %s)""",
                       (name, purchase_date, condition))
        conn.commit()
        return redirect("/admin")
    return render_template("create_equipment.html")

@app.route('/delete_equipment', methods=["GET", "POST"])
@admin_required
def delete_equipment():
    if request.method == "POST":
        eid = request.form["eid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM EQUIPMENT WHERE EID = %s", (eid,))
        conn.commit()
        return redirect("/admin")

    cursor = conn.cursor()
    cursor.execute("SELECT EID, NAME FROM EQUIPMENT")
    equipments = cursor.fetchall()

    return render_template("delete_equipment.html", equipments=equipments)


@app.route('/assign_class_equipment', methods=["GET", "POST"])
@admin_required
def assign_class_equipment():
    if request.method == "POST":
        ueid = request.form["ueid"]
        ucid = request.form["ucid"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO CLASS_EQUIPMENT (UEID, UCID)
                        VALUES (%s, %s)""",
                       (ueid, ucid))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and class data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EQUIPMENT")
    equipment_data = cursor.fetchall()
    cursor.execute("SELECT * FROM CLASS")
    class_data = cursor.fetchall()
    return render_template("assign_class_equipment.html", equipment=equipment_data, classes=class_data)

@app.route('/delete_class_equipment', methods=["GET", "POST"])
@admin_required
def delete_class_equipment():
    if request.method == "POST":
        ceid = request.form["ceid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM CLASS_EQUIPMENT WHERE UEID = %s", (ceid,))
        conn.commit()
        return redirect("/admin")

    # Fetch class equipment data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT UEID, UCID FROM CLASS_EQUIPMENT")
    class_equipment_data = cursor.fetchall()

    return render_template("delete_class_equipment.html", class_equipment=class_equipment_data)


@app.route('/create_staff', methods=["GET", "POST"])
@admin_required
def create_staff():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        email = request.form["email"]
        password = request.form["password"]
        contact = request.form["contact"]
        salary = request.form["salary"]
        position = request.form["position"]
        employment_date = request.form["employment_date"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO STAFF (FNAME, LNAME, GENDER, DOB, EMAIL, PASS, CONTACT, SALARY, POSITION, EMPLOYMENTDATE)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (fname, lname, gender, dob, email, password, contact, salary, position, employment_date))
        conn.commit()
        return redirect("/admin")
    return render_template("create_staff.html")

@app.route('/delete_staff', methods=["GET", "POST"])
@admin_required
def delete_staff():
    if request.method == "POST":
        sid = request.form["sid"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM STAFF WHERE SID = %s", (sid,))
        conn.commit()
        return redirect("/admin")

    # Fetch staff data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT SID, FNAME, LNAME FROM STAFF")
    staff_data = cursor.fetchall()

    return render_template("delete_staff.html", staff=staff_data)


@app.route('/assign_logs', methods=["GET", "POST"])
def assign_logs():
    if request.method == "POST":
        leid = request.form["leid"]
        lsid = request.form["lsid"]
        ldate = request.form["ldate"]
        details = request.form["details"]
        cost = request.form["cost"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO LOGS (LEID, LSID, LDATE, DETAILS, COST)
                          VALUES (%s, %s, %s, %s, %s)""",
                       (leid, lsid, ldate, details, cost))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EQUIPMENT")
    equipment_data = cursor.fetchall()
    cursor.execute("SELECT * FROM STAFF")
    staff_data = cursor.fetchall()
    return render_template("assign_logs.html", equipment=equipment_data, staff=staff_data)

@app.route('/delete_logs', methods=["GET", "POST"])
@admin_required
def delete_logs():
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


@app.route('/assign_session', methods=["GET", "POST"])
def assign_session():
    if request.method == "POST":
        scid = request.form["scid"]
        ssid = request.form["ssid"]
        sdate = request.form["sdate"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO SESSION (SCID, SSID, SDATE)
                          VALUES (%s, %s, %s)""",
                       (scid, ssid, sdate))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLASS")
    class_data = cursor.fetchall()
    cursor.execute("SELECT * FROM STAFF")
    staff_data = cursor.fetchall()
    return render_template("assign_session.html", classes=class_data, staff=staff_data)

@app.route('/delete_session', methods=["GET", "POST"])
@admin_required
def delete_session():
    if request.method == "POST":
        scid = request.form["scid"]
        ssid = request.form["ssid"]
        sdate = request.form["sdate"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM SESSION WHERE SCID = %s AND SSID = %s AND SDATE = %s", (scid, ssid, sdate))
        conn.commit()
        return redirect("/admin")

    # Fetch session data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT SCID, SSID, SDATE FROM SESSION")
    session_data = cursor.fetchall()

    return render_template("delete_session.html", sessions=session_data)


@app.route('/assign_registered', methods=["GET", "POST"])
def assign_registered():
    if request.method == "POST":
        regmid = request.form["regmid"]
        regsid = request.form["regsid"]
        regcid = request.form["regcid"]
        regdate = request.form["regdate"]
        
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO REGISTERED (REGMID, REGSID, REGCID, REGDATE)
                          VALUES (%s, %s, %s, %s)""",
                       (regmid, regsid, regcid, regdate))
        conn.commit()
        return redirect("/admin")
    # Fetch equipment and staff data to populate dropdowns
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    member_data = cursor.fetchall()
    cursor.execute("SELECT * FROM SESSION")
    session_data = cursor.fetchall()
    return render_template("assign_registered.html", members=member_data, sessions=session_data)

@app.route('/delete_registered', methods=["GET", "POST"])
@admin_required
def delete_registered():
    if request.method == "POST":
        regmid = request.form["regmid"]
        regsid = request.form["regsid"]
        regcid = request.form["regcid"]
        regdate = request.form["regdate"]

        cursor = conn.cursor()
        cursor.execute("DELETE FROM REGISTERED WHERE REGMID = %s AND REGSID = %s AND REGCID = %s AND REGDATE = %s", (regmid, regsid, regcid, regdate))
        conn.commit()
        return redirect("/admin")

    # Fetch registered data to populate dropdown
    cursor = conn.cursor()
    cursor.execute("SELECT REGMID, REGSID, REGCID, REGDATE FROM REGISTERED")
    registered_data = cursor.fetchall()

    return render_template("delete_registered.html", registered=registered_data)


if __name__ == '__main__':
    app.run(debug=True)
