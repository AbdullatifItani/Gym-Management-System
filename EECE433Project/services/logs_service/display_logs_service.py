from flask import render_template, request

def display_logs(conn):
    equipment_id = request.args.get('equipment_id')
    cursor = conn.cursor()
    
    if equipment_id:
        if equipment_id == '':  # If 'All Equipment' option is selected
            cursor.execute("SELECT EQUIPMENT.EID, EQUIPMENT.NAME, LOGS.LID, STAFF.FNAME, STAFF.LNAME, LOGS.LDATE, LOGS.DETAILS FROM EQUIPMENT INNER JOIN LOGS ON EQUIPMENT.EID = LOGS.LEID INNER JOIN STAFF ON LOGS.LSID = STAFF.SID")
        else:
            cursor.execute("SELECT EQUIPMENT.EID, EQUIPMENT.NAME, LOGS.LID, STAFF.FNAME, STAFF.LNAME, LOGS.LDATE, LOGS.DETAILS FROM EQUIPMENT INNER JOIN LOGS ON EQUIPMENT.EID = LOGS.LEID INNER JOIN STAFF ON LOGS.LSID = STAFF.SID WHERE EQUIPMENT.EID = %s", (equipment_id,))
    else:
        cursor.execute("SELECT EQUIPMENT.EID, EQUIPMENT.NAME, LOGS.LID, STAFF.FNAME, STAFF.LNAME, LOGS.LDATE, LOGS.DETAILS FROM EQUIPMENT INNER JOIN LOGS ON EQUIPMENT.EID = LOGS.LEID INNER JOIN STAFF ON LOGS.LSID = STAFF.SID")
    
    equipment_maintenance = cursor.fetchall()
    cursor.execute("SELECT EID, NAME FROM EQUIPMENT")
    equipments = cursor.fetchall()
    return render_template("display_logs.html", equipment_maintenance=equipment_maintenance, equipments=equipments)
