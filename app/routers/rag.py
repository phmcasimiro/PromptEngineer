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


def _formatar_contexto(documentos: list[str], metadados: list[dict]) -> str:
    """Formata os chunks recuperados com título e fonte para o prompt."""
    partes = []
    for i, (doc, meta) in enumerate(zip(documentos, metadados), start=1):
        titulo = meta.get("title", "—")
        fonte = meta.get("source", "—")
        partes.append(f"[Fonte {i} — {fonte} | {titulo}]\n{doc}")
    return "\n\n".join(partes)


def _recuperar_chunks(texto: str) -> tuple[list[str], list[dict]]:
    """
    Recupera os 3 chunks mais relevantes da Doutrina PCDF.
    A doutrina já contém os artigos de lei embutidos em cada seção,
    tornando o CP puro redundante e potencialmente ruidoso.
    """
    resultado = collection.query(
        query_texts=[texto],
        n_results=3,
        where={"source": "Doutrina PCDF"},
    )
    return resultado["documents"][0], resultado["metadatas"][0]


@router.post("/tipificar_caso")
async def tipificar_com_rag(pergunta: Pergunta):
    """
    Tipificação penal de crimes patrimoniais via RAG.

    Recupera os 3 chunks mais relevantes da Doutrina PCDF
    e gera uma análise jurídica estruturada com base nesse contexto.
    """
    # ── Retrieval ─────────────────────────────────────────────────
    documentos, metadados = _recuperar_chunks(pergunta.texto)
    contexto_formatado = _formatar_contexto(documentos, metadados)

    # ── Augmented Generation ──────────────────────────────────────
    prompt_sistema = f"""
    Você é um Escrivão Jurídico da PCDF especializado em crimes contra o patrimônio.
    Analise o RELATO DO CASO abaixo e tipifique o crime com base no CONTEXTO JURÍDICO recuperado.

    CONTEXTO JURÍDICO RECUPERADO:
    {contexto_formatado}

    REGRAS DE FORMATAÇÃO E TIPAGEM:
    1. Se atenha aos verbos e aos substantivos do relato para tipificar o crime. 
    2. Se houver "violência física", "ameaça com arma" ou "ameaça de morte", trata-se de Roubo (Art. 157) ou Extorsão (Art. 158). Se pegar escondido, é Furto (Art. 155). Mas, se a pessoa entregar voluntariamente, é Estelionato (Art. 156).
    3. Identifique corretamente se há concurso de pessoas, emprego de arma (faca ou fogo) ou privação de liberdade.
    4. RESPONDA APENAS o objeto JSON puro, seguindo o esquema e os campos exatos solicitados. 
    5. Se a conduta descrita não se encaixar de jeito nenhum no contexto, preencha o campo crime com "NAO IDENTIFICADO".

    <Exemplo>
    Caso: "O homem encostou uma faca na minha costela e tomou meu relógio."
    {{
        "crime": "Roubo",
        "artigo": "Art. 157, §2º, VII, CP"
    }}
    </Exemplo>
    """

    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[
            {"role": "system", "content": prompt_sistema},
            {
                "role": "user",
                "content": f"RELATO DO CASO REAL: {pergunta.texto}\nSua tipificação em JSON:",
            },
        ],
        format="json",
        options={"temperature": 0.0},
    )

    return {
        "tipificacao": response["message"]["content"],
        "fontes_consultadas": [
            {
                "titulo": m.get("title"),
                "fonte": m.get("source"),
                "crime": m.get("crime"),
            }
            for m in metadados
        ],
    }
