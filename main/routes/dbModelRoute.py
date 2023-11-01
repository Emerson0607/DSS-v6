from flask import Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g
from main.models.dbModel import User, Community, Program, Subprogram, Role, Upload, CPF, CESAP
from main import db
from main import Form
from flask import Response
from datetime import datetime


dbModel_route = Blueprint('dbModel', __name__)

@dbModel_route.route("/login", methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for('dbModel.dashboard'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dbModel.dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@dbModel_route.route("/admin_dashboard")
def dashboard():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("dashboard.html")


def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = User.query.get(session['user_id'])
        if user:
            return user.firstname, user.role
    return None, None
@dbModel_route.before_request
def before_request():
    g.current_user, g.current_role = get_current_user()

@dbModel_route.context_processor
def inject_current_user():
    return dict(current_user=g.current_user, current_role=g.current_role)


@dbModel_route.route("/clear_session")
def clear_session():
    session.clear()
    return redirect(url_for('dbModel.login'))

@dbModel_route.route("/result")
def programCSVresult():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return redirect(url_for('randomForest.programOneRow'))

#FOR USER CRUD

@dbModel_route.route("/manage_account")
def manage_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = User.query.all()
    role = Role.query.all()
    program8 = Program.query.all()
    return render_template("manage_account.html", users = all_data, role = role, program8=program8)

@dbModel_route.route("/add_account", methods=["POST"])
def add_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        role = request.form.get("role")
        program = request.form.get("program")
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            new_user = User(username=username, firstname=firstname, lastname=lastname, 
            password=password, role = role, program = program)
            try: 
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the account. Please try again.', 'error')
    return redirect(url_for('dbModel.manage_account'))

@dbModel_route.route('/edit_account', methods=['POST'])
def edit_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        user_id = request.form.get('id')
        new_username = request.form['new_username']
        new_firstname = request.form['new_firstname']
        new_lastname = request.form['new_lastname']
        new_password = request.form['new_password']
        new_role = request.form['new_role']
        new_program = request.form['new_program']
        
        user = User.query.get(user_id)
        
        if user:
            user.username = new_username
            user.firstname = new_firstname
            user.lastname = new_lastname
            user.password = new_password
            user.role = new_role
            user.program = new_program

            db.session.commit()
            flash('Account updated successfully!', 'success')
        else:
            flash('User not found. Please try again.', 'error')

        return redirect(url_for('dbModel.manage_account'))

@dbModel_route.route('/delete_account/<int:id>', methods=['GET'])
def delete_account(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    user = User.query.get(id)

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('dbModel.manage_account'))


##################  FOR COORDINATOR  #######################
@dbModel_route.route("/coordinator")
def coordinator():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("coordinator.html")


##################  FOR COMMUNITY CRUD  #######################
@dbModel_route.route("/get_community_data")
def get_community_data():
    try:
        community_data = [
        {
            'community': record.community,
            'program': record.program,
            'subprogram': record.subprogram,
            'week': record.week,
            'totalWeek': record.totalWeek,
            'user': record.user
        }
        for record in Community.query.all()
        ]
        return jsonify(community_data)
    except Exception as e:
        # Log the error for debugging
        print(str(e))
        return make_response("Internal Server Error", 500)

@dbModel_route.route("/manage_community")
def manage_community():
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
    return render_template("community.html", community = all_data, form=form, program8=program8, user1 = user1)

#fetch for user
@dbModel_route.route("/subprogram1/<get_program>")
def get_program(get_program):
    sub = User.query.filter_by(program=get_program).all()
    subArray = [user.username for user in sub]  
    return jsonify({'user': subArray})



# Function to convert date strings to Python date objects
def convert_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date() 


@dbModel_route.route("/add_community", methods=["POST"])
def add_community():
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
      

        existing_community = Community.query.filter_by(user= user, program = program, subprogram=subprogram).first()

        if existing_community is None:
            new_community = Community(community=community, program=program, subprogram=subprogram, start_date=start_date,
            end_date=end_date, week=week, totalWeek=totalWeek, user=user, department=department, subDepartment=subDepartment, status=status)

            db.session.add(new_community)
            db.session.commit()
        else:
            return redirect(url_for('dbModel.manage_community'))
        
        
        if cpf_file and cesap_file:
            # Read the file data
            cpf_data = cpf_file.read()
            cesap_data = cesap_file.read()

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

            db.session.add(cpf_record)
            db.session.add(cesap_record)
            db.session.commit()
        return redirect(url_for('dbModel.manage_community'))
       
    return redirect(url_for('dbModel.manage_community'))



@dbModel_route.route('/edit_community', methods=['POST'])
def edit_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        user_id = request.form.get('id')  # Get the user ID from the form
        new_community = request.form['new_community']
        new_program = request.form['new_program']
        new_subprogram = request.form['new_subprogram']
        new_week= request.form['new_week']
        new_totalWeek = request.form['new_totalWeek']
        new_user = request.form['new_user']
        
        # Query the user by ID
        user = Community.query.get(user_id)
        
        if user:
            # Update the user's information
            user.community = new_community
            user.program = new_program
            user.subprogram = new_subprogram
            user.week = new_week
            user.totalWeek = new_totalWeek
            user.user = new_user

            # Commit the changes to the database
            db.session.commit()
            flash('Account updated successfully!', 'success')
        else:
            flash('User not found. Please try again.', 'error')

        return redirect(url_for('dbModel.manage_community'))

@dbModel_route.route('/delete_community/<int:id>', methods=['GET'])
def delete_community(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    community = Community.query.get(id)
    program = request.args.get('program')
    subprogram = request.args.get('subprogram')

    if community:
        try:
            # Delete the user from the database
            db.session.delete(community)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')

     # First, find and delete records from the database
    cpf_record = CPF.query.filter_by(program=program, subprogram=subprogram).first()
    cesap_record = CESAP.query.filter_by(program=program, subprogram=subprogram).first()

    if cpf_record:
        # Delete the file associated with the CPF record
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cpf_record)
            db.session.commit()
            
            flash('File data and record deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()

    if cesap_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cesap_record)
            db.session.commit()
            
            flash('File data and record deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()

    db.session.commit()
    return redirect(url_for('dbModel.manage_community'))


############# UPDATE WEEK BASED FROM Subprogram ##############
# Flask Route
@dbModel_route.route('/update_week', methods=['POST'])
def update_week():
    data = request.get_json()
    subprogram = data['subprogram']
    totalCheckboxes = data['totalCheckboxes']

    # Query the database to get records with the specified subprogram
    communities = Community.query.filter_by(subprogram=subprogram).all()

    for community in communities:
        # Update the "week" column to match the totalCheckboxes
        community.week = totalCheckboxes
    db.session.commit()
    return jsonify({'message': 'Week column updated for the specified subprogram.'})

