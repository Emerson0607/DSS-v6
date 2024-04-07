from flask import g, Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g, redirect
from main.models.dbModel import Program, Pending_project, Users, Logs, Fundraising, Archive_fund, Pending_fund, Donor_cash
from main import db
from flask import Response
import secrets
from datetime import datetime, timedelta
from sqlalchemy import func, case
from mailbox import Message
from main import Form, app, mail
from flask_mail import Mail, Message
import pytz, re
import base64
# LINE BELOW IS FOR PASS ENCRYPTION (UNCOMMENT IF NEEDED)
from werkzeug.security import generate_password_hash, check_password_hash 

fundraising_route = Blueprint('fundraising', __name__)
token_store = {}

#################### Date Converter ##################
def convert_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def convert_date1(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = Users.query.get(session['user_id'])
        
        
        #pending project count
        declined_count = Pending_project.query.filter_by(status="Declined", program=user.program).count()
        max_declined_count = 9
        declined_count_display = min(declined_count, max_declined_count)
        declined_count_display = '9+' if declined_count > max_declined_count else declined_count

        #pending fund project count for ADMIN
        declined_fund_count = Pending_fund.query.filter_by(status="For Review").count()
        max_declined_fund_count = 9
        declined_fund_count_display = min(declined_fund_count, max_declined_fund_count)
        declined_fund_count_display = '9+' if declined_fund_count > max_declined_fund_count else declined_fund_count
        
        #pending fund project count for COORDINATOR
        cDeclined_fund_count = Pending_fund.query.filter_by(status="Declined", coordinator_id=user.id).count()
        cMax_declined_fund_count = 9
        cDeclined_fund_count_display = min(cDeclined_fund_count, cMax_declined_fund_count)
        cDeclined_fund_count_display = '9+' if cDeclined_fund_count > cMax_declined_fund_count else cDeclined_fund_count

        profile_picture_base64 = None
        if user:
            if user.profile_picture:
                # Convert the profile picture to base64 encoding
                profile_picture_base64 = base64.b64encode(user.profile_picture).decode('utf-8')
            return user.username, user.role, user.program, declined_count_display, user.firstname, user.lastname, user.department_A, profile_picture_base64, cDeclined_fund_count_display, user.id, declined_fund_count_display
    return None, None, None, 0, None, None, None, None, None, None, None
    
@fundraising_route.before_request
def before_request():
    g.current_user, g.current_role, g.current_program, g.declined_count_display, g.current_firstname, g.current_lastname, g.current_department_A, g.profile_picture_base64, g.cDeclined_fund_count_display, g.current_id, g.declined_fund_count_display = get_current_user()

@fundraising_route.context_processor
def inject_current_user():
    current_program_coordinator = g.current_program
    return dict(current_user=g.current_user, current_role=g.current_role, current_program=g.current_program, declined_count = g.declined_count_display, current_firstname=g.current_firstname, current_lastname=g.current_lastname, current_department_A=g.current_department_A, profile_picture_base64 = g.profile_picture_base64, cDeclined_fund_count=g.cDeclined_fund_count_display, current_id=g.current_id, declined_fund_count=g.declined_fund_count_display)

########################Fundraising Activity#############################
@fundraising_route.route("/fund")
def fund():
    form = Form()
    placeholder_choice = ("", "-- Select Program --")
    form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
    form.program.default = ""
    form.process()
    form=form

    # Check if the user is an admin
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    coordinators = Users.query.filter_by(role='Coordinator').all()
    # Dynamically generate the years
    current_year = datetime.now().year
    fund_list = Fundraising.query.all()
    pending_fund_list = Pending_fund.query.filter_by(status="For Review").all()

    # Render the template with the current year and the next four years
    return render_template("fund.html", form=form, current_year=current_year, fund_list=fund_list, coordinators=coordinators, pending_fund_list=pending_fund_list)

@fundraising_route.route("/add_fund", methods=["POST"])
def add_fund():
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        project_name = request.form.get("project_name")
        program = request.form.get("program")
        venue = request.form.get("venue")
        proposed_date1 = request.form.get("proposed_date")
        target_date1 = request.form.get("target_date")
        coordinator = request.form.get("coordinator")
        event_organizer = request.form.get("event_organizer")
        lead_proponent = request.form.get("lead_proponent")
        contact_details = request.form.get("contact_details")
        status = "Ongoing"
        donation_type = request.form.get("donation_type")

        #Convert date
        proposed_date = convert_date(proposed_date1)
        target_date = convert_date(target_date1)
        
        if coordinator:
            firstname = coordinator.split()[0]
            
        coordinator_name= Users.query.filter_by(firstname=firstname).first()
      
        existing_fund= Fundraising.query.filter_by(project_name=project_name, program=program, venue=venue).first()

        if existing_fund is None:
            new_fund = Fundraising(project_name=project_name, program=program, venue=venue, proposed_date=proposed_date, target_date=target_date, coordinator=coordinator, event_organizer=event_organizer, lead_proponent=lead_proponent, contact_details=contact_details, status=status, donation_type=donation_type, coordinator_id=coordinator_name.id)

            userlog = g.current_user
            action = f'ADDED new fundraising {program} project.'
            ph_tz = pytz.timezone('Asia/Manila')
            ph_time = datetime.now(ph_tz)
            timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = convert_date1(timestamp1)
            insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
            if insert_logs:
                db.session.add(insert_logs)
                db.session.commit()

            db.session.add(new_fund)
            db.session.commit()
            flash('New fundraising project added!', 'add_community')
        else:
            flash(f"Sorry, '{project_name}' already exist.", 'existing_community')
        return redirect(url_for('fundraising.fund'))
    return redirect(url_for('fundraising.fund'))

@fundraising_route.route("/view_fund/<int:fund_id>")
def view_fund(fund_id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    p = Fundraising.query.get(fund_id)

    return render_template("fund_details.html",id=p.id, project_name=p.project_name, program=p.program, venue=p.venue, proposed_date=p.proposed_date, target_date=p.target_date, coordinator=p.coordinator, event_organizer=p.event_organizer, lead_proponent=p.lead_proponent, contact_details=p.contact_details, donation_type=p.donation_type )

@fundraising_route.route('/delete_fund/<int:id>', methods=['GET'])
def delete_fund(id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    fund_to_delete = Fundraising.query.get(id)
    program = request.args.get('program')
    project_name = request.args.get('project_name')

    if fund_to_delete:
        
        p = Fundraising.query.filter_by(id=id, program = program, project_name=project_name).first()

        new_row = Archive_fund(
                project_name = p.project_name,
                program = p.program,
                venue = p.venue,
                proposed_date = p.proposed_date,
                target_date = p.target_date,
                coordinator = p.coordinator,
                event_organizer = p.event_organizer,
                lead_proponent = p.lead_proponent,
                contact_details = p.contact_details,
                status = p.status,
                donation_type = p.donation_type,
                url = "None",
                coordinator_id = p.coordinator_id
        )
        db.session.add(new_row)
        db.session.commit()



        userlog = g.current_user
        action = f'DELETED {project_name} project'
        ph_tz = pytz.timezone('Asia/Manila')
        ph_time = datetime.now(ph_tz)
        timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = convert_date1(timestamp1)
        insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
        if insert_logs:
            db.session.add(insert_logs)
            db.session.commit()  

        try:
            # Delete the user from the database
            db.session.delete(fund_to_delete)
            db.session.commit()
            flash('Delete successfully!', 'delete_account')
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('fundraising.fund'))

@fundraising_route.route('/delete_pending_fund/<int:id>', methods=['GET'])
def delete_pending_fund(id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    fund_to_delete = Pending_fund.query.get(id)
    program = request.args.get('program')
    project_name = request.args.get('project_name')

    if fund_to_delete:
        userlog = g.current_user
        action = f'DELETED pending {project_name} project'
        ph_tz = pytz.timezone('Asia/Manila')
        ph_time = datetime.now(ph_tz)
        timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = convert_date1(timestamp1)
        insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
        if insert_logs:
            db.session.add(insert_logs)
            db.session.commit()  

        try:
            # Delete the user from the database
            db.session.delete(fund_to_delete)
            db.session.commit()
            flash('Delete successfully!', 'delete_account')
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('fundraising.fund'))

@fundraising_route.route("/view_pending_fund/<int:fund_id>")
def view_pending_fund(fund_id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    p = Pending_fund.query.get(fund_id)

    return render_template("pending_fund_details.html",id=p.id, project_name=p.project_name, program=p.program, venue=p.venue, proposed_date=p.proposed_date, target_date=p.target_date, coordinator=p.coordinator, event_organizer=p.event_organizer, lead_proponent=p.lead_proponent, contact_details=p.contact_details, donation_type=p.donation_type, comments=p.comments  )

@fundraising_route.route("/approve_fund", methods=["POST"])
def approve_fund():
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        fund_id = request.form.get("id")
        project_name = request.form.get("project_name")
        program = request.form.get("program")
 
        existing_fund = Fundraising.query.filter_by(project_name= project_name, program=program).first()
        
        
        
        
        if existing_fund is None:
            p = Pending_fund.query.filter_by(id=fund_id).first()
            # Iterate through the data and move it to CPFARCHIVE
        
                # Create a new row in CPFARCHIVE
            new_row = Fundraising(
                project_name = p.project_name,
                program = p.program,
                venue = p.venue,
                proposed_date = p.proposed_date,
                target_date = p.target_date,
                coordinator = p.coordinator,
                event_organizer = p.event_organizer,
                lead_proponent = p.lead_proponent,
                contact_details = p.contact_details,
                status = "Ongoing",
                donation_type = p.donation_type,
                coordinator_id = p.coordinator_id
        )

            userlog = g.current_user
            action = f'APPROVE pending {project_name} project of {program}'
            ph_tz = pytz.timezone('Asia/Manila')
            ph_time = datetime.now(ph_tz)
            timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = convert_date1(timestamp1)
            insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
            if insert_logs:
                db.session.add(insert_logs)
                db.session.commit()
                db.session.add(new_row)
                db.session.commit()
                flash('Approved fundraising project!', 'add_community')

            pending_delete = Pending_fund.query.filter_by(id=fund_id).first()
            if pending_delete:
                try:
                    # Delete the user from the database
                    db.session.delete(pending_delete)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # You may want to log the exception for debugging purposes
            else:
                flash('Project not found. Please try again.', 'error')
        else:
            flash(f"Sorry, '{project_name}' is already taken.", 'existing_community')
  
        return redirect(url_for('fundraising.fund'))
       
    return redirect(url_for('fundraising.fund'))
    
@fundraising_route.route("/decline_fund", methods=["POST"])
def decline_fund():
    if g.current_role not in ["Admin", "BOR"]:
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    # Extract data from the form
    project_name = request.form.get('project_name')
    program = request.form.get('program')
    fund_id = request.form.get('id')
    comments = request.form.get('comments')

    # Check if the request method is POST
    if request.method == "POST":
        # Query the pending fund by ID
        p = Pending_fund.query.filter_by(id=fund_id).first()

        # Update the status and comments if the fund exists
        if p:
            p.status = "Declined"
            p.comments = comments

            # Commit changes to the database
            db.session.commit()

            # Log the action
            userlog = g.current_user
            action = f'DECLINED {project_name} project of {program}'
            ph_tz = pytz.timezone('Asia/Manila')
            ph_time = datetime.now(ph_tz)
            timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = convert_date1(timestamp1)
            insert_logs = Logs(userlog=userlog, timestamp=timestamp, action=action)
            if insert_logs:
                db.session.add(insert_logs)
                db.session.commit()

            # Redirect to the fundraising page after processing the form
            return redirect(url_for('fundraising.fund'))

    # If the request method is not POST or the form submission fails, redirect back to the fundraising page
    return redirect(url_for('fundraising.fund'))

######################## Coordinator Fundraising Activity#############################
@fundraising_route.route("/cFund")
def cFund():
    form = Form()
    placeholder_choice = ("", "-- Select Program --")
    form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
    form.program.default = ""
    form.process()
    form=form

    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    current_year = datetime.now().year
    fund_list = Fundraising.query.filter(Fundraising.coordinator_id==g.current_id).all()
    pending_fund_list = Pending_fund.query.filter(Pending_fund.coordinator_id==g.current_id).all()

    # Render the template with the current year and the next four years
    return render_template("cFund.html", form=form, current_year=current_year, fund_list=fund_list, pending_fund_list=pending_fund_list)

@fundraising_route.route("/cAdd_fund", methods=["POST"])
def cAdd_fund():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        project_name = request.form.get("project_name")
        program = request.form.get("program")
        venue = request.form.get("venue")
        proposed_date1 = request.form.get("proposed_date")
        target_date1 = request.form.get("target_date")
        coordinator = request.form.get("coordinator")
        event_organizer = request.form.get("event_organizer")
        lead_proponent = request.form.get("lead_proponent")
        contact_details = request.form.get("contact_details")
        status = "For Review"
        donation_type = request.form.get("donation_type")
       

        #Convert date
        proposed_date = convert_date(proposed_date1)
        target_date = convert_date(target_date1)
      
        if coordinator:
            firstname = coordinator.split()[0]
            
        coordinator_name= Users.query.filter_by(firstname=firstname).first()
        existing_fund= Pending_fund.query.filter_by(project_name=project_name, program=program, venue=venue).first()

        if existing_fund is None:
            new_fund = Pending_fund(project_name=project_name, program=program, venue=venue, proposed_date=proposed_date, target_date=target_date, coordinator=coordinator, event_organizer=event_organizer, lead_proponent=lead_proponent, contact_details=contact_details, status=status, donation_type=donation_type, coordinator_id=coordinator_name.id)

            userlog = g.current_user
            action = f'ADDED {program} project {project_name} for review.'
            ph_tz = pytz.timezone('Asia/Manila')
            ph_time = datetime.now(ph_tz)
            timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = convert_date1(timestamp1)
            insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
            if insert_logs:
                db.session.add(insert_logs)
                db.session.commit()

            db.session.add(new_fund)
            db.session.commit()
            flash('New fundraising project added for review!', 'add_community')
        else:
            flash(f"Sorry, '{project_name}' already exist.", 'existing_community')
        return redirect(url_for('fundraising.cFund'))
    return redirect(url_for('fundraising.cFund'))

@fundraising_route.route("/cView_fund/<int:fund_id>")
def cView_fund(fund_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    p = Fundraising.query.get(fund_id)

    return render_template("cFund_details.html",id=p.id, project_name=p.project_name, program=p.program, venue=p.venue, proposed_date=p.proposed_date, target_date=p.target_date, coordinator=p.coordinator, event_organizer=p.event_organizer, lead_proponent=p.lead_proponent, contact_details=p.contact_details, donation_type=p.donation_type )

@fundraising_route.route("/cView_pending_fund/<int:fund_id>")
def cView_pending_fund(fund_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    
    
    p = Pending_fund.query.get(fund_id)

    form = Form()
    placeholder_choice = (p.program, p.program)
    form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
    form.program.default = ""
    form.process()
    form=form
    
    return render_template("cPending_fund_details.html", form=form, id=p.id, project_name=p.project_name, program=p.program, venue=p.venue, proposed_date=p.proposed_date, target_date=p.target_date, coordinator=p.coordinator, event_organizer=p.event_organizer, lead_proponent=p.lead_proponent, contact_details=p.contact_details, donation_type=p.donation_type, comments=p.comments )

@fundraising_route.route('/cDelete_fund/<int:id>', methods=['GET'])
def cDelete_fund(id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    fund_to_delete = Fundraising.query.get(id)
    program = request.args.get('program')
    project_name = request.args.get('project_name')

    if fund_to_delete:
        
        p = Fundraising.query.filter_by(id=id, program = program, project_name=project_name).first()

        new_row = Archive_fund(
                project_name = p.project_name,
                program = p.program,
                venue = p.venue,
                proposed_date = p.proposed_date,
                target_date = p.target_date,
                coordinator = p.coordinator,
                event_organizer = p.event_organizer,
                lead_proponent = p.lead_proponent,
                contact_details = p.contact_details,
                status = p.status,
                donation_type = p.donation_type,
                url = "None"
        )
        db.session.add(new_row)
        db.session.commit()



        userlog = g.current_user
        action = f'DELETED {project_name} project'
        ph_tz = pytz.timezone('Asia/Manila')
        ph_time = datetime.now(ph_tz)
        timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = convert_date1(timestamp1)
        insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
        if insert_logs:
            db.session.add(insert_logs)
            db.session.commit()  

        try:
            # Delete the user from the database
            db.session.delete(fund_to_delete)
            db.session.commit()
            flash('Delete successfully!', 'delete_account')
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('fundraising.cFund'))

@fundraising_route.route('/cDelete_pending_fund/<int:id>', methods=['GET'])
def cDelete_pending_fund(id):

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    fund_to_delete = Pending_fund.query.get(id)
    program = request.args.get('program')
    project_name = request.args.get('project_name')

    if fund_to_delete:
        userlog = g.current_user
        action = f'DELETED pending {project_name} project'
        ph_tz = pytz.timezone('Asia/Manila')
        ph_time = datetime.now(ph_tz)
        timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = convert_date1(timestamp1)
        insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
        if insert_logs:
            db.session.add(insert_logs)
            db.session.commit()  

        try:
            # Delete the user from the database
            db.session.delete(fund_to_delete)
            db.session.commit()
            flash('Delete successfully!', 'delete_account')
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('fundraising.cFund'))

######################## Archived fundraising #############################
@fundraising_route.route("/archived_fund")
def archived_fund():
    # Check if the user is an admin
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    current_year = datetime.now().year
    archived_fund_list = Archive_fund.query.all()

    # Render the template with the current year and the next four years
    return render_template("archived_fund.html",current_year=current_year, archived_fund_list=archived_fund_list)

@fundraising_route.route("/view_archived_fund/<int:fund_id>")
def view_archived_fund(fund_id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    p = Archive_fund.query.get(fund_id)

    return render_template("fund_archived_details.html",id=p.id, project_name=p.project_name, program=p.program, venue=p.venue, proposed_date=p.proposed_date, target_date=p.target_date, coordinator=p.coordinator, event_organizer=p.event_organizer, lead_proponent=p.lead_proponent, contact_details=p.contact_details, donation_type=p.donation_type, url=p.url )

@fundraising_route.route('/delete_archived_fund/<int:id>', methods=['GET'])
def delete_archived_fund(id):
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    fund_to_delete = Archive_fund.query.get(id)
    program = request.args.get('program')
    project_name = request.args.get('project_name')

    if fund_to_delete:
        userlog = g.current_user
        action = f'DELETED {project_name} project'
        ph_tz = pytz.timezone('Asia/Manila')
        ph_time = datetime.now(ph_tz)
        timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = convert_date1(timestamp1)
        insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
        if insert_logs:
            db.session.add(insert_logs)
            db.session.commit()  

        try:
            # Delete the user from the database
            db.session.delete(fund_to_delete)
            db.session.commit()
            flash('Delete successfully!', 'delete_account')
        except Exception as e:
            db.session.rollback()
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('fundraising.archived_fund'))

@fundraising_route.route('/update_pending_fund', methods=['POST'])
def update_pending_fund():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        pending_id = request.form.get('id')
        project_name = request.form.get("project_name")
        program = request.form.get("program")
        venue = request.form.get("venue")
        proposed_date1 = request.form.get("proposed_date")
        target_date1 = request.form.get("target_date")
        coordinator = request.form.get("coordinator")
        event_organizer = request.form.get("event_organizer")
        lead_proponent = request.form.get("lead_proponent")
        contact_details = request.form.get("contact_details")
        donation_type = request.form.get("donation_type")
       
        #Convert date
        proposed_date = convert_date(proposed_date1)
        target_date = convert_date(target_date1)

        form = Form()
        placeholder_choice = (program, program)
        form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
        form.program.default = ""
        form.process()
        form=form
    
        pending = Pending_fund.query.get(pending_id)

        if pending:

            pending.project_name = project_name
            pending.program = program
            pending.venue = venue
            pending.proposed_date = proposed_date
            pending.target_date = target_date
            pending.coordinator = coordinator
            pending.event_organizer = event_organizer
            pending.lead_proponent = lead_proponent
            pending.contact_details = contact_details
            pending.status = "For Review"
            pending.donation_type = donation_type

            userlog = g.current_user
            action = f'UPDATED pending {project_name} projects of {program}'
            ph_tz = pytz.timezone('Asia/Manila')
            ph_time = datetime.now(ph_tz)
            timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
            timestamp = convert_date1(timestamp1)
            insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
            if insert_logs:
                db.session.add(insert_logs)
                db.session.commit()
                
            db.session.commit()
            flash('Pending updated successfully!', 'edit_account')

    p = Pending_fund.query.get(pending_id)

    return render_template("cPending_fund_details.html",form=form, id=p.id, project_name=p.project_name, program=p.program, venue=p.venue, proposed_date=p.proposed_date, target_date=p.target_date, coordinator=p.coordinator, event_organizer=p.event_organizer, lead_proponent=p.lead_proponent, contact_details=p.contact_details, donation_type=p.donation_type, comments=p.comments )

######################## fundraising programs #############################
@fundraising_route.route('/fund_programs')
def fund_programs():
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))
    
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("fund_programs.html")

@fundraising_route.route("/get_fund_data", methods=['GET'])
def get_fund_data():
    try:
        fund_data = []
        # Fetch fundraising projects
        fundraising_records = Fundraising.query.all()
        for record in fundraising_records:
            # Fetch donor data associated with each fundraising project
            donors = Donor_cash.query.filter_by(fund_id=record.id).all()
            donor_list = [{'name': donor.name, 'donation': donor.donation, 'date': donor.date} for donor in donors]
            # Include fund_id in the donor data
            donor_list_with_fund_id = [{'fund_id': donor.fund_id, 'name': donor.name, 'donation': donor.donation, 'date': donor.date} for donor in donors]
            fund_data.append({
                'id': record.id,
                'program': record.program,
                'coordinator': record.coordinator,
                'project_name': record.project_name,
                'proposed_date': record.proposed_date,
                'target_date': record.target_date,
                'venue': record.venue,
                'event_organizer': record.event_organizer,
                'lead_proponent': record.lead_proponent,
                'contact_details': record.contact_details,
                'donation_type': record.donation_type,
                'status': record.status,
                'coordinator_id': record.coordinator_id,
                'donors': donor_list_with_fund_id  # Use the donor_list_with_fund_id instead of donor_list
            })

        if fund_data:
            return jsonify(fund_data)
        else:
            # Handle the case when no data is found
            return jsonify({'message': 'There are no active projects available for display.'}), 200

    except Exception as e:
        # Log the error for debugging
        print(str(e))
        return make_response("Internal Server Error", 500)

@fundraising_route.route('/update_fund', methods=['POST'])
def update_fund():
    data = request.get_json()
    fund_id = data['id']
    status = data['status']
    donation_type = data['donation_type']
    donors = data['donors']

    # Query the database to get the fundraising record
    fund_update = Fundraising.query.get(fund_id)

    if fund_update:
        # Update the status for the specific record
        fund_update.status = status

        # Add donor data
        for donor in donors:
            date1 = convert_date(donor['date'])  # Assuming convert_date function is defined elsewhere
            new_donor = Donor_cash(fund_id=fund_id, program=fund_update.program, name=donor['name'], donation=donor['donation'], date=date1)
            db.session.add(new_donor)

        db.session.commit()
        return jsonify({'message': 'Status updated successfully.'})
    else:
        return jsonify({'message': 'Record not found.'}), 404

@fundraising_route.route('/archive_fund_donor', methods=['POST'])
def archive_fund_donor():
    if g.current_role != "Admin" and g.current_role != "BOR":
        return redirect(url_for('dbModel.login'))

    data = request.get_json()
    fund_id = data['id']
    project_name = data['project_name']
    program = data['program']
    coordinator = data['coordinator']
    status = data['status']
    url = data.get('url', '')

    # Validate URL
    if url and not re.match(r'^https?://(?:www\.)?\w+\.\w+', url):
        flash('Invalid URL format. Please enter a valid URL.', 'delete_account')
        return jsonify({'error': 'Invalid URL format'})
      
    data_to_move = Fundraising.query.filter_by(id=fund_id).first()
    # Iterate through the data and move it to CPFARCHIVE
        
        # Create a new row in CPFARCHIVE
    new_row = Archive_fund(
        program = data_to_move.program,
        coordinator = data_to_move.coordinator,
        project_name = data_to_move.project_name,
        proposed_date = data_to_move.proposed_date,
        target_date = data_to_move.target_date,
        venue = data_to_move.venue,
        event_organizer = data_to_move.event_organizer,
        lead_proponent = data_to_move.lead_proponent,
        contact_details = data_to_move.contact_details,
        donation_type = data_to_move.donation_type,
        status = data_to_move.status,
        url = url,
        coordinator_id = data_to_move.coordinator_id
    )
    userlog = g.current_user
    action = f'ARCHIVED {project_name} project of {program}'
    ph_tz = pytz.timezone('Asia/Manila')
    ph_time = datetime.now(ph_tz)
    timestamp1 = ph_time.strftime('%Y-%m-%d %H:%M:%S')
    timestamp = convert_date1(timestamp1)
    insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
    if insert_logs:
        db.session.add(insert_logs)
        db.session.commit()

    db.session.add(new_row)
    db.session.commit()

    fund_delete = Fundraising.query.filter_by(id=fund_id).first()
    if fund_delete:
        try:
                # Delete the user from the database
            db.session.delete(fund_delete)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
                # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return jsonify({'message': 'Data archived.'})


    