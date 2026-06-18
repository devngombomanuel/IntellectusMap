from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.mindmap import MindMap
from models.statistics import Statistics

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    stats = Statistics.query.filter_by(user_id=current_user.id).first()
    latest_maps = MindMap.query.filter_by(user_id=current_user.id).order_by(MindMap.created_at.desc()).limit(5).all()
    
    last_activity = latest_maps[0].created_at.strftime('%d/%m/%Y %H:%M') if latest_maps else 'Nenhuma atividade recente'
    
    return render_template('dashboard/index.html', stats=stats, latest_maps=latest_maps, last_activity=last_activity)