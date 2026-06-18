import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import db
from models.document import Document
from models.mindmap import MindMap
from services.pdf_service import PDFService
from services.docx_service import DocxService
from services.gemini_service import GeminiService
from services.statistics_service import StatisticsService

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def process_content():
    if request.method == 'POST':
        title = request.form.get('title') or "Documento Sem Título"
        text_content = request.form.get('text_content')
        file = request.files.get('file')
        
        content = ""
        file_type = "text"
        filename = None
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            if filename.endswith('.pdf'):
                content = PDFService.extract_text(file_path)
                file_type = 'pdf'
            elif filename.endswith('.docx'):
                content = DocxService.extract_text(file_path)
                file_type = 'docx'
        else:
            content = text_content
            file_type = 'text'
            
        if not content or content.strip() == "":
            flash("Nenhum conteúdo válido foi processado.")
            return redirect(url_for('upload.process_content'))
            
        doc = Document(user_id=current_user.id, title=title, file_name=filename, file_type=file_type, content=content)
        db.session.add(doc)
        db.session.commit()
        
        words_count = len(content.split())
        StatisticsService.update_stats(current_user.id, words_count, inc_doc=True)
        
        try:
            mermaid_code = GeminiService.generate_mindmap(content)
            
            mindmap = MindMap(user_id=current_user.id, document_id=doc.id, title=f"Mapa - {title}", mermaid_code=mermaid_code)
            db.session.add(mindmap)
            db.session.commit()
            
            StatisticsService.update_stats(current_user.id, 0, inc_map=True)
            return redirect(url_for('maps.view_map', map_id=mindmap.id))
        except Exception as e:
            flash(f"Erro ao gerar mapa via IA: {str(e)}")
            return redirect(url_for('dashboard.index'))
            
    return render_template('dashboard/upload.html')