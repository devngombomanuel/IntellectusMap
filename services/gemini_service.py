import google.generativeai as genai
from flask import current_app

class GeminiService:
    @staticmethod
    def generate_mindmap(text_content):
        api_key = current_app.config.get('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("A chave GEMINI_API_KEY não foi encontrada nas configurações.")
            
        genai.configure(api_key=api_key)
        
        # Tentativa com o nome de modelo legado estável de texto que ignora o roteamento v1beta
        try:
            model = genai.GenerativeModel('gemini-1.0-pro')
            
            prompt = (
                "Você é um especialista em análise acadêmica e organização de conhecimento.\n\n"
                "Analise o texto fornecido.\n\n"
                "Regras:\n"
                "* Utilize apenas as informações presentes no texto.\n"
                "* Não invente conceitos.\n"
                "* Identifique tema principal.\n"
                "* Identifique subtemas.\n"
                "* Identifique conceitos importantes.\n"
                "* Identifique relações entre conceitos.\n"
                "* Organize tudo em formato Mermaid Mindmap.\n"
                "* Retorne somente código Mermaid.\n"
                "* Não adicione explicações.\n\n"
                f"Texto Acadêmico:\n{text_content}"
            )
            
            response = model.generate_content(prompt)
            return response.text.replace("```mermaid", "").replace("```", "").strip()
            
        except Exception:
            # Fallback de emergência caso o servidor do Google recuse o modelo pro
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(prompt)
            return response.text.replace("```mermaid", "").replace("```", "").strip()