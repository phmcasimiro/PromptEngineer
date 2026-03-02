import sys
import os

# Adiciona a raiz do projeto ao path para importar o config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import chromadb
from chromadb.utils import embedding_functions
from app.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    MODEL_EMBEDDING,
    OLLAMA_API_EMBEDDING,
)


CHUNK_SEPARATOR = "<!-- CHUNK_BREAK -->"


def _extrair_titulo(chunk: str) -> str:
    """Extrai o título do chunk a partir do heading markdown."""
    for line in chunk.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("# ").strip()
    return "Bloco Geral"


def _extrair_crime(titulo: str) -> str:
    """Identifica o crime principal a partir do título do chunk."""
    titulo_lower = titulo.lower()
    if "furto de coisa comum" in titulo_lower:
        return "Furto de Coisa Comum"
    if "furto" in titulo_lower:
        return "Furto"
    if "latrocínio" in titulo_lower:
        return "Latrocínio"
    if "extorsão mediante sequestro" in titulo_lower:
        return "Extorsão Mediante Sequestro"
    if "extorsão indireta" in titulo_lower:
        return "Extorsão Indireta"
    if "extorsão" in titulo_lower:
        return "Extorsão"
    if "roubo" in titulo_lower:
        return "Roubo"
    if "jurisprudência" in titulo_lower or "jurisprudencias" in titulo_lower:
        return "Jurisprudência Geral"
    return "Geral"


def indexar_codigo_penal():
    # Indexa APENAS a doutrina otimizada para evitar ruído semântico da lei seca
    arquivos = [
        ("docs/CrimesPatrimonio_Comentarios.md", "Doutrina PCDF"),
    ]

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    ollama_ef = embedding_functions.OllamaEmbeddingFunction(
        url=OLLAMA_API_EMBEDDING, model_name=MODEL_EMBEDDING
    )

    # Recria a coleção limpa
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print(f"Coleção anterior '{COLLECTION_NAME}' removida.")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME, embedding_function=ollama_ef
    )

    documents = []
    ids = []
    metadatas = []
    chunk_global = 0

    for file_path, source_label in arquivos:
        if not os.path.exists(file_path):
            print(f"Aviso: {file_path} não encontrado. Pulando.")
            continue

        print(f"\nAbrindo {file_path} ({source_label})...")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Usa o separador <!-- CHUNK_BREAK --> para o comentário e --- para o CP puro
        if CHUNK_SEPARATOR in content:
            raw_chunks = content.split(CHUNK_SEPARATOR)
        else:
            raw_chunks = content.split("---")

        chunks = [
            c.strip()
            for c in raw_chunks
            if c.strip() and not c.strip().startswith("<!--")
        ]
        print(f"  {len(chunks)} chunks identificados.")

        for chunk in chunks:
            titulo = _extrair_titulo(chunk)
            crime = _extrair_crime(titulo)

            documents.append(chunk)
            ids.append(f"chunk_{chunk_global}")
            metadatas.append(
                {
                    "source": source_label,
                    "title": titulo,
                    "crime": crime,
                }
            )
            chunk_global += 1

    print(f"\nTotal: {chunk_global} chunks para indexar.")
    print("Gerando embeddings em lotes de 10... (isso pode demorar)")

    BATCH_SIZE = 10
    total = len(documents)
    for start in range(0, total, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total)
        collection.add(
            documents=documents[start:end],
            ids=ids[start:end],
            metadatas=metadatas[start:end],
        )
        print(f"  Lote {start // BATCH_SIZE + 1}: chunks {start + 1}–{end} indexados.")

    print(f"\nSucesso! {total} documentos indexados na coleção '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    indexar_codigo_penal()
