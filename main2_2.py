# ==============================================================================
# ARQUIVO: main2-2.py
# OBJETIVO: Receber uma imagem (arquivo) e gerar um laudo descritivo
# ==============================================================================
from fastapi import FastAPI  # Importa a biblioteca FastAPI que permite criar APIs
from fastapi import UploadFile  # Importa a biblioteca UploadFile que permite receber arquivos
from fastapi import File  # Importa a biblioteca File que permite receber arquivos
from openai import OpenAI  # Importa a biblioteca OpenAI que permite interagir com o modelo
import base64  # Importa a biblioteca base64

app = FastAPI(title="IntelliDoc - Visão") # Cria a API
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama') # Inicializa o cliente OpenAI

# Modelos de Visão Computacional
# Codifica a imagem em base64
def encode_image(file_content):
    return base64.b64encode(file_content).decode("utf-8") 


# Define a rota da API para verificar o status da API
@app.get("/")
def verificar_status():
    return {"status": "online"}  # Retorna o status da API


# Define a rota da API para receber a imagem e gerar o laudo
@app.post("/descrever_evidencia")
async def ver_imagem(
    arquivo: UploadFile = File(...), foco: str = "Describe the objects in the image."
):
    print(f"Processando imagem: {arquivo.filename}")  # Imprime o nome do arquivo
    conteudo = await arquivo.read()  # Lê o conteúdo do arquivo
    img_b64 = encode_image(conteudo)  # Codifica a imagem em base64

    # Engenharia de Prompt: Persona e Estrutura JSON
    prompt_sistema = """
    Você é um Perito Criminal de Elite da Polícia Técnica.
    Sua função é analisar tecnicamente a imagem da cena do crime/acidente.
    
    REGRAS DE RESPOSTA (OBRIGATÓRIO):
    1. Analise a imagem com frieza e objetividade técnica.
    2. Responda APENAS um objeto JSON válido. Não adicione texto antes ou depois.
    3. O JSON deve seguir este formato estrito:
    {
        "classificacao_cena": "Tipo do ambiente",
        "objetos_principais": "Lista de objetos principais relevantes",
        "detalhes_tecnicos": "Descrição detalhada dos objetos principais",
    }
    """

    response = client.chat.completions.create(
        model="qwen3-vl:8b",  # Modelo multimodal
        messages=[
            {
                "role": "user",
                "content": prompt_sistema + f"\n\nFOCO DA ANÁLISE: {foco}",
                "images": [img_b64],
            }
        ],
        temperature=0.1,  # Temperatura baixa para garantir a estrutura JSON
    )

    # Tentativa de limpar a resposta caso o modelo seja "verboso" (markdown json)
    resposta_texto = (
        response.choices[0]
        .message.content.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return {"laudo_tecnico": resposta_texto}


# ==============================================================================
# RODAR NO TERMINAL:
# uvicorn main2_2:app --port 8001--reload
# ==============================================================================
