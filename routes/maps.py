from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import db
from models.mindmap import MindMap

maps_bp = Blueprint('maps', __name__)

@maps_bp.route('/maps')
@login_required
def history():
    user_maps = MindMap.query.filter_by(user_id=current_user.id).order_by(MindMap.created_at.desc()).all()
    return render_template('maps/history.html', maps=user_maps)

@maps_bp.route('/maps/<int:map_id>')
@login_required
def view_map(map_id):
    mindmap = MindMap.query.get_or_404(map_id)
    if mindmap.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))
    return render_template('maps/view.html', mindmap=mindmap)

@maps_bp.route('/maps/<int:map_id>/delete', methods=['POST'])
@login_required
def delete_map(map_id):
    mindmap = MindMap.query.get_or_404(map_id)
    if mindmap.user_id == current_user.id:
        db.session.delete(mindmap)
        db.session.commit()
    return redirect(url_for('maps.history'))