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
        # Captura dos dados do formulário
        name = request.form.get('name')
        course = request.form.get('course')
        university = request.form.get('university')
        academic_year = request.form.get('academic_year')
        bio = request.form.get('bio')
        file = request.files.get('profile_photo')

        # Atualização do modelo do usuário atual
        current_user.name = name if name else current_user.name
        current_user.course = course
        current_user.university = university
        current_user.academic_year = academic_year
        current_user.bio = bio

        # Processamento do upload da foto de perfil direto na pasta uploads/
        if file and file.filename != '':
            filename = f"user_{current_user.id}_{secure_filename(file.filename)}"
            
            # Salva direto em static/uploads/ que já é criada automaticamente pelo app.py
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Salva o caminho simplificado no banco de dados
            current_user.profile_photo = f"uploads/{filename}"

        try:
            db.session.commit()
            flash('Perfil updated com sucesso!', 'success')
            return redirect(url_for('profile.view_profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar o perfil: {str(e)}', 'danger')

    return render_template('profile/view.html', stats=stats)