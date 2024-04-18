from main import db, app
from flask_migrate import Migrate
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func
import secrets

"""
flask db init

flask db migrate -m "budget_type column added"
flask db upgrade


flask db downgrade

"""

migrate = Migrate(app, db)

class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    user = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=True)
    activity = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    subprogram = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)  # LEAD
    subDepartment = db.Column(db.String(255), nullable=True)  # SUPPORT
    status = db.Column(db.String(255), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    cna = db.Column(db.LargeBinary, nullable=True)
    cpf = db.Column(db.LargeBinary, nullable=True)
    cesap = db.Column(db.LargeBinary, nullable=True)
    cna_filename = db.Column(db.String(255), nullable=True)
    cpf_filename = db.Column(db.String(255), nullable=True)
    cesap_filename = db.Column(db.String(255), nullable=True)
    department_A = db.Column(db.String(255), nullable=True)
    volunteer = db.Column(db.Integer, nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    otp = db.Column(db.String(6), nullable=True)
    otp_timestamp = db.Column(db.DateTime, nullable=True)
    program = db.Column(db.String(255), unique=True, nullable=True)
    department_A = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    mobile_number = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.LargeBinary, nullable=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_A = db.Column(db.String(255), nullable=True)
    department_F = db.Column(db.String(255), nullable=True)
    
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), unique=True, nullable=True)

class Subprogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    subprogram = db.Column(db.String(255), nullable=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=True)

# ----------------------- Upload Files ------------------------------------
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

# For pending projects
class Pending_project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    subprogram = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)  # LEAD
    subDepartment = db.Column(db.String(255), nullable=True)  # SUPPORT
    status = db.Column(db.String(255), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    cna = db.Column(db.LargeBinary, nullable=True)
    cpf = db.Column(db.LargeBinary, nullable=True)
    cesap = db.Column(db.LargeBinary, nullable=True)
    cna_filename = db.Column(db.String(255), nullable=True)
    cpf_filename = db.Column(db.String(255), nullable=True)
    cesap_filename = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.String(255), nullable=True)
    department_A = db.Column(db.String(255), nullable=True)
    volunteer = db.Column(db.Integer, nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    subprogram = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)  # LEAD
    subDepartment = db.Column(db.String(255), nullable=True)  # SUPPORT
    status = db.Column(db.String(255), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    cna = db.Column(db.LargeBinary, nullable=True)
    cpf = db.Column(db.LargeBinary, nullable=True)
    cesap = db.Column(db.LargeBinary, nullable=True)
    cna_filename = db.Column(db.String(255), nullable=True)
    cpf_filename = db.Column(db.String(255), nullable=True)
    cesap_filename = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.String(255), nullable=True)
    department_A = db.Column(db.String(255), nullable=True)
    volunteer = db.Column(db.Integer, nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)

class Archive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    subprogram = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)  # LEAD
    subDepartment = db.Column(db.String(255), nullable=True)  # SUPPORT
    status = db.Column(db.String(255), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    cna = db.Column(db.LargeBinary, nullable=True)
    cpf = db.Column(db.LargeBinary, nullable=True)
    cesap = db.Column(db.LargeBinary, nullable=True)
    cna_filename = db.Column(db.String(255), nullable=True)
    cpf_filename = db.Column(db.String(255), nullable=True)
    cesap_filename = db.Column(db.String(255), nullable=True)
    department_A = db.Column(db.String(255), nullable=True)
    volunteer = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(255), nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)

# FOR FUNDRAISING TABLE
class Fundraising(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    coordinator = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    proposed_date = db.Column(db.Date, nullable=True)
    target_date = db.Column(db.Date, nullable=True)
    venue = db.Column(db.String(255), nullable=True)
    event_organizer = db.Column(db.String(255), nullable=True)
    lead_proponent = db.Column(db.String(255), nullable=True)
    contact_details = db.Column(db.String(255), nullable=True)
    donation_type = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)

class Pending_fund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    coordinator = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    proposed_date = db.Column(db.Date, nullable=True)
    target_date = db.Column(db.Date, nullable=True)
    venue = db.Column(db.String(255), nullable=True)
    event_organizer = db.Column(db.String(255), nullable=True)
    lead_proponent = db.Column(db.String(255), nullable=True)
    contact_details = db.Column(db.String(255), nullable=True)
    donation_type = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.String(255), nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)

class Archive_fund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    coordinator = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    proposed_date = db.Column(db.Date, nullable=True)
    target_date = db.Column(db.Date, nullable=True)
    venue = db.Column(db.String(255), nullable=True)
    event_organizer = db.Column(db.String(255), nullable=True)
    lead_proponent = db.Column(db.String(255), nullable=True)
    contact_details = db.Column(db.String(255), nullable=True)
    donation_type = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    coordinator_id = db.Column(db.Integer, nullable=True)

class Donor_cash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, nullable=True)
    program = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    donation = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

class Donor_cash_total(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, nullable=True)
    program = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    donation = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)
  
class Donor_inkind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, nullable=True)
    program = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    donation = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

class Donor_inkind_total(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, nullable=True)
    program = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    donation = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)
# --------------------- LOGS ------------------------#
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userlog = db.Column(db.String(255), nullable=True)
    action = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=True)

# FOR BUDGET
class Cash_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    total_cash = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)
    
class Total_budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

class Current_total_budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

class Program_cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)
    total_cost = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

########### ALL BUDGET (HINDI NABABAWASAN) ############
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_type = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

########### ALL BUDGET (NABABAWASAN) ############
class Current_Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_type = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

########### ALL BUDGET (HINDI NADADAGDAGAN) ############
class Budget_cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)
    total_cost = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)
    
class Budget_program_cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    subprogram = db.Column(db.String(255), nullable=True)
    community = db.Column(db.String(255), nullable=True)
    budget_type = db.Column(db.String(255), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    balance = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)
    
class Unused_budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=True)
    total = db.Column(db.Integer, nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    balance = db.Column(db.Integer, nullable=True)
    current = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)

# --------------------- TODO: MULTI-IMAGES UPLOAD ----------------------

# Create the database tables
with app.app_context():
    db.create_all()

###################### QUERIES #########################
def multiple_insert():
    # Create a list of Program instances
    program_insert = [
        Program(program="Literacy"),
        Program(program="Socio-economic"),
        Program(program="Environmental Stewardship"),
        Program(program="Health and Wellness"),
        Program(program="Cultural Enhancement"),
        Program(program="Values Formation"),
        Program(program="Disaster Management"),
        Program(program="Gender and Development"),
    ]

    # Create a list of Role instances
    role_insert = [Role(role="Coordinator")]

    # Add the program records to the session and commit
    for program in program_insert:
        db.session.add(program)

    # Add the role records to the session and commit
    for role in role_insert:
        db.session.add(role)

    db.session.commit()


def insert_community():
    community = "Bubukal"
    program = "Literacy"
    subprogram = "Sub-Literacy"
    start_date = datetime.strptime("2023-10-01", "%Y-%m-%d").date()
    end_date = datetime.strptime("2023-11-01", "%Y-%m-%d").date()
    week = 2
    totalWeek = 10
    user = "Admin"
    department = "Department"
    subDepartment = "Sub-department"
    status = "Ongoing"
    budget = 100

    community_insert = Community(
        community=community,
        program=program,
        subprogram=subprogram,
        start_date=start_date,
        end_date=end_date,
        week=week,
        totalWeek=totalWeek,
        user=user,
        department=department,
        subDepartment=subDepartment,
        status=status,
        budget=budget,
    )

    if community_insert:
        # If a row with the specified program value is found, delete it
        db.session.add(community_insert)
        db.session.commit()


def insert_pending():
    community = "Bubukal"
    program = "Literacy"
    subprogram = "Sub-Literacy"
    start_date = datetime.strptime("2023-10-01", "%Y-%m-%d").date()
    end_date = datetime.strptime("2023-11-01", "%Y-%m-%d").date()
    week = 2
    totalWeek = 10
    user = "Admin"
    department = "Department"
    subDepartment = "Sub-department"
    status = "Pending"
    budget = 100

    community_insert = Pending_project(
        community=community,
        program=program,
        subprogram=subprogram,
        start_date=start_date,
        end_date=end_date,
        week=week,
        totalWeek=totalWeek,
        user=user,
        department=department,
        subDepartment=subDepartment,
        status=status,
        budget=budget,
    )

    if community_insert:
        # If a row with the specified program value is found, delete it
        db.session.add(community_insert)
        db.session.commit()


def insert_userx():
    username = "admin2"
    firstname = "Joselle2"
    lastname = "Banocnoc2"
    email = "1ls1ucesu50@gmail.com"
    program = "CESU"
    password = "@123ABCabc"
    role = "Admin"

    user_insert = Users(
        username=username,
        firstname=firstname,
        lastname=lastname,
        program=program,
        email=email,
        password=password,
        role=role,
    )
    db.session.add(user_insert)
    db.session.commit()

    username = "admin"
    firstname = "Joselle1"
    lastname = "Banocnoc1"
    email = "1ls1ucesu501@gmail.com"
    program = "CESU "
    password = "@123ABCabc"
    role = "Admin"

    user_insert = Users(
        username=username,
        firstname=firstname,
        lastname=lastname,
        program=program,
        email=email,
        password=password,
        role=role,
    )
    db.session.add(user_insert)
    db.session.commit()
    
    username = "BOR"
    firstname = "LU"
    lastname = "BOR"
    email = "BOR@gmail.com"
    program = "BOR"
    password = "@123ABCabc"
    role = "Coordinator"

    user_insert = Users(
        username=username,
        firstname=firstname,
        lastname=lastname,
        program=program,
        email=email,
        password=password,
        role=role,
    )
    db.session.add(user_insert)
    db.session.commit()


def delete_data():
    # Delete all records in the Subprogram table
    data = Community.query.filter_by(user="Admin").first()

    db.session.delete(data)
    db.session.commit()


@app.route("/db")
def initialize_database():
    # multiple_insert()
    # insert_community()
    # insert_userx()
    # insert_pending()
    # delete_data()

    return "Program."


@app.route("/test")
def display_community_data():
    subprogram_data = db.session.query(Subprogram).all()
    all_community_data = db.session.query(Community).all()
    Pending_project_data = Pending_project.query.all()
    User = Users.query.all()
    UserLogs = Logs.query.all()
    planner = Plan.query.all()
    department = Department.query.all()
    archive_project = db.session.query(Archive).all()
    return render_template(
        "test.html",
        planner=planner,
        UserLogs=UserLogs,
        community_data=all_community_data,
        subprogram_data=subprogram_data,
        Pending_project_data=Pending_project_data,
        Users=User,
        archive_project=archive_project,
        department=department,
    )
