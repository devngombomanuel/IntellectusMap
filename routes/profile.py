import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import db, User
from models.statistics import Statistics

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    stats = Statistics.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        new_email = request.form.get('email')
        name = request.form.get('name')
        course = request.form.get('course')
        university = request.form.get('university')
        academic_year = request.form.get('academic_year')
        bio = request.form.get('bio')
        file = request.files.get('profile_photo')

        if new_email and new_email != current_user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                flash('Este e-mail já está sendo usado por outra conta.', 'danger')
                return redirect(url_for('profile.view_profile'))
            current_user.email = new_email

        current_user.name = name if name else current_user.name
        current_user.course = course
        current_user.university = university
        current_user.academic_year = academic_year
        current_user.bio = bio

        if file and file.filename != '':
            filename = f"user_{current_user.id}_{secure_filename(file.filename)}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            current_user.profile_photo = f"uploads/{filename}"

        try:
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('profile.view_profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar o perfil: {str(e)}', 'danger')

    return render_template('profile/view.html', stats=stats)