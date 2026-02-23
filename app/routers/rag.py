from fastapi import APIRouter
from pydantic import BaseModel
import ollama
import chromadb
from chromadb.utils import embedding_functions
from app.config import (
    MODEL_TEXT,
    CHROMA_PATH,
    COLLECTION_NAME,
    MODEL_EMBEDDING,
    OLLAMA_API_EMBEDDING,
)

router = APIRouter()


class Pergunta(BaseModel):
    texto: str


# Configuração do Cliente e Coleção
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url=OLLAMA_API_EMBEDDING, model_name=MODEL_EMBEDDING
)
collection = chroma_client.get_collection(
    name=COLLECTION_NAME, embedding_function=ollama_ef
)


@router.post("/tipificar_caso")
async def tipificar_com_rag(pergunta: Pergunta):
    """
    Tipificação penal baseada no Código Penal via RAG.
    """
    # Recuperação (Retrieval)
    resultados = collection.query(query_texts=[pergunta.texto], n_results=3)

    contexto_legal = "\n\n".join(resultados["documents"][0])

    # Geração Aumentada (Generation)
    prompt_sistema = f"""
    Você é um Escrivão Jurídico da PCDF. 
    Analise o caso abaixo e tipifique o crime usando APENAS a BASE LEGAL fornecida.
    Se a resposta não estiver na base legal, diga que são necessários mais detalhes para conclusão conforme o CP.

    BASE LEGAL RECUPERADA:
    {contexto_legal}
    """

    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"CASO PARA ANÁLISE: {pergunta.texto}"},
        ],
        format="json",
    )

    return {
        "analise_baseada_no_cp": response["message"]["content"],
        "fontes_consultadas": resultados["metadatas"][0],
    }
