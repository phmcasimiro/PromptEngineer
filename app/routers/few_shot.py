from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from app.config import MODEL_TEXT

router = APIRouter()


# Classe que define o modelo de dados para a requisição
class Relato(BaseModel):
    texto: str


# Endpoint para classificação de crime patrimonial usando Few-Shot (com exemplos)
@router.post("/analisar")
async def analisar_few_shot(relato: Relato):
    # Prompt do sistema, que é enviado para o modelo para que ele entenda o contexto da tarefa
    prompt_sistema = """
    Você é um Escrivão especialista da PCDF. Analise o relato e tipifique o crime na sua forma mais genérica.

    EXEMPLOS DE TIPIFICAÇÃO MACRO:

    Exemplo 1: (Categoria: SUBTRAÇÃO SEM VIOLÊNCIA)
    Relato: "De madrugada, pulou o muro da minha casa, quebrou o cadeado e levou minha bicicleta que estava no quintal escondida."
    Resposta: { "tipificacao": "FURTO", "base_legal": "Art. 155", "explicacao": "Subtração de coisa alheia móvel para si ou para outrem, sem o emprego de violência ou grave ameaça contra a pessoa." }

    Exemplo 2: (Categoria: SUBTRAÇÃO COM VIOLÊNCIA/AMEAÇA)
    Relato: "O homem me abordou na parada de ônibus com uma faca, me deu um empurrão e arrancou o celular da minha mão à força."
    Resposta: { "tipificacao": "ROUBO", "base_legal": "Art. 157", "explicacao": "Subtração de coisa alheia móvel mediante o emprego de violência física ou grave ameaça." }

    Exemplo 3: (Categoria: COAÇÃO / PARTICIPAÇÃO DA VÍTIMA)
    Relato: "Fui abordado por bandidos armados que me obrigaram a entrar no carro, rodar pela cidade e fazer saques no caixa eletrônico. Eles ameaçaram atirar se eu não digitasse a senha."
    Resposta: { "tipificacao": "EXTORSÃO", "base_legal": "Art. 158", "explicacao": "Constranger alguém, mediante violência ou ameaça, a fazer ou tolerar algo (digitar senha/sacar) visando indevida vantagem econômica." }

    Exemplo 4: (Categoria: ENGANO / FRAUDE)
    Relato: "Recebi um link dizendo que tinha uma dívida falsa. Fiquei assustado, cliquei no link, preenchi meus dados bancários e transferi o valor voluntariamente."
    Resposta: { "tipificacao": "ESTELIONATO", "base_legal": "Art. 171", "explicacao": "Obtenção de vantagem ilícita induzindo a vítima a erro de forma voluntária, sem o uso de violência." }

    RESPONDA SEMPRE EM JSON seguindo estritamente o formato de chaves dos exemplos: "tipificacao", "base_legal" e "explicacao".
    """
    # Prompt do usuário, que é enviado para o modelo para que ele execute a tarefa
    response = ollama.chat(
        model=MODEL_TEXT,  # Modelo de texto
        messages=[  # Mensagens da conversa
            {"role": "system", "content": prompt_sistema},  # Prompt do sistema
            {
                "role": "user",
                "content": f"RELATO ATUAL: {relato.texto}",
            },  # Prompt do usuário
        ],
        format="json",  # Formato da resposta
    )
    # Retorno da API
    return response["message"]["content"]
