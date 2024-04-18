from flask import g, Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g, redirect
from main.models.dbModel import Community, Program, Subprogram, Role, Upload, Pending_project, Users, Archive, Logs, Plan, Department, Resources, Pending_fund, Fundraising, Budget, Total_budget, Current_Budget, Current_total_budget, Budget_cost, Budget_program_cost, Program_cost
from main import db
from flask import Response
import secrets
from datetime import datetime, timedelta
from sqlalchemy import func, case, extract
from mailbox import Message
from main import Form, app, mail
from flask_mail import Mail, Message
import pytz, re
import base64
from flask_wtf import FlaskForm
from wtforms import SelectField
# LINE BELOW IS FOR PASS ENCRYPTION (UNCOMMENT IF NEEDED)
from werkzeug.security import generate_password_hash, check_password_hash 

bor_route = Blueprint('bor', __name__)
token_store = {}

# Function to validate email format
def is_valid_email(email):
    # Regular expression pattern for validating email format
    pattern = r'^[\w\.-]+@gmail\.com$'
    return re.match(pattern, email) is not None


def convert_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def convert_date1(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


#################### CURRENT USER ##################
def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = Users.query.get(session['user_id'])
        
        pending_count = Pending_project.query.filter_by(status="For Review").count()
        max_pending_count = 9
        pending_count_display = min(pending_count, max_pending_count)
        pending_count_display = '9+' if pending_count > max_pending_count else pending_count

        #pending fund project count for ADMIN
        declined_fund_count = Pending_fund.query.filter_by(status="For Review").count()
        max_declined_fund_count = 9
        declined_fund_count_display = min(declined_fund_count, max_declined_fund_count)
        declined_fund_count_display = '9+' if declined_fund_count > max_declined_fund_count else declined_fund_count
        
        profile_picture_base64 = None
        if user:
            if user.profile_picture:
                # Convert the profile picture to base64 encoding
                profile_picture_base64 = base64.b64encode(user.profile_picture).decode('utf-8')

            return user.username, user.role, pending_count_display, user.firstname, user.lastname, profile_picture_base64, declined_fund_count_display
    return None, None, 0, None, None, None, None

@bor_route.before_request
def before_request():
    g.current_user, g.current_role, g.pending_count_display, g.current_firstname, g.current_lastname, g.profile_picture_base64, g.declined_fund_count_display = get_current_user()

@bor_route.context_processor
def inject_current_user():
    current_user, current_role, pending_count, current_firstname, current_lastname, profile_picture_base64, declined_fund_count = get_current_user()
    return dict(current_user=current_user, current_role=current_role, pending_count=pending_count, current_firstname=current_firstname, current_lastname=current_lastname, profile_picture_base64=profile_picture_base64, declined_fund_count=declined_fund_count)

@bor_route.route("/bor_dashboard")
def bor_dashboard():
     # Check if the user is logged in
    if g.current_user != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Community.query.filter_by(status="Ongoing").all()
    program8 = Program.query.all()
    department = Department.query.all()
    user1 = Users.query.all()
    coordinators = Users.query.filter_by(role='Coordinator').all()
    return render_template("bCommunity.html", community = all_data, program8=program8, user1 = user1, department=department, coordinators=coordinators)

@bor_route.route("/bManage_community")
def bManage_community():
    if g.current_user != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Community.query.filter_by(status="Ongoing").all()
    program8 = Program.query.all()
    department = Department.query.all()
    user1 = Users.query.all()
    coordinators = Users.query.filter_by(role='Coordinator').all()
    return render_template("bCommunity.html", community = all_data, program8=program8, user1 = user1, department=department, coordinators=coordinators)

####################################### BUDGET ######################################
@bor_route.route("/bBudget")
def bBudget():
    if g.current_user != "BOR":
        return redirect(url_for('dbModel.login'))

    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    form = Form()
    placeholder_choice = ("Literacy", "Literacy")
    form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
    form.program.default = ""
    form.process()
    form=form

    current_year = datetime.now().year

    # Retrieve all unique years from the Budget table
    all_years = Budget.query.with_entities(extract('year', Budget.date)).distinct()

    budget_years = sorted([year[0] for year in all_years])
    placeholder_choice = (current_year, current_year)
    budget_years_with_placeholder = [placeholder_choice] + [(year, year) for year in budget_years]

    ############################ FOR TOTAL BUDGET ##############################
    # Retrieve all budgets with the same year as the current date
    budgets_same_year = Budget.query.filter(extract('year', Budget.date) == current_year).all()
    total_budget_same_year = sum(budget.total for budget in budgets_same_year)
    budget_total = Budget.query.filter(Budget.budget_type == "Budget", extract('year', Budget.date) == current_year).first()
    fund_total = Budget.query.filter(Budget.budget_type == "Donation", extract('year', Budget.date) == current_year).first()
    # Set budget_total and fund_total to 0 if they are None and format to two decimal points
    budget_total_value = "{:.2f}".format(budget_total.total) if budget_total else "0.00"
    fund_total_value = "{:.2f}".format(fund_total.total) if fund_total else "0.00"
        
    ############################ FOR CURRENT BUDGET ##############################
    current_same_year = Current_Budget.query.filter(extract('year', Current_Budget.date) == current_year).all()
    total_current_same_year = sum(current.total for current in current_same_year)
    budget_current_total = Current_Budget.query.filter(Current_Budget.budget_type == "Budget", extract('year', Current_Budget.date) == current_year).first()
    fund_current_total = Current_Budget.query.filter(Current_Budget.budget_type == "Donation", extract('year', Current_Budget.date) == current_year).first()
    # Set budget_total and fund_total to 0 if they are None and format to two decimal points
    budget_current_total_value = "{:.2f}".format(budget_current_total.total) if budget_current_total else "0.00"
    fund_current_year_value = "{:.2f}".format(fund_current_total.total) if fund_current_total else "0.00"
    
    ############################ FOR BUDGET COST ##############################
    cost_same_year = Budget_cost.query.filter(extract('year', Budget_cost.date) == current_year).all()
    total_cost_same_year = sum(cost.total_cost for cost in cost_same_year)
    
    budget_cost_total = Budget_cost.query.filter(Budget_cost.budget_type == "Budget", extract('year', Budget_cost.date) == current_year).all()
    fund_cost_total = Budget_cost.query.filter(Budget_cost.budget_type == "Donation", extract('year', Budget_cost.date) == current_year).all()

    # Calculate total cost for budget and fund
    budget_total_sum = sum(budget.total_cost for budget in budget_cost_total) if budget_cost_total else 0
    fund_total_sum = sum(fund.total_cost for fund in fund_cost_total) if fund_cost_total else 0

    # Format the totals to two decimal points
    budget_cost_total_value = "{:.2f}".format(budget_total_sum)
    fund_cost_total_value = "{:.2f}".format(fund_total_sum)
    
    
    # FOR PROGRAMS' BUDGET:
    
    ############################ FOR TOTAL BUDGET ##############################
    # Retrieve all budgets with the same year as the current date
    budgets_same_year1 = Total_budget.query.filter(extract('year', Total_budget.date) == current_year, Total_budget.program == "Literacy").all()
    total_budget_same_year1_sum = sum(budget.total for budget in budgets_same_year1)
    total_budget_same_year1= "{:.2f}".format(total_budget_same_year1_sum)
    
    
    budget_total1 = Total_budget.query.filter(
    Total_budget.budget_type == "Budget",
    extract('year', Total_budget.date) == current_year,
    Total_budget.program == "Literacy"
    ).first()

    fund_total1 = Total_budget.query.filter(
        Total_budget.budget_type == "Donation",
        extract('year', Total_budget.date) == current_year,
        Total_budget.program == "Literacy"
    ).first()

    budget_total_value1 = "{:.2f}".format(budget_total1.total) if budget_total1 else "0.00"
    fund_total_value1 = "{:.2f}".format(fund_total1.total) if fund_total1 else "0.00"
        
    ############################ FOR CURRENT BUDGET PROGRAMS ##############################
    current_same_year1 = Current_total_budget.query.filter(extract('year', Current_total_budget.date) == current_year, Current_total_budget.program == "Literacy").all()
    
    total_current_same_year1_sum = sum(current.total for current in current_same_year1)
    total_current_same_year1= "{:.2f}".format(total_current_same_year1_sum)

    
    budget_current_total1 = Current_total_budget.query.filter(Current_total_budget.budget_type == "Budget", extract('year', Current_total_budget.date) == current_year, Current_total_budget.program == "Literacy").first()
    fund_current_total1 = Current_total_budget.query.filter(Current_total_budget.budget_type == "Donation", extract('year', Current_total_budget.date) == current_year, Current_total_budget.program == "Literacy").first()
    
    # Set budget_total and fund_total to 0 if they are None and format to two decimal points
    budget_current_total_value1 = "{:.2f}".format(budget_current_total1.total) if budget_current_total1 else "0.00"
    fund_current_year_value1 = "{:.2f}".format(fund_current_total1.total) if fund_current_total1 else "0.00"
    
    
    
    ############################ FOR BUDGET COST ##############################
    cost_same_year1 = Program_cost.query.filter(extract('year', Program_cost.date) == current_year, Program_cost.program == "Literacy").all()
    total_cost_same_year1_sum = sum(cost.total_cost for cost in cost_same_year1)
    total_cost_same_year1= "{:.2f}".format(total_cost_same_year1_sum)
    
    budget_cost_total1 = Program_cost.query.filter(Program_cost.budget_type == "Budget", extract('year', Program_cost.date) == current_year, Program_cost.program == "Literacy").all()
    fund_cost_total1 = Program_cost.query.filter(Program_cost.budget_type == "Donation", extract('year', Program_cost.date) == current_year, Program_cost.program == "Literacy").all()

    # Calculate total cost for budget and fund
    budget_total_cost = sum(budget.total_cost for budget in budget_cost_total1) if budget_cost_total1 else 0
    fund_total_cost = sum(fund.total_cost for fund in fund_cost_total1) if fund_cost_total1 else 0

    # Format the totals to two decimal points
    budget_cost_total_value1 = "{:.2f}".format(budget_total_cost)
    fund_cost_total_value1 = "{:.2f}".format(fund_total_cost)

    
    # Assuming current_year is defined elsewhere
    project_closure = Budget_program_cost.query.filter(func.extract('year', Budget_program_cost.date) == current_year).all()

    # Preprocess the data to replace None with 0
    for row in project_closure:
        row.budget = row.budget or 0
        row.cost = row.cost or 0
        row.balance = row.balance or 0

    
    # Render the template with the current year and the next four years
    return render_template("bBudget.html", form=form, current_year=current_year, budget_years_with_placeholder=budget_years_with_placeholder,total_budget_same_year=total_budget_same_year, budget_total=budget_total_value,fund_total=fund_total_value,budget_current_total_value=budget_current_total_value,fund_current_year_value=fund_current_year_value, total_current_same_year=total_current_same_year, total_cost_same_year=total_cost_same_year, budget_cost_total_value=budget_cost_total_value, fund_cost_total_value=fund_cost_total_value,
                           budget_total1=budget_total_value1,
                           fund_total1=fund_total_value1,
                           total_budget_same_year1=total_budget_same_year1,
                           total_current_same_year1=total_current_same_year1,
                           budget_current_total_value1=budget_current_total_value1,
                           fund_current_year_value1=fund_current_year_value1,
                           total_cost_same_year1=total_cost_same_year1,
                           budget_cost_total_value1=budget_cost_total_value1,
                           fund_cost_total_value1=fund_cost_total_value1, project_closure=project_closure)

@bor_route.route("/bResources")
def bResources():
    if g.current_user != "BOR":
        return redirect(url_for('dbModel.login'))

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    # Dynamically generate the years
    current_year = datetime.now().year
     # Fetch all user records from the database
    all_data = Resources.query.all()
    program8 = Program.query.all()
    user1 = Users.query.all()
    coordinators = Users.query.filter_by(role='Coordinator').all()
    return render_template("bResources.html", current_year=current_year, community = all_data, program8=program8, user1 = user1, coordinators=coordinators)
