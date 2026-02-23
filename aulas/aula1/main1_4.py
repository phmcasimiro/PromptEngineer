# ==============================================================================
# ARQUIVO: main1_4.py
# OBJETIVO: Construir um endpoint de Chat com IA para Classificação de Crimes com técnica Chain of Thoughts
# ==============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI 

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama' 
)

app = FastAPI(title="IntelliDoc PCDF - Módulo 1")

class BoletimOcorrencia(BaseModel):
    relato: str
    delegacia: str = "PCDF Geral"

@app.get("/")
def verificar_status():
    return {"status": "online"}

# Rota anterior (Few-Shot) continua aqui...
@app.post("/analisar_inteligente")
def analisar_com_ia(bo: BoletimOcorrencia):
    print(f"Enviando para o Llama: {bo.relato}...")
    prompt_sistema = """
    Você é um classificador. Classifique em: [FURTO, ROUBO, ESTELIONATO].
    Exemplos:
    "Arma apontada" -> ROUBO
    "Sumiu da mesa" -> FURTO
    """
    response = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=[{"role": "system", "content": prompt_sistema},
                  {"role": "user", "content": bo.relato}],
        temperature=0.0
    )
    return {"classificacao": response.choices.message.content}

# [NOVO] Rota Avançada com Chain of Thought (CoT)
@app.post("/analisar_cot")
def analisar_raciocinio(bo: BoletimOcorrencia):
    print(f"Raciocínando sobre: {bo.relato}...")
    
    # PROMPT CoT: Passo a Passo
    prompt_cot = """
    Aja como um Delegado. Analise o caso seguindo este roteiro mental:
    
    PASSO 1: Fatos - Liste o que realmente aconteceu.
    PASSO 2: Violência - Houve grave ameaça ou violência física? (Sim/Não)
    PASSO 3: Subtração - O bem foi retirado ou entregue voluntariamente?
    
    Com base nisso, defina a tipificação penal.
    
    Formato de Resposta:
    RACIOCINIO: [Sua análise detalhada]
    VEREDITO: [FURTO, ROUBO ou ESTELIONATO]
    """
    
    response = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=[
            {"role": "system", "content": prompt_cot},
            {"role": "user", "content": bo.relato}
        ],
        temperature=0.1 # Leve criatividade para escrever a explicação
    )
    
    return {
        "tecnica": "Chain of Thought (CoT)",
        "analise_completa": response.choices[0].message.content
    }

# ==============================================================================
# RODAR NO TERMINAL:
# uvicorn main1_4:app --reload
# ==============================================================================