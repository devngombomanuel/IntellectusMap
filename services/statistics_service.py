from models.user import db
from models.statistics import Statistics

class StatisticsService:
    @staticmethod
    def update_stats(user_id, words_count, inc_doc=False, inc_map=False):
        stats = Statistics.query.filter_by(user_id=user_id).first()
        if not stats:
            stats = Statistics(user_id=user_id)
            db.session.add(stats)
        
        if inc_doc:
            stats.total_documents += 1
        if inc_map:
            stats.total_maps += 1
        stats.total_words += words_count
        db.session.commit()