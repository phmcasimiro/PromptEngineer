# ==============================================================================
# ARQUIVO: main3_2.py (API RAG)
# OBJETIVO: API para o sistema de IA que cria a memória do assistente
# ==============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

app = FastAPI(title="IntelliDoc - Módulo RAG")

# 1. Conexão com a Memória (Igual ao script anterior)
chroma_client = chromadb.PersistentClient(path="./banco_vetorial")
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="qwen3-embedding:latest"
)
collection = chroma_client.get_collection(name="inqueritos_pcdf", embedding_function=ollama_ef)

# 2. Conexão com o Cérebro (Llama)
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

class Pergunta(BaseModel):
    texto: str

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao IntelliDoc - Módulo RAG"}

@app.post("/investigar")
def investigar_caso(pergunta: Pergunta):
    print(f"Buscando evidências para: {pergunta.texto}")

    # PASSO 1: Retrieval (Recuperação)
    # Buscamos no banco os 3 trechos mais parecidos com a pergunta
    resultados = collection.query(
        query_texts=[pergunta.texto],
        n_results=3 # Traz os top 3 pedaços mais relevantes
    )

    # Juntamos os pedaços recuperados em um único texto
    contexto_recuperado = "\n".join(resultados['documents'][0])
    print(f"Contexto encontrado: {contexto_recuperado}")

    # PASSO 2: Augmented Generation (Geração Aumentada)
    # Colamos o contexto no prompt do sistema
    prompt_sistema = f"""
    Você é um assistente de inteligência policial.
    Responda à pergunta do usuário usando APENAS o contexto abaixo.
    Se a resposta não estiver no contexto, diga "Não consta nos autos".

    CONTEXTO DOS AUTOS:
    {contexto_recuperado}
    """

    response = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": pergunta.texto}
        ],
        temperature=0.9
    )

    return {
        "pergunta": pergunta.texto,
        "resposta": response.choices[0].message.content,
        "fontes_utilizadas": resultados['documents']
    }

# ==============================================================================
# RODAR NO TERMINAL:
# uvicorn main3_2:app --port:8001 --reload
# ==============================================================================