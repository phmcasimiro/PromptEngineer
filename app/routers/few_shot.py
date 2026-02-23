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
    Você é um Escrivão especialista da PCDF. Analise o relato e tipifique o crime.
    
    EXEMPLOS:
    
    Exemplo 1:
    Relato: "Deixei meu celular na mesa do restaurante e fui ao banheiro. Quando voltei, tinha sumido."
    Resposta: { "tipificacao": "FURTO SIMPLES", "base_legal": "Art. 155, caput", "explicacao": "Subtração de coisa alheia móvel sem violência." }
    
    Exemplo 2:
    Relato: "Um homem me abordou com uma faca e mandou eu entregar a bolsa."
    Resposta: { "tipificacao": "ROUBO", "base_legal": "Art. 157, § 2º, VII", "explicacao": "Subtração mediante grave ameaça com emprego de arma branca." }
    
    Exemplo 3:
    Relato: "Recebi um link dizendo que ganhei um prêmio. Cliquei, pediram meus dados do banco e depois sumiu dinheiro da conta."
    Resposta: { "tipificacao": "ESTELIONATO ELETRÔNICO", "base_legal": "Art. 171, § 2º-A", "explicacao": "Obtenção de vantagem ilícita induzindo a vítima a erro via meio eletrônico." }
    
    RESPONDA SEMPRE EM JSON seguindo o padrão acima.
    """
    # Prompt do usuário, que é enviado para o modelo para que ele execute a tarefa  
    response = ollama.chat(
        model=MODEL_TEXT, # Modelo de texto
        messages=[ # Mensagens da conversa
            {"role": "system", "content": prompt_sistema}, # Prompt do sistema
            {"role": "user", "content": f"RELATO ATUAL: {relato.texto}"}, # Prompt do usuário
        ],
        format="json", # Formato da resposta
    )
    # Retorno da API
    return response["message"]["content"]
