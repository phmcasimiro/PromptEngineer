# ==============================================================================
# ARQUIVO: main2-2.py
# OBJETIVO: Receber uma imagem (arquivo) e gerar um laudo descritivo
# ==============================================================================
from fastapi import FastAPI # Importa a biblioteca FastAPI que permite criar APIs
from fastapi import UploadFile # Importa a biblioteca UploadFile que permite receber arquivos
from fastapi import File # Importa a biblioteca File que permite receber arquivos
from openai import OpenAI # Importa a biblioteca OpenAI que permite interagir com o modelo
import base64 # Importa a biblioteca base64

app = FastAPI(title="IntelliDoc - Visão") # Cria a API
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama') # Inicializa o cliente OpenAI

def encode_image(file_content):
    return base64.b64encode(file_content).decode('utf-8') # Codifica a imagem em base64

# Define a rota da API para verificar o status da API
@app.get("/")
def verificar_status():
    return {"status": "online"} # Retorna o status da API

# Define a rota da API para receber a imagem e gerar o laudo
@app.post("/descrever_evidencia")
async def ver_imagem(
    arquivo: UploadFile = File(...),
    foco: str = "Describe the objects in the image."
): 
    print(f"Processando imagem: {arquivo.filename}") # Imprime o nome do arquivo
    conteudo = await arquivo.read() # Lê o conteúdo do arquivo
    img_b64 = encode_image(conteudo) # Codifica a imagem em base64
    
    response = client.chat.completions.create(
        model="llava:7b", # Modelo multimodal leve
        messages=[
            {
                "role": "user",
                "content": foco, # O prompt guia o olhar da IA
                "images": [img_b64] # Envia a imagem para o modelo
            }
        ],
        temperature=0.2 # Define a temperatura do modelo
    )
    return {"laudo_visual": response.choices[0].message.content}

# ==============================================================================
# RODAR NO TERMINAL:
# uvicorn main2_2:app --reload
# ==============================================================================