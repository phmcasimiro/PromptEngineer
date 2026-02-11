from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import json

# 1. Definição do App
app = FastAPI(
    title="Classificador de Crimes - AI Engineering",
    description="API para classificação de notícias de segurança pública usando Ollama"
)

# 2. Modelo de dados para entrada (JSON do Swagger)
class Noticia(BaseModel):
    text: str

# 3. Lógica de Prompt Engineering (Few Shot)
SYSTEM_PROMPT = """
Você é um assistente especializado em segurança pública brasileira.
Sua tarefa é ler uma notícia e classificar o crime conforme os exemplos abaixo:

Exemplo 1:
Notícia: "Indivíduo levou a carteira da vítima que estava distraída no metrô, sem que ela percebesse."
Resposta: {"categoria": "FURTO", "justificativa": "Subtração de bens sem uso de violência ou ameaça."}

Exemplo 2:
Notícia: "Dois homens armados renderam o motorista e levaram o carro sob graves ameaças."
Resposta: {"categoria": "ROUBO", "justificativa": "Subtração de bem mediante uso de arma e ameaça direta."}

Agora, classifique a notícia fornecida seguindo este padrão de JSON.
Categorias permitidas: [HOMICIDIO, ROUBO, FURTO, TRAFICO, ESTELIONATO, OUTROS].
"""

@app.post("/classificar")
async def classificar_noticia(noticia: Noticia):
    try:
        # Chamada assíncrona ao Ollama
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': f"Classifique esta notícia: {noticia.text}"}
            ],
            format='json' # Garante que o Ollama tente retornar um JSON válido
        )

        # Parse do conteúdo retornado pela IA
        resultado_ia = json.loads(response['message']['content'])
        
        return {
            "status": "sucesso",
            "entrada": noticia.text,
            "classificacao": resultado_ia
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar IA: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)