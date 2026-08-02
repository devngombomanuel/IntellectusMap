import requests
from flask import current_app

class GeminiService:
    @staticmethod
    def generate_mindmap(text_content):
        api_key = current_app.config.get('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("A chave GEMINI_API_KEY não foi encontrada nas configurações.")
            
      
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
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
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        if response.status_code != 200:
            error_msg = response_data.get('error', {}).get('message', 'Erro desconhecido na API do Google')
            raise Exception(f"Erro {response.status_code}: {error_msg}")
            
        try:
            generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
            return generated_text.replace("```mermaid", "").replace("```", "").strip()
        except KeyError:
            raise Exception("A estrutura de resposta da IA veio em um formato inesperado.")