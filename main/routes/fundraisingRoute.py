from flask import g, Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g, redirect
from main.models.dbModel import Community, Program, Subprogram, Role, Upload, Pending_project, Users, Archive, Logs, Plan, Department, Resources
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

# Get the timezone for the Philippines


fundraising_route = Blueprint('fundraising', __name__)
token_store = {}


#################### CURRENT USER ##################
def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = Users.query.get(session['user_id'])
        pending_count = Pending_project.query.filter_by(status="For Review").count()
            
        # Set a maximum value for pending_count
        max_pending_count = 9
        pending_count_display = min(pending_count, max_pending_count)

        # If pending_count is 9 or greater, display it as '9+'
        pending_count_display = '9+' if pending_count > max_pending_count else pending_count

        profile_picture_base64 = None
        if user:
            if user.profile_picture:
                # Convert the profile picture to base64 encoding
                profile_picture_base64 = base64.b64encode(user.profile_picture).decode('utf-8')

            return user.username, user.role, pending_count_display, user.firstname, user.lastname, profile_picture_base64
    return None, None, 0, None, None, None

@fundraising_route.before_request
def before_request():
    g.current_user, g.current_role, g.pending_count_display, g.current_firstname, g.current_lastname, g.profile_picture_base64 = get_current_user()

@fundraising_route.context_processor
def inject_current_user():
    current_user, current_role, pending_count, current_firstname, current_lastname, profile_picture_base64 = get_current_user()
    return dict(current_user=current_user, current_role=current_role, pending_count=pending_count, current_firstname=current_firstname, current_lastname=current_lastname, profile_picture_base64=profile_picture_base64)


########################Fundraising Activity#############################
@fundraising_route.route("/fundraising_activity")
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

    # Render the template with the current year and the next four years
    return render_template("fund.html",form=form, current_year=current_year, coordinators=coordinators)