from models.user import db
from datetime import datetime

class Statistics(db.Model):
    __tablename__ = 'statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_maps = db.Column(db.Integer, default=0)
    total_documents = db.Column(db.Integer, default=0)
    total_words = db.Column(db.Integer, default=0)
    study_time = db.Column(db.Integer, default=0) # em minutos
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)