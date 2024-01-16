from flask import Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g, redirect
from main.models.dbModel import User, Community, Program, Subprogram, Role, Upload, CPF, CESAP, CNA, Pending_project, CPFp, CESAPp, CNAp, CPFARCHIVE, CesuUserX
from main import db
from flask import Response
import secrets
from datetime import datetime, timedelta
from sqlalchemy import func, case
from mailbox import Message
from main import Form, app, mail
from flask_mail import Mail, Message

dbModel_route = Blueprint('dbModel', __name__)
token_store = {}
# Function to convert date strings to Python date objects
def convert_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()
    

@dbModel_route.route("/rec", methods=["GET", "POST"])
def rec():
    return render_template('password_recovery_email.html')

@dbModel_route.route("/send_recovery_mail", methods=['GET', 'POST'])
def send_recovery_mail():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email exists in the database
        user = CesuUserX.query.filter_by(email=email).first()

        if user:
            # Generate and store OTP in the database
            otp = secrets.token_hex(3)  # 6 characters in hex format
            user.otp = otp
            user.otp_timestamp = datetime.utcnow() + timedelta(minutes=5)  # Set expiration time to 5 minutes
            db.session.commit()

            # Send OTP via email
            send_mail(otp, email)

            return render_template('password_recovery.html', email=email)
        else:
            return "Email not found in the database."

    return render_template('password_recovery_request.html')

@dbModel_route.route("/recover_password", methods=['GET', 'POST'])
def recover_password():

    if request.method == "POST":
        email = request.form.get("email")
        otp_entered = request.form.get("otp")
        new_password = request.form.get("new_password")

        # Check if the email exists in the database
        user = CesuUserX.query.filter_by(email=email).first()

        if user:
            print(f"OTP Entered: {otp_entered}")
            print(f"Stored OTP: {user.otp}")
            print(f"OTP Timestamp: {user.otp_timestamp}")

            if user.otp == otp_entered:
                # Check if the OTP has not expired (within a 5-minute window)
                expiration_time = user.otp_timestamp + timedelta(minutes=5)
                if datetime.utcnow() < expiration_time:
                    # Update the password and reset OTP fields
                    user.password = new_password
                    user.otp = None
                    user.otp_timestamp = None
                    db.session.commit()
                    return "Success!"
                    #return redirect(url_for('dbModel.dashboard'))
                else:
                    return "OTP has expired. Please request a new one."
            else:
                return "Invalid OTP."

    return "Invalid request."



#For email
@dbModel_route.route("/send_mail")
def send_mail(otp, recipient_email):
    #OTP = "123456"
    #recipient_email = "martinezemerson52@gmail.com"
    sender_name = "LU-CESU"
    
    mail_message = Message(
            'Account Recovery', 
            sender =   (sender_name, 'emer22297@gmail.com'), 
            recipients = [recipient_email, 'emer22297@gmail.com'])
    mail_message.body = f"""
    Your One-Time Password (OTP): {otp}

    This OTP is valid for a single use and will expire shortly. 
    Do not share it with anyone for security reasons. 

    If you did not request this OTP or experience any issues, please contact our support team immediately. 

    Thank you for trusting us with your security.

    Best regards,
    CESU MIS Team
    """
    mail_message.html = f"""
    <html>
        <body>
            <p>Hi {recipient_email},</p>
            <p>Your One-Time Password (OTP): <strong>{otp}</strong></p>
            <p>This OTP is valid for a single use and will expire shortly. 
            Do not share it with anyone for security reasons.</p>
            <p>If you did not request this OTP or experience any issues, please contact our support team immediately.</p>
            <p>Thank you for trusting us with your security.</p>
            <h1 style="margin-top: 1rem;"></h1>
            <p><em>Best regards, CESU MIS Team</em></p>
        </body>
    </html>
    """
    mail.send(mail_message)
    return "Mail has sent"


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
            if user.role == 'Admin': #Admin
                flash(f'Login successful!', 'success')
                return redirect(url_for('dbModel.dashboard'))
            else:      #------------------------- COORDINATOR PAGE ---------------------
                return redirect(url_for('coordinator.coordinator_dashboard'))
        else:
            flash(f'Invalid username or password.', 'login_error')
            return redirect(url_for('dbModel.login'))
    return render_template('login.html')

@dbModel_route.route('/forgot_password', methods=["GET",'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get("username")
        birthday1 = request.form.get("birthday")
        birthday = convert_date(birthday1)

        user = User.query.filter_by(birthday=birthday, username=username).first()
        if user:
            # Redirect the user to a page where they can reset their password using the token
            return render_template('reset_password.html', username=username, birthday=birthday)
        else:
            return jsonify({'error': 'Incorrect credentials'}), 400  # Send a JSON response for AJAX handling
    return render_template('login.html')

@dbModel_route.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if ' ' in new_password:
            flash('Password cannot contain spaces.', 'newpassword_space')
            return render_template('reset_password.html', username=username, new_password=new_password, confirm_password=confirm_password)
        if user:
            if new_password == confirm_password:
                user.password = new_password

                # Commit the changes to the database
                db.session.commit()

                flash('Password reset successful. You can now log in with your new password.')
                return redirect(url_for('dbModel.login'))  # Replace 'login' with your actual login route
            else:
                flash('New password and confirmation not match.', 'not_match')
                return render_template('reset_password.html', username=username)
        else:
            flash('User not found.')
            return render_template('reset_password.html', username=username)

    return render_template('reset_password.html')



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
        pending_count = Pending_project.query.filter_by(pending="pending").count()
            
        # Set a maximum value for pending_count
        max_pending_count = 9
        pending_count_display = min(pending_count, max_pending_count)

        # If pending_count is 9 or greater, display it as '9+'
        pending_count_display = '9+' if pending_count > max_pending_count else pending_count

        if user:
            return user.firstname, user.role, pending_count_display
    return None, None, 0

@dbModel_route.before_request
def before_request():
    g.current_user, g.current_role, g.pending_count_display = get_current_user()

@dbModel_route.context_processor
def inject_current_user():
    return dict(current_user=g.current_user, current_role=g.current_role, pending_count = g.pending_count_display)


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
        birthday1 = request.form.get("birthday")
        password = request.form.get("password")
        role = request.form.get("role")
        program = request.form.get("program")

        birthday = convert_date(birthday1)
        # Check if the username already exists in the database
        existing_username = User.query.filter_by(username=username).first()
        existing_program = User.query.filter_by(program=program).first()

        if ' ' in password:
            flash('Password cannot contain spaces.', 'password_space')
            return redirect(url_for('dbModel.manage_account'))
        if ' ' in username:
            flash('Password cannot contain spaces.', 'username_space')
            return redirect(url_for('dbModel.manage_account'))

        if existing_program:
            flash(f"Sorry, '{program}' is already taken. Please choose another name or check existing programs.", 'existing_program')
        else:
            if existing_username:
                flash('Username already exists. Please choose a different username.', 'existing_username')
            else:
                new_user = User(username=username, firstname=firstname, lastname=lastname, birthday=birthday,
                password=password, role = role, program = program)
                try: 
                    db.session.add(new_user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                flash('User added successfully!', 'add_account')
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
        new_birthday1 = request.form['new_birthday']
        new_program = request.form['new_program']

        new_birthday = convert_date(new_birthday1)
        
        if ' ' in new_password:
            flash('Password cannot contain spaces.', 'password_space')
            return redirect(url_for('dbModel.manage_account'))
        if ' ' in new_username:
            flash('Password cannot contain spaces.', 'username_space')
            return redirect(url_for('dbModel.manage_account'))
        

        user = User.query.get(user_id)
        
        if user:
            user.username = new_username
            user.firstname = new_firstname
            user.lastname = new_lastname
            user.birthday = new_birthday
            user.password = new_password
            user.role = new_role
            user.program = new_program
            
            db.session.commit()
            flash('Account updated successfully!', 'edit_account')

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
            flash('Account deleted successfully!', 'delete_account')
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('dbModel.manage_account'))


##################  FOR COORDINATOR  #######################
@dbModel_route.route('/coordinator/<data>')
def coordinator(data):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("coordinator.html", data=data)

##################  FOR COMMUNITY CRUD  #######################
@dbModel_route.route("/get_community_data", methods=['GET'])
def get_community_data():
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

@dbModel_route.route("/community_data_list")
def community_data_list():
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
    all_data = Community.query.filter_by(status="Ongoing").all()
    program8 = Program.query.all()
    user1 = User.query.all()
    return render_template("community.html", community = all_data, form=form, program8=program8, user1 = user1)

#fetch for user
@dbModel_route.route("/subprogram1/<get_program>")
def get_program(get_program):
    sub = User.query.filter_by(program=get_program).all()
    subArray = [user.username for user in sub]  
    return jsonify({'user': subArray})

 

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
        cna_file = request.files['CNA']
      

        existing_community = Community.query.filter_by(user= user, community=community, program = program, subprogram=subprogram).first()

        if existing_community is None:
            new_community = Community(community=community, program=program, subprogram=subprogram, start_date=start_date,
            end_date=end_date, week=week, totalWeek=totalWeek, user=user, department=department, subDepartment=subDepartment, status=status)

            db.session.add(new_community)
            db.session.commit()
            flash('New community project added!', 'add_community')

            #FOR SUBPROGRAM
            #existing_subprogram = Subprogram.query.filter_by(program = program, subprogram=subprogram).first()

            new_subprogram = Subprogram(program=program, subprogram=subprogram)
            db.session.add(new_subprogram)
            db.session.commit()
            

            cpf_data = cpf_file.read()
            cpf_record = CPF(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cpf_file.filename,
                data=cpf_data
            )
            db.session.add(cpf_record)
            db.session.commit()

            cesap_data = cesap_file.read()
            cesap_record = CESAP(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cesap_file.filename,
                data=cesap_data
            )
            db.session.add(cesap_record)
            db.session.commit()

            cna_data = cna_file.read()
            cna_record = CNA(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cna_file.filename,
                data=cna_data
            )
            db.session.add(cna_record)
            db.session.commit()
        else:
            flash(f"Sorry, '{subprogram}' is already taken in {{community}}.", 'existing_community')

        

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
    community_name = request.args.get('community')

    # First, find and delete records from the database
    cpf_record = CPF.query.filter_by(community = community_name, program=program, subprogram=subprogram).first()
    cesap_record = CESAP.query.filter_by(community = community_name, program=program, subprogram=subprogram).first()
    subprogram_record = Subprogram.query.filter_by(program=program, subprogram=subprogram).first()
    cna_record = CNA.query.filter_by(community = community_name, program=program, subprogram=subprogram).first()

    if community:
        try:
            # Delete the user from the database
            db.session.delete(community)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')

    if subprogram_record:
        try:
            # Delete the user from the database
            db.session.delete(subprogram_record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')

    if cpf_record:
        # Delete the file associated with the CPF record
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cpf_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()

    if cesap_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cesap_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
    if cna_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cna_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()

    if subprogram_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(subprogram_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
    flash('Delete successfully!', 'delete_account')
    return redirect(url_for('dbModel.manage_community'))

############################### FOR PENDING ###################################

@dbModel_route.route("/manage_pending")
def manage_pending():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Pending_project.query.all()

    return render_template("pending.html", pending_project_data = all_data)

@dbModel_route.route('/delete_pending/<int:id>', methods=['GET'])
def delete_pending(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    community = Pending_project.query.get(id)

    if community:
        try:
            # Delete the user from the database
            db.session.delete(community)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')

     # First, find and delete records from the database
    cpf_record = CPFp.query.filter_by(community=community.community, program=community.program, subprogram=community.subprogram).first()
    cesap_record = CESAPp.query.filter_by(community=community.community, program=community.program, subprogram=community.subprogram).first()
    cna_record = CNAp.query.filter_by(community=community.community, program=community.program, subprogram=community.subprogram).first()
    if cpf_record:
        # Delete the file associated with the CPF record
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cpf_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()

    if cesap_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cesap_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
    if cna_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cna_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
    flash('Delete successfully!', 'delete_pending')
    return redirect(url_for('dbModel.manage_pending'))

@dbModel_route.route('/view_pending/<int:pending_id>', methods=['GET'])
def view_pending(pending_id):
    p = Pending_project.query.get(pending_id)
    cna_data = CNAp.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    cesap_data = CESAPp.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    cpf_data = CPFp.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()

    cpf_data_filename = cpf_data.filename
    cesap_data_filename = cesap_data.filename
    cna_data_filename = cna_data.filename

    return render_template("pending_details.html", community=p.community, program=p.program, subprogram = p.subprogram, totalWeek = p.totalWeek, user=p.user, start_date = p.start_date, end_date = p.end_date, department=p.department, subDepartment = p.subDepartment, cpf_data_filename=cpf_data_filename, cesap_data_filename=cesap_data_filename, cna_data_filename=cna_data_filename)

@dbModel_route.route('/view_cpf/<program>/<subprogram>/<community>', methods=['GET'])
def view_cpf(program, subprogram, community):
    upload_entry = CPFp.query.filter_by(community = community, program = program, subprogram = subprogram).first()
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404

@dbModel_route.route('/view_cna/<program>/<subprogram>/<community>', methods=['GET'])
def view_cna(program, subprogram, community):
    upload_entry = CNAp.query.filter_by(community = community, program = program, subprogram = subprogram).first()
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404

@dbModel_route.route('/view_cesap/<program>/<subprogram>/<community>', methods=['GET'])
def view_cesap(program, subprogram, community):
    upload_entry = CESAPp.query.filter_by(community = community, program = program, subprogram = subprogram).first()
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404


@dbModel_route.route("/approve", methods=["POST"])
def approve():
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
      

        existing_community = Community.query.filter_by(user= user, community=community, program = program, subprogram=subprogram).first()

        if existing_community is None:
            new_community = Community(community=community, program=program, subprogram=subprogram, start_date=start_date,
            end_date=end_date, week=week, totalWeek=totalWeek, user=user, department=department, subDepartment=subDepartment, status=status)

            db.session.add(new_community)
            db.session.commit()
            flash('New community project added!', 'add_community')

            
            pending_delete = Pending_project.query.filter_by(community=community, program = program, subprogram=subprogram).first()

            if pending_delete:
                try:
                    # Delete the user from the database
                    db.session.delete(pending_delete)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # You may want to log the exception for debugging purposes
            else:
                flash('User not found. Please try again.', 'error')

            # First, find and delete records from the database
            cpf_record = CPFp.query.filter_by(community=community, program=program, subprogram=subprogram).first()
            cesap_record = CESAPp.query.filter_by(community=community, program=program, subprogram=subprogram).first()
            cna_record = CNAp.query.filter_by(community=community, program=program, subprogram=subprogram).first()
            if cpf_record:
                # Delete the file associated with the CPF record
                try:
                    # Delete the 'Upload' record from the database
                    db.session.delete(cpf_record)
                    db.session.commit()
                    
                except Exception as e:
                    db.session.rollback()

            if cesap_record:
                try:
                    # Delete the 'Upload' record from the database
                    db.session.delete(cesap_record)
                    db.session.commit()
                    
                except Exception as e:
                    db.session.rollback()
            if cna_record:
                try:
                    # Delete the 'Upload' record from the database
                    db.session.delete(cna_record)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
        else:
            flash(f"Sorry, '{subprogram}' is already taken in {{community}}.", 'existing_community')

        #FOR SUBPROGRAM
        existing_subprogram = Subprogram.query.filter_by(program = program, subprogram=subprogram).first()
        if existing_subprogram is None:
            new_subprogram = Subprogram(program=program, subprogram=subprogram)
            db.session.add(new_subprogram)
            db.session.commit()
        
        existing_cpf_file = CPF.query.filter_by(community=community, program = program, subprogram=subprogram).first()
        if existing_cpf_file is None:
            cpf_data = cpf_file.read()
            cpf_record = CPF(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cpf_file.filename,
                data=cpf_data
            )
            db.session.add(cpf_record)
            db.session.commit()

        existing_cesap_file = CESAP.query.filter_by(community=community, program = program, subprogram=subprogram).first()
        if existing_cesap_file is None:
            cesap_data = cesap_file.read()
            cesap_record = CESAP(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cesap_file.filename,
                data=cesap_data
            )
            db.session.add(cesap_record)
            db.session.commit()

        existing_cna_file = CNA.query.filter_by(community=community, program = program, subprogram=subprogram).first()
        if existing_cna_file is None:
            cna_data = cna_file.read()
            cna_record = CNA(
                community=community,
                program=program,
                subprogram=subprogram,
                filename=cna_file.filename,
                data=cna_data
            )
            db.session.add(cna_record)
            db.session.commit()
        


        return redirect(url_for('dbModel.manage_pending'))
       
    return redirect(url_for('dbModel.manage_pending'))


############# UPDATE WEEK BASED FROM Subprogram ##############

@dbModel_route.route('/update_week', methods=['POST'])
def update_week():
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
@dbModel_route.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    community = data['community']
    subprogram = data['subprogram']
    program = data['program']
    status = data['status']

    # Query the database to get records with the specified subprogram
    communities = Community.query.filter_by(community = community, program=program, subprogram=subprogram).all()

    for community in communities:
        community.status = status
    db.session.commit()
    return jsonify({'message': 'Week column updated for the specified subprogram.'})


#display kaakbay program and coordinator
def get_ongoing_count(session, program_name):
    result = db.session.query(
        Community.program,
        func.sum(case((Community.status == 'Ongoing', 1), else_=0)).label('ongoing_count')
    ).filter(Community.program == program_name).group_by(Community.program).all()
    
    if result:
        return result[0][1]
    else:
        return 0
def get_completed_count(session, program_name):
    result = db.session.query(
        Community.program,
        func.sum(case((Community.status == 'Completed', 1), else_=0)).label('completed_count')
    ).filter(Community.program == program_name).group_by(Community.program).all()
    
    if result:
        return result[0][1]
    else:
        return 0
@dbModel_route.route("/kaakbay_program")
def kaakbay_program():
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
        ongoing_count = get_ongoing_count(session, program_name)
        program_ongoing_counts[program_name] = ongoing_count
        
    for program_name in program_names:
        completed_count = get_completed_count(session, program_name)
        program_completed_counts[program_name] = completed_count
    
    return render_template("kaakbay_program.html", literacy_firstname=literacy_firstname, literacy_lastname=literacy_lastname,
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
@dbModel_route.route("/change_password")
def change_password():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("change_password.html")

@dbModel_route.route("/new_password", methods=["GET", "POST"])
def new_password():
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
            return redirect(url_for('dbModel.change_password'))
        if user:
            if new_password == confirm_password:
                user.password = new_password
                db.session.commit()
                flash('Password successfully changed.', 'new_password')
                return redirect(url_for('dbModel.change_password'))
            else:
                flash('New password and confirmation do not match.', 'not_match')
        else:
            flash('Wrong old password.', 'wrong_old')
    return redirect(url_for('dbModel.change_password'))

############# project files ##############
@dbModel_route.route("/project_files")
def project_files():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("project_files.html")

@dbModel_route.route("/project_file_list/<data>")
def project_file_list(data):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    project_file_list = Community.query.filter_by(program=data).all()
    return render_template("project_table.html", project_file_list=project_file_list, data=data)

@dbModel_route.route("/view_project/<int:project_id>")
def view_project(project_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    p = Community.query.get(project_id)
    cna_data = CNA.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    cesap_data = CESAP.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    cpf_data = CPF.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()

    cpf_data_filename = cpf_data.filename
    cesap_data_filename = cesap_data.filename
    cna_data_filename = cna_data.filename

    return render_template("project_details.html", community=p.community, program=p.program, subprogram = p.subprogram, totalWeek = p.totalWeek, user=p.user, start_date = p.start_date, end_date = p.end_date, department=p.department, subDepartment = p.subDepartment, cpf_data_filename=cpf_data_filename, cesap_data_filename=cesap_data_filename, cna_data_filename=cna_data_filename)


@dbModel_route.route("/delete_project/<int:project_id>")
def delete_project(project_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    p = Community.query.filter_by(id=project_id).first()
    if p:
        try:
            # Delete the user from the database
            db.session.delete(p)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
     # First, find and delete records from the database
    cna_record = CNA.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    cesap_record = CESAP.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    cpf_record = CPF.query.filter_by(community = p.community, program = p.program, subprogram = p.subprogram).first()
    
    if cpf_record:
        # Delete the file associated with the CPF record
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cpf_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()

    if cesap_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cesap_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
    if cna_record:
        try:
            # Delete the 'Upload' record from the database
            db.session.delete(cna_record)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
    flash('Delete successfully!', 'delete_project')
    return redirect(url_for('dbModel.project_files'))

@dbModel_route.route('/view_cpf_project/<program>/<subprogram>/<community>', methods=['GET'])
def view_cpf_project(program, subprogram, community):
    upload_entry = CPF.query.filter_by(community = community, program = program, subprogram = subprogram).first()
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404

@dbModel_route.route('/view_cna_project/<program>/<subprogram>/<community>', methods=['GET'])
def view_cna_project(program, subprogram, community):
    upload_entry = CNA.query.filter_by(community = community, program = program, subprogram = subprogram).first()
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404

@dbModel_route.route('/view_cesap_project/<program>/<subprogram>/<community>', methods=['GET'])
def view_cesap_project(program, subprogram, community):
    upload_entry = CESAP.query.filter_by(community = community, program = program, subprogram = subprogram).first()
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404


# prototype to move data from table1 to table 2 (archive)
@dbModel_route.route('/move_data')
def move_data():
    # Fetch data from CPF
    data_to_move = CPFARCHIVE.query.all()

    # Iterate through the data and move it to CPFARCHIVE
    for row in data_to_move:
        # Create a new row in CPFARCHIVE
        new_row = CPF(
            community=row.community,
            program=row.program,
            subprogram=row.subprogram,
            filename=row.filename,
            data=row.data
        )
        db.session.add(new_row)

    # Commit the changes to CPFARCHIVE
    db.session.commit()

    # Delete the corresponding rows from CPF
    CPFARCHIVE.query.delete()

    # Commit the changes to CPF
    db.session.commit()

    return 'Data moved successfully'