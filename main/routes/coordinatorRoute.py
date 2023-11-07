from flask import Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g, redirect
from main.models.dbModel import User, Community, Program, Subprogram, Role, Upload, CPF, CESAP, CNA
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
    return dict(current_user=g.current_user, current_role=g.current_role, current_program=g.current_program)

@coordinator_route.route("/cClear_session")
def cClear_session():
    session.clear()
    return redirect(url_for('dbModel.login'))


##################  FOR COORDINATOR  #######################
@coordinator_route.route('/cCoordinator/<data>')
def cCoordinator(data):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("cCoordinator.html", data=data)

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
                for record in Community.query.filter_by(program=program).all()
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
                for record in Community.query.all()
            ]
        return jsonify(community_data)
    except Exception as e:
        # Log the error for debugging
        print(str(e))
        return make_response("Internal Server Error", 500)


@coordinator_route.route("/cManage_community")
def cManage_community():
    form = Form()
    placeholder_choice = ("", "-- Select Program --")
    form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
    form.program.default = ""
    form.process()
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Community.query.all()
    program8 = Program.query.all()
    user1 = User.query.all()
    return render_template("cCommunity.html", community = all_data, form=form, program8=program8, user1 = user1)

#fetch for user
@coordinator_route.route("/cSubprogram1/<get_program>")
def get_program(get_program):
    sub = User.query.filter_by(program=get_program).all()
    subArray = [user.username for user in sub]  
    return jsonify({'user': subArray})

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

        #Convert date
        start_date = convert_date(start_date1)
        end_date = convert_date(end_date1)

         # Access uploaded files
        cpf_file = request.files['CPF']
        cesap_file = request.files['CESAP']
        cna_file = request.files['CNA']
      

        existing_community = Community.query.filter_by(user= user, program = program, subprogram=subprogram).first()

        if existing_community is None:
            new_community = Community(community=community, program=program, subprogram=subprogram, start_date=start_date,
            end_date=end_date, week=week, totalWeek=totalWeek, user=user, department=department, subDepartment=subDepartment, status=status)

            db.session.add(new_community)
            db.session.commit()
        else:
            return redirect(url_for('coordinator.cManage_community'))

        #FOR SUBPROGRAM
        existing_subprogram = Subprogram.query.filter_by(program = program, subprogram=subprogram).first()

        if existing_subprogram is None:
            new_subprogram = Subprogram(program=program, subprogram=subprogram)

            db.session.add(new_subprogram)
            db.session.commit()
        else:
            return redirect(url_for('coordinator.cManage_community'))
        
        
        if cpf_file and cesap_file and cna_file :
            # Read the file data
            cpf_data = cpf_file.read()
            cesap_data = cesap_file.read()
            cna_date = cna_file.read()

            # Create records in the database
            cpf_record = CPF(
                program=program,
                subprogram=subprogram,
                filename=cpf_file.filename,
                data=cpf_data
            )

            cesap_record = CESAP(
                program=program,
                subprogram=subprogram,
                filename=cesap_file.filename,
                data=cesap_data
            )

            cna_record = CNA(
                program=program,
                subprogram=subprogram,
                filename=cesap_file.filename,
                data=cesap_data
            )

            db.session.add(cpf_record)
            db.session.add(cesap_record)
            db.session.add(cna_record)
            db.session.commit()
        return redirect(url_for('coordinator.cManage_community'))
       
    return redirect(url_for('coordinator.cManage_community'))


############# UPDATE WEEK BASED FROM Subprogram ##############

@coordinator_route.route('/cUpdate_week', methods=['POST'])
def cUpdate_week():
    data = request.get_json()
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


@coordinator_route.route("/cKaakbay_program")
def cKaakbay_program():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    literacy_program_data = User.query.filter_by(program="Literacy").first()
    economic_program_data = User.query.filter_by(program="Socio-economic").first()
    environmental_program_data = User.query.filter_by(program="Environmental Stewardship").first()
    health_program_data = User.query.filter_by(program="Health and Wellness").first()
    cultural_program_data = User.query.filter_by(program="Cultural Enhancement").first()
    values_program_data = User.query.filter_by(program="Values Formation").first()
    disaster_program_data = User.query.filter_by(program="Disaster Management").first()
    gender_program_data = User.query.filter_by(program="Gender and Development").first()

    literacy_firstname = literacy_program_data.firstname if literacy_program_data else None
    literacy_lastname = literacy_program_data.lastname if literacy_program_data else None

    economic_firstname = economic_program_data.firstname if economic_program_data else None
    economic_lastname = economic_program_data.lastname if economic_program_data else None

    environmental_firstname = environmental_program_data.firstname if environmental_program_data else None
    environmental_lastname = environmental_program_data.lastname if environmental_program_data else None

    health_firstname = health_program_data.firstname if health_program_data else None
    health_lastname = health_program_data.lastname if health_program_data else None

    cultural_firstname = cultural_program_data.firstname if cultural_program_data else None
    cultural_lastname = cultural_program_data.lastname if cultural_program_data else None

    values_firstname = values_program_data.firstname if values_program_data else None
    values_lastname = values_program_data.lastname if values_program_data else None

    disaster_firstname = disaster_program_data.firstname if disaster_program_data else None
    disaster_lastname = disaster_program_data.lastname if disaster_program_data else None

    gender_firstname = gender_program_data.firstname if gender_program_data else None
    gender_lastname = gender_program_data.lastname if gender_program_data else None



    program_names = ['Literacy', 'Socio-economic', 'Environmental Stewardship', 'Health and Wellness', 'Cultural Enhancement', 'Values Formation', 'Disaster Management', 'Gender and Development' ]
    program_ongoing_counts = {}
    program_completed_counts = {}

    for program_name in program_names:
        ongoing_count = cGet_ongoing_count(session, program_name)
        program_ongoing_counts[program_name] = ongoing_count
        
    for program_name in program_names:
        completed_count = cGet_completed_count(session, program_name)
        program_completed_counts[program_name] = completed_count
    
    return render_template("cKaakbay_program.html", literacy_firstname=literacy_firstname, literacy_lastname=literacy_lastname,
                      economic_firstname=economic_firstname, economic_lastname=economic_lastname,
                      environmental_firstname=environmental_firstname, environmental_lastname=environmental_lastname,
                      health_firstname=health_firstname, health_lastname=health_lastname,
                      cultural_firstname=cultural_firstname, cultural_lastname=cultural_lastname,
                      values_firstname=values_firstname, values_lastname=values_lastname,
                      disaster_firstname=disaster_firstname, disaster_lastname=disaster_lastname,
                      gender_firstname=gender_firstname, gender_lastname=gender_lastname,
                      literacy_ongoing_count = program_ongoing_counts.get('Literacy', 0),
                      literacy_completed_count = program_completed_counts.get('Literacy', 0),
                      socio_ongoing_count = program_ongoing_counts.get('Socio-economic', 0),
                      socio_completed_count = program_completed_counts.get('Socio-economic', 0),
                      environmental_ongoing_count = program_ongoing_counts.get('Environmental Stewardship', 0),
                      environmental_completed_count = program_completed_counts.get('Environmental Stewardship', 0),
                      health_ongoing_count = program_ongoing_counts.get('Health and Wellness', 0),
                      health_completed_count = program_completed_counts.get('Health and Wellness', 0),
                      cultural_ongoing_count = program_ongoing_counts.get('Cultural Enhancement', 0),
                      cultural_completed_count = program_completed_counts.get('Cultural Enhancement', 0),
                      values_ongoing_count = program_ongoing_counts.get('Values Formation', 0),
                      values_completed_count = program_completed_counts.get('Values Formation', 0),
                      disaster_ongoing_count = program_ongoing_counts.get('Disaster Management', 0),
                      disaster_completed_count = program_completed_counts.get('Disaster Management', 0),
                      gender_ongoing_count = program_ongoing_counts.get('Gender and Development', 0),
                      gender_completed_count = program_completed_counts.get('Gender and Development', 0),
                      )


############# changepassword ##############
@coordinator_route.route("/cChange_password")
def cChange_password():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
   
    return render_template("cChange_password.html")

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

        user = User.query.filter_by(id=session['user_id'], password = old_password).first()

        if user:
            if new_password == confirm_password:
                user.password = new_password
                db.session.commit()
                flash('Password successfully changed.', 'success')
                return render_template("cChange_password.html")
            else:
                flash('New password and confirmation do not match.', 'error')
        else:
            flash('Invalid current password.', 'error')
    return render_template("cChange_password.html")