import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from flask import current_app

class GeminiService:
    @staticmethod
    def generate_mindmap(text_content):
        api_key = current_app.config.get('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("A chave GEMINI_API_KEY não foi encontrada nas configurações.")
            
        # Configura a chave
        genai.configure(api_key=api_key)
        
        # SOLUÇÃO DEFINITIVA: Força explicitamente a API estável (v1) e o modelo flash
        # Isso impede que o SDK tente usar caminhos 'v1beta' que geram o erro 404
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=GenerationConfig(response_mime_type="text/plain")
        )
        
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
            "Exemplo:\n"
            "mindmap\n"
            "root((Banco de Dados))\n"
            "  Conceitos\n"
            "    SGBD\n"
            "    Tabelas\n"
            "    Relacionamentos\n"
            "  Modelagem\n"
            "    Entidade\n"
            "    Atributo\n"
            "    Cardinalidade\n\n"
            f"Texto Acadêmico:\n{text_content}"
        )
        
        # Força o bypass do endpoint legado enviando a requisição direta na API estável
        response = model.generate_content(prompt)
        
        if not response.text:
            raise Exception("A API do Gemini retornou uma resposta em branco.")
            
        # Tratamento completo de strings para limpar o retorno da IA
        clean_code = response.text.replace("```mermaid", "").replace("```", "").strip()
        return clean_code