from flask import Blueprint, redirect, url_for, render_template, session, flash, request, Response, g
from main.models.dbModel import Upload, Users, Pending_project, Logs
from main import db
from datetime import datetime, timedelta

file_route = Blueprint('file', __name__)


def convert_date1(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = Users.query.get(session['user_id'])
        pending_count = Pending_project.query.filter_by(status="Pending").count()
            
        # Set a maximum value for pending_count
        max_pending_count = 9
        pending_count_display = min(pending_count, max_pending_count)

        # If pending_count is 9 or greater, display it as '9+'
        pending_count_display = '9+' if pending_count > max_pending_count else pending_count


        declined_count = Pending_project.query.filter_by(status="Declined", program=user.program).count()
            
        # Set a maximum value for pending_count
        max_declined_count = 9
        declined_count_display = min(declined_count, max_declined_count)

        # If pending_count is 9 or greater, display it as '9+'
        declined_count_display = '9+' if declined_count > max_declined_count else declined_count

        if user:
            return user.username, user.role, pending_count_display, declined_count_display
    return None, None, 0, 0

@file_route.before_request
def before_request():
    g.current_user, g.current_role, g.pending_count_display, g.declined_count_display = get_current_user()

@file_route.context_processor
def inject_current_user():
    return dict(current_user=g.current_user, current_role=g.current_role, pending_count = g.pending_count_display, declined_count = g.declined_count_display)

# -------------------------   DL FILES for admin
@file_route.route('/files')
def files():
     # Check if current_role is "admin"
    if g.current_role != "Admin":
        return redirect(url_for('dbModel.login')) 

    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    upload_data = Upload.query.all()
    return render_template("dlfiles.html", upload_data=upload_data)

@file_route.route('/uploadfile', methods=['POST'])
def upload():
    if g.current_role != "Admin":
        return redirect(url_for('dbModel.login')) 

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # Read the file and insert it into the database
            data = file.read()
            upload_entry = Upload(filename=file.filename, data=data)
            db.session.add(upload_entry)
            db.session.commit()
            flash('File uploaded successfully!', 'upload_file')

            userlog = g.current_user
            action = f'ADDED new file {file.filename}'
            timestamp1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamp = convert_date1(timestamp1)
            insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
            if insert_logs:
                db.session.add(insert_logs)
                db.session.commit()

    return redirect(url_for('file.files'))


@file_route.route('/view/<int:file_id>')
def view(file_id):
    if g.current_role != "Admin":
        return redirect(url_for('dbModel.login'))

    upload_entry = Upload.query.get(file_id)
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

@file_route.route('/delete_file/<int:id>', methods=['GET'])
def delete_file(id):
    if g.current_role != "Admin":
        return redirect(url_for('dbModel.login'))
        
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    upload = Upload.query.get(id)
    if upload:
        userlog = g.current_user
        action = f'DELETED file {upload.filename}'
        timestamp1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp = convert_date1(timestamp1)
        insert_logs = Logs(userlog = userlog, timestamp = timestamp, action = action)
        if insert_logs:
            db.session.add(insert_logs)
            db.session.commit()
        try:
            # Delete the user from the database
            db.session.delete(upload)
            db.session.commit()
            flash('File deleted successfully!', 'delete_file')
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('file.files'))

# -------------------------   DL FILES for COORDINATOR
@file_route.route('/cFiles')
def cFiles():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    upload_data = Upload.query.all()
    return render_template("cDlfiles.html", upload_data=upload_data)


@file_route.route('/cView/<int:file_id>')
def cView(file_id):
    upload_entry = Upload.query.get(file_id)
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
