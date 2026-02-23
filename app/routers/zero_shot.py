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
    Sua tarefa é ler um relato e indicar qual o crime provável e o nível de gravidade.
    
    RESPONDA APENAS EM JSON:
    {
        "crime_provavel": "NOME DO CRIME",
        "gravidade": "ALTA/MÉDIA/BAIXA",
        "resumo_curto": "Um pequeno resumo de 1 frase"
    }
    """
    # Prompt do usuário, que é enviado para o modelo para que ele execute a tarefa
    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[
            {"role": "system", "content": prompt_sistema}, # Prompt do sistema
            {"role": "user", "content": f"RELATO DA OCORRÊNCIA: {relato.texto}"}, # Prompt do usuário
        ],
        format="json", # Formato de saída
    )
    # Retorno da API
    return response["message"]["content"]
