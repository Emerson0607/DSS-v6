from flask import Blueprint, redirect, url_for, render_template, session, flash, request, Response, g
from main.models.dbModel import Upload, User
from main import db


file_route = Blueprint('file', __name__)

def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = User.query.get(session['user_id'])
        if user:
            return user.firstname, user.role
    return None, None
    
@file_route.before_request
def before_request():
    g.current_user, g.current_role = get_current_user()

@file_route.context_processor
def inject_current_user():
    return dict(current_user=g.current_user, current_role=g.current_role)

# -------------------------   DL FILES for admin
@file_route.route('/files')
def files():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    upload_data = Upload.query.all()
    return render_template("dlfiles.html", upload_data=upload_data)

@file_route.route('/uploadfile', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # Read the file and insert it into the database
            data = file.read()
            upload_entry = Upload(filename=file.filename, data=data)
            db.session.add(upload_entry)
            db.session.commit()
    return redirect(url_for('file.files'))


@file_route.route('/view/<int:file_id>')
def view(file_id):
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
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    upload = Upload.query.get(id)
    if upload:
        try:
            # Delete the user from the database
            db.session.delete(upload)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
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
