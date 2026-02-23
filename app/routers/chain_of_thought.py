from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from app.config import MODEL_TEXT

router = APIRouter()


class Ocorrencia(BaseModel):
    relato: str


@router.post("/analisar_cot")
async def analisar_raciocinio(bo: Ocorrencia):
    """
    Análise profunda de crime patrimonial usando Chain-of-Thought.
    """
    prompt_cot = """
    Aja como um Delegado da PCDF. Analise o caso seguindo este roteiro mental:
    
    PASSO 1: Fatos - Liste objetivamente o que aconteceu.
    PASSO 2: Violência/Ameaça - Houve emprego de força física ou grave ameaça contra a pessoa?
    PASSO 3: Inversão da Posse - Como o bem saiu da vítima (subtração furtiva, entrega voluntária por erro, ou tomada à força)?
    PASSO 4: Qualificadoras - Há sinais de rompimento de obstáculo, concurso de pessoas, ou uso de fraude eletrônica?
    
    Com base nisso, defina a tipificação penal e fundamente.
    
    RESPONDA APENAS EM JSON:
    {
        "analise_detalhada": {
            "fatos": "...",
            "violencia": "...",
            "posse": "...",
            "qualificadoras": "..."
        },
        "veredito": {
            "crime": "...",
            "artigo": "...",
            "fundamentacao_juridica": "..."
        }
    }
    """

    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[
            {"role": "system", "content": prompt_cot},
            {"role": "user", "content": f"OCORRÊNCIA PARA ANÁLISE: {bo.relato}"},
        ],
        format="json",
    )

    return response["message"]["content"]
