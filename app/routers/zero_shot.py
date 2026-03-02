import json

from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from app.config import MODEL_TEXT

router = APIRouter()


class Relato(BaseModel):
    texto: str


@router.post("/classificar")
async def classificar_zero_shot(relato: Relato):
    """
    Classificação rápida de crime patrimonial usando Zero-Shot.
    """
    # Prompt do sistema, que é enviado para o modelo para que ele entenda o contexto da tarefa
    prompt_sistema = """
    Você é um Escrivão de Polícia Virtual da PCDF especializado em crimes contra o patrimônio.
    Sua tarefa é ler um relato e indicar qual o crime provável.
    
    RESPONDA APENAS EM JSON:
    {
        "crime_provavel": "NOME DO CRIME",
        "resumo_curto": "Um pequeno resumo de 1 frase"
    }
    """
    # Prompt do usuário, que é enviado para o modelo para que ele execute a tarefa
    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[
            {"role": "system", "content": prompt_sistema},  # Prompt do sistema
            {
                "role": "user",
                "content": f"RELATO DA OCORRÊNCIA: {relato.texto}",
            },  # Prompt do usuário
        ],
        format="json",  # Formato de saída
    )

    # O modelo pequeno às vezes retorna a chave com acento ("crime_provável").
    # Precisamos normalizar para garantir compatibilidade com o frontend, sem alterar o prompt Zero-Shot.
    try:
        dados = json.loads(response["message"]["content"])
        if "crime_provável" in dados and "crime_provavel" not in dados:
            dados["crime_provavel"] = dados.pop("crime_provável")
        return dados
    except (json.JSONDecodeError, KeyError):
        # Fallback: retorna o conteúdo bruto se o JSON for inválido
        return response["message"]["content"]
