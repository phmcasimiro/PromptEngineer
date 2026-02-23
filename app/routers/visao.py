from fastapi import APIRouter, UploadFile, File
import ollama
import base64
from app.config import MODEL_VISION

router = APIRouter()


def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


@router.post("/analisar_evidencia")
async def analisar_imagem(arquivo: UploadFile = File(...)):
    """
    Análise técnica de evidência visual (imagem) de crime patrimonial.
    """
    conteudo = await arquivo.read()
    img_b64 = encode_image(conteudo)

    prompt_sistema = """
    Você é um Perito Criminal da PCDF especializado em Crimes Patrimoniais.
    Sua função é analisar a imagem de uma cena de crime ou evidência e descrever danos, ferramentas ou objetos estranhos.
    
    RESPONDA APENAS UM JSON VÁLIDO:
    {
        "descricao_da_evidencia": "Descrição técnica detalhada",
        "danos_identificados": "Ex: rompimento de cadeado, vidro quebrado, etc",
        "objetos_relevantes": ["lista", "de", "objetos"],
        "classificacao_da_cena": "Ex: arrombamento de residência, fraude em caixa eletrônico"
    }
    """

    response = ollama.chat(
        model=MODEL_VISION,
        messages=[{"role": "user", "content": prompt_sistema, "images": [img_b64]}],
        format="json",
    )

    return response["message"]["content"]
