from flask import Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g, redirect
from main.models.dbModel import User, Community, Program, Subprogram, Role, Upload, CPF, CESAP, CNA, Pending_project, CPFp, CESAPp, CNAp
from main import db
from main import Form
from flask import Response
from datetime import datetime
from sqlalchemy import func, case

coordinator_route = Blueprint('coordinator', __name__)

@coordinator_route.route("/coordinator_dashboard")
def coordinator_dashboard():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("cDashboard.html")

def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = User.query.get(session['user_id'])
        if user:
            return user.firstname, user.role, user.program
    return None, None
    
@coordinator_route.before_request
def before_request():
    g.current_user, g.current_role, g.current_program = get_current_user()

@coordinator_route.context_processor
def inject_current_user():
    current_program_coordinator = g.current_program
    return dict(current_user=g.current_user, current_role=g.current_role, current_program=g.current_program)

@coordinator_route.route("/cClear_session")
def cClear_session():
    session.clear()
    return redirect(url_for('dbModel.login'))

##################  FOR COORDINATOR  #######################
@coordinator_route.route('/cCoordinator')
def cCoordinator():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("cCoordinator.html")

##################  FOR COMMUNITY CRUD  #######################
@coordinator_route.route("/cGet_community_data", methods=['GET'])
def cGet_community_data():
    try:
        # Retrieve the "program" parameter from the query string
        program = request.args.get("program")

        if program:
            community_data = [
                {
                    'community': record.community,
                    'program': record.program,
                    'subprogram': record.subprogram,
                    'week': record.week,
                    'totalWeek': record.totalWeek,
                    'user': record.user,
                    'department': record.department,
                    'subDepartment': record.subDepartment,
                    'start_date': record.start_date,
                    'end_date': record.end_date,
                    'status': record.status
                }
                for record in Community.query.filter_by(program=g.current_program).all()
            ]
            if community_data:
                return jsonify(community_data)
            else:
                # Handle the case when no data is found
                return jsonify({'message': 'No data found for the program.'}), 200
          
        else:
            # Handle the case when "program" is not provided
            return make_response("Program not specified", 400)


    except Exception as e:
        # Log the error for debugging
        print(str(e))
        return make_response("Internal Server Error", 500)

@coordinator_route.route("/cCommunity_data_list")
def cCommunity_data_list():
    try:
        community_data = [
            {
                    'community': record.community,
                    'program': record.program,
                    'subprogram': record.subprogram,
                    'week': record.week,
                    'totalWeek': record.totalWeek,
                    'user': record.user,
                    'department': record.department,
                    'subDepartment': record.subDepartment,
                    'status': record.status
            }
                for record in Community.query.filter_by(program=g.current_program).all()
            ]
        return jsonify(community_data)
    except Exception as e:
        # Log the error for debugging
        print(str(e))
        return make_response("Internal Server Error", 500)


@coordinator_route.route("/cManage_community")
def cManage_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Community.query.filter_by(program=g.current_program).all()

    return render_template("cCommunity.html", community = all_data)


# Function to convert date strings to Python date objects
def convert_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date() 

@coordinator_route.route("/cAdd_community", methods=["POST"])
def cAdd_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        community = request.form.get("community")
        program = request.form.get("program")
        subprogram = request.form.get("subprogram")
        start_date1 = request.form.get("start_date")
        end_date1 = request.form.get("end_date")
        week = 0
        totalWeek = request.form.get("totalWeek")
        user = request.form.get("user")
        department = request.form.get("lead")
        subDepartment = request.form.get("support")
        status = "Ongoing"
        pending = "pending"

        #Convert date
        start_date = convert_date(start_date1)
        end_date = convert_date(end_date1)

         # Access uploaded files
        cpf_file = request.files['CPF']
        cesap_file = request.files['CESAP']
        cna_file = request.files['CNA']
      

        existing_community = Pending_project.query.filter_by(community=community, program = program, subprogram=subprogram).first()

        if existing_community is None:
            new_community = Pending_project(community=community, program=program, subprogram=subprogram, start_date=start_date,
            end_date=end_date, week=week, totalWeek=totalWeek, user=user, department=department, subDepartment=subDepartment, status=status, pending = pending)

            db.session.add(new_community)
            db.session.commit()
        else:
            return redirect(url_for('coordinator.cManage_community'))
        
        if cpf_file:
            cpf_data = cpf_file.read()
            cpf_record = CPFp(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cpf_file.filename,
                data=cpf_data
            )
            db.session.add(cpf_record)
            db.session.commit()

        if cesap_file: 
            cesap_data = cesap_file.read()
            cesap_record = CESAPp(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cesap_file.filename,
                data=cesap_data
            )
            db.session.add(cesap_record)
            db.session.commit()

        if cna_file:
            cna_data = cna_file.read()
            cna_record = CNAp(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cna_file.filename,
                data=cna_data
            )
            db.session.add(cna_record)
            db.session.commit()

        flash('New community project added!', 'add_community')
        return redirect(url_for('coordinator.cManage_community'))
       
    return redirect(url_for('coordinator.cManage_community'))


############# UPDATE WEEK BASED FROM Subprogram ##############

@coordinator_route.route('/cUpdate_week', methods=['POST'])
def cUpdate_week():
    data = request.get_json()
    community = data['community']
    subprogram = data['subprogram']
    totalCheckboxes = data['totalCheckboxes']
    program = data['program']

    # Query the database to get records with the specified subprogram
    communities = Community.query.filter_by(program=program, subprogram=subprogram).all()

    for community in communities:
        # Update the "week" column to match the totalCheckboxes
        community.week = totalCheckboxes
    db.session.commit()
    return jsonify({'message': 'Week column updated for the specified subprogram.'})

############# UPDATE Status BASED FROM Subprogram ##############
@coordinator_route.route('/cUpdate_status', methods=['POST'])
def cUpdate_status():
    data = request.get_json()
    community = data['community']
    subprogram = data['subprogram']
    program = data['program']
    status = data['status']

    # Query the database to get records with the specified subprogram
    communities = Community.query.filter_by(program=program, subprogram=subprogram).all()

    for community in communities:
        community.status = status
    db.session.commit()
    return jsonify({'message': 'Week column updated for the specified subprogram.'})


#display kaakbay program and coordinator
def cGet_ongoing_count(session, program_name):
    result = db.session.query(
        Community.program,
        func.sum(case((Community.status == 'Ongoing', 1), else_=0)).label('ongoing_count')
    ).filter(Community.program == program_name).group_by(Community.program).all()
    
    if result:
        return result[0][1]
    else:
        return 0

def cGet_completed_count(session, program_name):
    result = db.session.query(
        Community.program,
        func.sum(case((Community.status == 'Completed', 1), else_=0)).label('completed_count')
    ).filter(Community.program == program_name).group_by(Community.program).all()
    
    if result:
        return result[0][1]
    else:
        return 0

############# changepassword ##############
@coordinator_route.route("/cChange_password")
def cChange_password():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
   
    return render_template("cChange_password.html")

############# changepassword ##############
############# changepassword ##############
@coordinator_route.route("/cNew_password", methods=["GET", "POST"])
def cNew_password():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    if request.method == "POST":
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user = User.query.filter_by(id=session['user_id'], password=old_password).first()
        if ' ' in new_password:
            flash('Password cannot contain spaces.', 'newpassword_space')
            return redirect(url_for('coordinator.cChange_password'))
        if user:
            if new_password == confirm_password:
                user.password = new_password
                db.session.commit()
                flash('Password successfully changed.', 'new_password')
                return redirect(url_for('coordinator.cChange_password'))
            else:
                flash('New password and confirmation do not match.', 'not_match')
        else:
            flash('Wrong old password.', 'wrong_old')
    return redirect(url_for('coordinator.cChange_password'))