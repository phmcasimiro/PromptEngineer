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


def indexar_codigo_penal():
    file_path = "docs/CrimesPatrimonio_CP.md"

    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    print(f"Abrindo {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Dividindo por artigos (usando o separador --- que inseri na formatação)
    chunks = [c.strip() for c in content.split("---") if c.strip()]
    print(f"Total de {len(chunks)} blocos identificados para indexação.")

    # Conexão com ChromaDB
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Função de Embedding do Ollama
    ollama_ef = embedding_functions.OllamaEmbeddingFunction(
        url=OLLAMA_API_EMBEDDING, model_name=MODEL_EMBEDDING
    )

    # Deleta se já existir para garantir indexação limpa (opcional, mas recomendado no setup)
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print(f"Coleção anterior '{COLLECTION_NAME}' removida.")
    except:
        pass

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME, embedding_function=ollama_ef
    )

    # Indexação
    documents = []
    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        # Tenta extrair o título do Artigo para o metadado (ex: ### Art. 155)
        # O chunk começa com o título se seguir a formatação
        title = "Artigo Geral"
        lines = chunk.split("\n")
        for line in lines:
            if "Art." in line or "Capítulo" in line:
                title = line.strip("# ").strip()
                break

        documents.append(chunk)
        ids.append(f"cp_chunk_{i}")
        metadatas.append({"source": "Código Penal", "title": title})

    print("Gerando embeddings e salvando no banco... (isso pode demorar)")
    collection.add(documents=documents, ids=ids, metadatas=metadatas)

    print(
        f"Sucesso! {len(documents)} documentos indexados na coleção '{COLLECTION_NAME}'."
    )


if __name__ == "__main__":
    indexar_codigo_penal()
