from flask import render_template, request

def display_class_equipment(conn):
    class_id = request.args.get('class_id')
    cursor = conn.cursor()
    
    if class_id:
        if class_id == '':  # If 'All Classes' option is selected
            cursor.execute("SELECT CLASS.CID, CLASS.CNAME, EQUIPMENT.NAME FROM CLASS INNER JOIN CLASS_EQUIPMENT ON CLASS.CID = CLASS_EQUIPMENT.UCID INNER JOIN EQUIPMENT ON CLASS_EQUIPMENT.UEID = EQUIPMENT.EID")
        else:
            cursor.execute("SELECT CLASS.CID, CLASS.CNAME, EQUIPMENT.NAME FROM CLASS INNER JOIN CLASS_EQUIPMENT ON CLASS.CID = CLASS_EQUIPMENT.UCID INNER JOIN EQUIPMENT ON CLASS_EQUIPMENT.UEID = EQUIPMENT.EID WHERE CLASS.CID = %s", (class_id,))
    else:
        cursor.execute("SELECT CLASS.CID, CLASS.CNAME, EQUIPMENT.NAME FROM CLASS INNER JOIN CLASS_EQUIPMENT ON CLASS.CID = CLASS_EQUIPMENT.UCID INNER JOIN EQUIPMENT ON CLASS_EQUIPMENT.UEID = EQUIPMENT.EID")
    
    class_equipment = cursor.fetchall()
    cursor.execute("SELECT CID, CNAME FROM CLASS")
    classes = cursor.fetchall()
    return render_template("display_class_equipment.html", class_equipment=class_equipment, classes=classes)
