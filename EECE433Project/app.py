from flask import Flask, render_template, session, redirect
# from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# bcrypt = Bcrypt(app)

from .db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

conn = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

from EECE433Project.services import admin_service
from EECE433Project.services.registered_service import assign_registered_service, delete_registered_service
from EECE433Project.services.session_service import assign_session_service, delete_session_service
from EECE433Project.services.staff_service import create_staff_service, update_staff_service, delete_staff_service
from EECE433Project.services.class_equipment_service import assign_class_equipment_service, \
    delete_class_equipment_service
from EECE433Project.services.equipment_service import create_equipment_service, delete_equipment_service, \
    update_equipment_service
from EECE433Project.services.class_service import create_class_service, update_class_service, delete_class_service
from EECE433Project.services.member_gym_session_service import assign_member_gym_session_service, \
    delete_member_gym_session_service
from EECE433Project.services.gym_session_service import create_gym_session_service, delete_gym_session_service
from .services.package_service import create_package_service, update_package_service, delete_package_service
from EECE433Project.services.member_package_service import assign_member_package_service, delete_member_package_service
from EECE433Project.services.member_service import create_member_service, update_member_contact_service, \
    delete_member_service
from EECE433Project.services.emergency_contact_service import assign_emergency_contact_service, \
    update_emergency_contact_service, delete_emergency_contact_service
from EECE433Project.services.auth_service import login_service, register_service
from EECE433Project.services.logs_service import assign_logs_service, delete_logs_service
from EECE433Project.services.review_service import create_review_service, delete_review_service
from EECE433Project.helper_functions import admin_required


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/admin')
@admin_required
def admin():
    return admin_service.admin()


# Auth Service Start #


@app.route('/register', methods=["GET", "POST"])
def register():
    return register_service.register(conn)


@app.route('/login', methods=["GET", "POST"])
def login():
    return login_service.login(conn)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


# Auth Service End #
# Member Service Start #


@app.route('/create_member', methods=["GET", "POST"])
@admin_required
def create_member():
    return create_member_service.create_member(conn)


@app.route('/update_member_contact', methods=["GET", "POST"])
@admin_required
def update_member_contact():
    return update_member_contact_service.update_member_contact(conn)


@app.route('/delete_member', methods=["GET", "POST"])
@admin_required
def delete_member():
    return delete_member_service.delete_member(conn)


# Member Service End #
# Emergency Contact Service Start #


@app.route('/assign_emergency_contact', methods=["GET", "POST"])
@admin_required
def assign_emergency_contact():
    return assign_emergency_contact_service.assign_emergency_contact(conn)


@app.route('/update_emergency_contact', methods=["GET", "POST"])
@admin_required
def update_emergency_contact():
    return update_emergency_contact_service.update_emergency_contact(conn)


@app.route('/delete_emergency_contact', methods=["GET", "POST"])
@admin_required
def delete_emergency_contact():
    return delete_emergency_contact_service.delete_emergency_contact(conn)


# Emergency Contact Service End #
# Package Service Start #


@app.route('/create_package', methods=["GET", "POST"])
@admin_required
def create_package():
    return create_package_service.create_package(conn)


@app.route('/update_package', methods=["GET", "POST"])
@admin_required
def update_package():
    return update_package_service.update_package(conn)


@app.route('/delete_package', methods=["GET", "POST"])
@admin_required
def delete_package():
    return delete_package_service.delete_package(conn)


# Package Service End #
# Member Package Service Start #


@app.route('/assign_member_package', methods=["GET", "POST"])
@admin_required
def assign_member_package():
    return assign_member_package_service.assign_member_package(conn)


@app.route('/delete_member_package', methods=["GET", "POST"])
@admin_required
def delete_member_package():
    return delete_member_package_service.delete_member_package(conn)


# Member Package Service End #
# Review Service Start #


@app.route('/create_review', methods=["GET", "POST"])
@admin_required
def create_review():
    return create_review_service.create_review(conn)


@app.route('/delete_review', methods=["GET", "POST"])
@admin_required
def delete_review():
    return delete_review_service.delete_review(conn)


# Review Service End #
# Gym Session Service Start #


@app.route('/create_gym_session', methods=["GET", "POST"])
@admin_required
def create_gym_session():
    return create_gym_session_service.create_gym_session(conn)


@app.route('/delete_gym_session', methods=["GET", "POST"])
@admin_required
def delete_gym_session():
    return delete_gym_session_service.delete_gym_session(conn)


# Gym Session Service End #
# Member Gym Session Service Start #


@app.route('/assign_member_gym_session', methods=["GET", "POST"])
@admin_required
def assign_member_gym_session():
    return assign_member_gym_session_service.assign_member_gym_session(conn)


@app.route('/delete_member_gym_session', methods=["GET", "POST"])
@admin_required
def delete_member_gym_session():
    return delete_member_gym_session_service.delete_member_gym_session(conn)


# Member Gym Session Service End #
# Class Service Start #


@app.route('/create_class', methods=["GET", "POST"])
@admin_required
def create_class():
    return create_class_service.create_class(conn)


@app.route('/update_class', methods=["GET", "POST"])
@admin_required
def update_class():
    return update_class_service.update_class(conn)


@app.route('/delete_class', methods=["GET", "POST"])
@admin_required
def delete_class():
    return delete_class_service.delete_class(conn)


# Class Service End #
# Equipment Service Start #


@app.route('/create_equipment', methods=["GET", "POST"])
@admin_required
def create_equipment():
    return create_equipment_service.create_equipment(conn)


@app.route('/update_equipment', methods=["GET", "POST"])
@admin_required
def update_equipment():
    return update_equipment_service.update_equipment(conn)


@app.route('/delete_equipment', methods=["GET", "POST"])
@admin_required
def delete_equipment():
    return delete_equipment_service.delete_equipment(conn)


# Equipment Service End #
# Class Equipment Service Start #


@app.route('/assign_class_equipment', methods=["GET", "POST"])
@admin_required
def assign_class_equipment():
    return assign_class_equipment_service.assign_class_equipment(conn)


@app.route('/delete_class_equipment', methods=["GET", "POST"])
@admin_required
def delete_class_equipment():
    return delete_class_equipment_service.delete_class_equipment(conn)


# Class Equipment Service End #
# Staff Service Start #


@app.route('/create_staff', methods=["GET", "POST"])
@admin_required
def create_staff():
    return create_staff_service.create_staff(conn)


@app.route('/update_staff', methods=["GET", "POST"])
@admin_required
def update_staff():
    return update_staff_service.update_staff(conn)


@app.route('/delete_staff', methods=["GET", "POST"])
@admin_required
def delete_staff():
    return delete_staff_service.delete_staff(conn)


# Staff Service End #
# Logs Service Start #


@app.route('/assign_logs', methods=["GET", "POST"])
def assign_logs():
    return assign_logs_service.assign_logs(conn)


@app.route('/delete_logs', methods=["GET", "POST"])
@admin_required
def delete_logs():
    return delete_logs_service.delete_logs(conn)


# Logs Service End #
# Session Service Start #


@app.route('/assign_session', methods=["GET", "POST"])
def assign_session():
    return assign_session_service.assign_session(conn)


@app.route('/delete_session', methods=["GET", "POST"])
@admin_required
def delete_session():
    return delete_session_service.delete_session(conn)


# Session Service End #
# Registered Service Start #


@app.route('/assign_registered', methods=["GET", "POST"])
def assign_registered():
    return assign_registered_service.assign_registered(conn)


@app.route('/delete_registered', methods=["GET", "POST"])
@admin_required
def delete_registered():
    return delete_registered_service.delete_registered(conn)


# Registered Service End #


if __name__ == '__main__':
    app.run(debug=True)
