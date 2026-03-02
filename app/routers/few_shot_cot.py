from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from app.config import MODEL_TEXT

router = APIRouter()


class Ocorrencia(BaseModel):
    relato: str


@router.post("/analisar")
async def analisar_few_shot_cot(bo: Ocorrencia):
    """
    Análise profunda de crime patrimonial combinando Few-Shot com Chain-of-Thought.
    Fornece um exemplo de raciocínio lógico (CoT) completo estruturado em JSON para guiar o LLM.
    """
    prompt_fscot = """
    Aja como um Delegado da PCDF. Analise o caso seguindo este roteiro mental:
    
    PASSO 1: Fatos - Liste objetivamente o que aconteceu.
    PASSO 2: Violência/Ameaça - Houve emprego de violência física, arma de fogo ou arma branca ou ameaça à integridade física da vítima?
    PASSO 3: Inversão da Posse - Como o bem saiu da vítima (subtração furtiva, entrega voluntária por erro, ou tomada à força)?
    
    EXEMPLO DE RACIOCÍNIO ESPERADO (FEW-SHOT):
    Ocorrência: "Um sujeito puxou a bolsa da mulher. Ela resistiu, ele deu um tapa e fugiu."
    {
        "analise_detalhada": {
            "fatos": "Homem avistou uma mulher, subtraiu sua bolsa e a agrediu fisicamente para garantir a posse.",
            "violencia": "Sim. Houve emprego de violência física (tapa).",
            "posse": "A coisa saiu da vítima por meio de força física."
        },
        "veredito": {
            "crime": "ROUBO"
        }
    }
    
    Siga ESTRITAMENTE o formato de raciocínio e o JSON acima para analisar a nova ocorrência.
    """

    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[
            {"role": "system", "content": prompt_fscot},
            {"role": "user", "content": f"OCORRÊNCIA PARA ANÁLISE: {bo.relato}"},
        ],
        format="json",
    )

    return response["message"]["content"]
