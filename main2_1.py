# ==============================================================================
# ARQUIVO: main2-1.py
# OBJETIVO: Implementar Chain of Thought (CoT) para tipificação jurídica complexa
# ==============================================================================
from fastapi import FastAPI # Para criar a API
from pydantic import BaseModel # Para validação de dados
from openai import OpenAI # Para interagir com o modelo

# Conexão com o modelo
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama') 

# Inicialização da API
app = FastAPI(title="IntelliDoc - Módulo CoT")

# Modelo de dados
class Caso(BaseModel):
    relato: str
    delegacia: str = "PCDF"

# Rota de status
@app.get("/")
def verificar_status():
    return {"status": "online"}

# Rota de classificação simples
@app.post("/classificar_simples")  # O jeito "burro" (Zero-Shot)
def classificar_rapido(caso: Caso):
    prompt = "Classifique este crime juridicamente: " + caso.relato
    resp = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return {"classificacao": resp.choices[0].message.content}

# Rota de classificação com Chain of Thought
@app.post("/classificar_cot")  # O jeito "inteligente" (CoT)
def classificar_pensando(caso: Caso):
    # Engenharia de Prompt: Forçando a estrutura de pensamento [2][1]
    prompt_sistema = """
    Analise o relato como um Delegado de Policia, especialista em direito penal. 
    Siga ESTRICTAMENTE estes passos:
    
    PASSO 1 - Analise os Fatos com base nas palavras chave do relato
    PASSO 2 - Violência: Analise se houve violência física ou psíquica e/ou grave ameaça
    PASSO 3 - Vontade: Analise se a entrega do bem foi espontânea (mesmo que por engano) ou forçada
    PASSO 4 - Tipificação: Cruzes os passos 2 e 3 para definir o crime (Furto, Roubo, Estelionato, Apropriação Indébita).
    
    Saída:
    RACIOCINIO: [Resumo objetivo com base no direito penal brasileiro]
    VEREDITO: [nome do crime]
    """

    resp = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": caso.relato}
        ],
        temperature=0.2  # Um pouco de criatividade para a explicação
    )
    return {"analise": resp.choices[0].message.content}

# ==============================================================================
# RODAR NO TERMINAL:
# uvicorn main2_1:app --reload
# ==============================================================================