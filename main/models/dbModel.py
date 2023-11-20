from main import db, app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func
import secrets

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(255), nullable=False)
    department  = db.Column(db.String(255), nullable=False) #LEAD
    subDepartment = db.Column(db.String(255), nullable=False) #SUPPORT
    status = db.Column(db.String(255), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(255), unique=True, nullable=False)

class UsersK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(255), unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=False)



class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), unique=True, nullable=False)

class Subprogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=False)

# ----------------------- Upload Files ------------------------------------
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

class CPF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

class CESAP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

class CNA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

# For pending projects

class Pending_project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(255), nullable=False)
    department  = db.Column(db.String(255), nullable=False)
    subDepartment = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    pending = db.Column(db.String(255), nullable=False)

class CPFp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

class CESAPp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

class CNAp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255), nullable=False) 
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

# --------------------- TODO: MULTI-IMAGES UPLOAD ----------------------

# Create the database tables
with app.app_context():
    db.create_all()

###################### QUERIES #########################

def multiple_insert():
    # Create a list of Program instances
    program_insert = [
        Program(program='Literacy'),
        Program(program='Socio-economic'),
        Program(program='Environmental Stewardship'),
        Program(program='Health and Wellness'),
        Program(program='Cultural Enhancement'),
        Program(program='Values Formation'),
        Program(program='Disaster Management'),
        Program(program='Gender and Development'),
    ]

    # Create a list of Role instances
    role_insert = [
        Role(role='Admin'),
        Role(role='Coordinator')
    ]

    # Add the program records to the session and commit
    for program in program_insert:
        db.session.add(program)

    # Add the role records to the session and commit
    for role in role_insert:
        db.session.add(role)

    db.session.commit()
    
def insert_community():
    community = 'Community1'
    program = 'Literacy'
    subprogram = 'Sub-Literacy'
    start_date = datetime.strptime('2023-10-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2023-11-01', '%Y-%m-%d').date()
    week = 2
    totalWeek = 10
    user = 'Admin'
    department = 'Department'
    subDepartment = 'Sub-department'
    status = 'Ongoing'
   
    community_insert = Community(community=community,program=program,subprogram=subprogram, start_date=start_date,
    end_date=end_date, week=week, totalWeek=totalWeek, user=user, department=department, subDepartment=subDepartment, status=status )
    if community_insert:
        # If a row with the specified program value is found, delete it
        db.session.add(community_insert)
        db.session.commit()

def insert_user():
    username = 'admin11'
    firstname = 'Emerson'
    lastname = 'Martinez'
    password = '123'
    role = 'Admin'
    program = 'CESU1'
    birthday = datetime.strptime('2023-11-27', '%Y-%m-%d').date()
    
    user_insert = UsersK(username=username,firstname=firstname,lastname=lastname, password=password,
    role=role, program=program, birthday=birthday)
    if user_insert:
        # If a row with the specified program value is found, delete it
        db.session.add(user_insert)
        db.session.commit()

def delete_subprogram():
 # Delete all records in the Subprogram table
    Subprogram.query.delete()
    db.session.commit()

def delete_pending_files():
 # Delete all records in the Subprogram table
    CNAp.query.delete()
    CPFp.query.delete()
    CESAPp.query.delete()
    Pending_project.query.delete()
    db.session.commit()

def delete_CPF():
 # Delete all records in the Subprogram table
    CPF.query.delete()
    db.session.commit()
def delete_CNA():
 # Delete all records in the Subprogram table
    CNA.query.delete()
    db.session.commit()
def delete_CESAP():
 # Delete all records in the Subprogram table
    CESAP.query.delete()
    db.session.commit()

@app.route('/db')
def initialize_database():
    #delete_subprogram()
    #multiple_insert()
    #insert_user()
    #delete_pending_files()
    #delete_CNA()
    #delete_CESAP()
    #delete_CPF()
    
    return 'Program.'

@app.route('/test')
def display_community_data():
    CPF_data = CPF.query.all()
    CESAP_data = db.session.query(CESAP).all()
    subprogram_data = db.session.query(Subprogram).all()
    # Query and retrieve all records from the "community" table
    all_community_data = db.session.query(Community).all()
    CNA_data = CNA.query.all()
    Pending_project_data = Pending_project.query.all()
    CesuUser_data = UsersK.query.all()
    CPFp_data = CPFp.query.all()
    CESAPp_data = CESAPp.query.all()
    CNAp_data = CNAp.query.all()
    return render_template('test.html', community_data=all_community_data, CPF_data=CPF_data, CESAP_data=CESAP_data, subprogram_data=subprogram_data,CNA_data=CNA_data, Pending_project_data = Pending_project_data, CPFp_data=CPFp_data, CESAPp_data=CESAPp_data,CNAp_data=CNAp_data , CesuUser_data = CesuUser_data  )
