import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do Ollama
# URL base do Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# URL da API v1 do Ollama
OLLAMA_API_V1 = f"{OLLAMA_BASE_URL}/v1"
# URL da API de Embeddings do Ollama
OLLAMA_API_EMBEDDING = f"{OLLAMA_BASE_URL}/api/embeddings"

# Modelos
# Modelo de texto, o qual será usado para classificação de crimes
MODEL_TEXT = os.getenv("MODEL_TEXT", "llama3.2:1b")
# Modelo de visão, o qual será usado para análise de imagens de evidências
MODEL_VISION = os.getenv("MODEL_VISION", "qwen3-vl:8b")
# Modelo de embeddings, o qual será usado para busca semântica no Código Penal
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING", "nomic-embed-text")

# Configurações do ChromaDB
# Caminho do banco de vetores
CHROMA_PATH = os.getenv("CHROMA_PATH", "./banco_vetorial")
# Nome da coleção de vetores
COLLECTION_NAME = "crimes_patrimonio"
