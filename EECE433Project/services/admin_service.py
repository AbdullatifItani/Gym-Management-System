from flask import request, redirect, render_template


def admin():
    if request.method == "POST":
        if request.form.get("action") == "create_staff":
            return redirect("/create_staff")
        elif request.form.get("action") == "create_class":
            return redirect("/create_class")
    return render_template('admin_panel.html')
