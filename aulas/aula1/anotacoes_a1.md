# Aula 1: Fundamentos de API e Engenharia de Prompt (Zero-Shot, Few-Shot e CoT)

## Objetivo da Aula
O foco desta primeira aula foi construir a base do projeto web (uma API policial usando FastAPI) e introduzir, gradativamente, as três técnicas fundamentais de Engenharia de Prompt para classificar relatos de crimes usando a IA local (Ollama).

---

## Solução Arquitetural
- **FastAPI**: Framekwork Python escolhido para criar o servidor web. Permite que o código Python se torne acessível via internet/rede através de requisições HTTP (GET, POST).
- **Pydantic (BaseModel)**: Usado para criar um "contrato de dados". A classe `BoletimOcorrencia` garante que a API só aceite requisições válidas (que contenham obrigatoriamente um texto chamado `relato`).
- **OpenAI (Client)**: A biblioteca oficial da OpenAI foi usada para conectar com o Ollama rodando localmente.

### Por que usar a biblioteca oficial da OpenAI com o Ollama?

1. **O Padrão da Indústria (A 'Tomada Universal')**
A OpenAI (criadora do ChatGPT) dominou o mercado de IA tão rápido que o formato de código que ela criou para conversar com a Inteligência Artificial acabou virando um "padrão global" na indústria de programação.
É como se a OpenAI tivesse inventado o padrão de tomada de 3 pinos. Todas as outras empresas e ferramentas que surgiram depois (como o Ollama, Groq, LM Studio, vLLM) perceberam que, se quisessem ter sucesso, suas IAs precisariam "encaixar" nessa mesma tomada.

2. **Como a "Mágica" do Ollama Funciona**
O Ollama foi programado intencionalmente para ser um "Falso ChatGPT". Ele abre uma porta no seu computador (http://localhost:11434/v1) que escuta e fala exatamente o mesmo idioma técnico que os servidores milionários da OpenAI falam.
Por isso, quando o Python usa a biblioteca oficial openai (`client = OpenAI(...)`), a biblioteca acha que está conversando com a verdadeira OpenAI pela internet, mas na verdade o Ollama está "enganando" a biblioteca, processando tudo localmente na placa de vídeo do seu computador de forma gratuita e privada.

3. **A Vantagem de Design ensinada pelo Professor**
O professor fez isso para ensinar a você o conceito de Zero Vendor Lock-in (Fuga da Dependência de Fornecedor).
Se você usar sempre a biblioteca da openai no seu código fonte do IntelliDoc PCDF, o seu sistema policial estará preparado para qualquer cenário futuro, alterando literalmente apenas uma linha de código:
- Faltou internet na Delegacia? (Ou dados hiper-sigilosos): Você aponta o código para o Ollama local: `client = OpenAI(base_url='http://localhost:11434/v1', api_key='fake')`
- Inquérito gigantesco e o Ollama ficou muito lento? Você apaga o base_url e coloca a sua chave de cartão de crédito real da OpenAI. Instantaneamente, sem reescrever uma única vírgula de lógica no resto da API, o sistema passa a usar o poder de supercomputadores online: `client = OpenAI(api_key='sk-SUACHAVEREAL')`

Se o professor tivesse ensinado as primeiras aulas usando a biblioteca oficial do Ollama (como ele fez só lá na Aula 4 para mostrar recursos específicos de JSON), e o Governo do DF amanhã assinasse um super contrato com a OpenAI, você teria que reescrever boa parte do seu código. Usando o padrão OpenAI(), seu código "nasce" universal.

Exemplo de configuração da arquitetura de API (`main1_1.py`):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IntelliDoc PCDF - Módulo 1")

class BoletimOcorrencia(BaseModel):
    relato: str
    delegacia: str = "PCDF Geral"

@app.post("/analisar")
def receber_relato(bo: BoletimOcorrencia):
    return {"recebido": bo.relato}
```

---

## Técnicas de Prompt Apresentadas

A aula evoluiu a inteligência do sistema em três etapas (representadas nos arquivos `main1_2` a `main1_4`):

### 1. Zero-Shot Prompting (`main1_2.py`)
* **Conceito:** É a forma mais rudimentar de pedir algo para a IA. Damos a instrução direta de classificação sem apresentar nenhum exemplo prévio. É literalmente um "tiro no escuro" contando com o conhecimento pré-treinado do modelo.
* **Parâmetro de Temperatura:** Ajustado para `0.2` para forçar a IA a ser mais determinística e menos criativa.

Exemplo de código:
```python
prompt_sistema = """
Você é um especialista criminal da PCDF.
Classifique o relato ABAIXO como: FURTO, ROUBO ou ESTELIONATO.
Responda apenas a classificação.
"""

response = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": bo.relato}
    ],
    temperature=0.2
)
```

### 2. Few-Shot Prompting (`main1_3.py`)
* **Conceito:** A técnica de injetar exemplos (gabaritos pré-resolvidos) dentro do próprio prompt antes de pedir para a IA analisar a questão atual.
* **Vantagem:** O modelo entende instantaneamente qual é o padrão lógico e o formato exato esperado.

Exemplo de código demonstrando o Prompt Few-Shot:
```python
prompt_sistema = """
Você é um classificador automático da PCDF.
REGRAS OBRIGATÓRIAS:
1. Analise o relato.
2. Classifique ESTRITAMENTE em uma destas categorias: [FURTO, ROUBO, ESTELIONATO].

EXEMPLOS DE TREINAMENTO (Siga este padrão):

Relato: "Levaram meu celular da mesa sem eu ver."
Classificação: FURTO

Relato: "Dois homens armados levaram meu carro."
Classificação: ROUBO

Agora classifique o novo relato:
"""
```

### 3. Chain of Thought - CoT (`main1_4.py`)
* **Conceito:** CoT (Corrente de Pensamento) é forçar a IA a pensar em etapas (passo a passo) antes de dar o resultado final. O processamento lógico do modelo ocorre por meio da geração de texto intermediário.

Exemplo de código demonstrando a estrutura CoT:
```python
prompt_cot = """
Aja como um Delegado. Analise o caso seguindo este roteiro mental:

PASSO 1: Fatos - Liste o que realmente aconteceu.
PASSO 2: Violência - Houve grave ameaça ou violência física? (Sim/Não)
PASSO 3: Subtração - O bem foi retirado ou entregue voluntariamente?

Com base nisso, defina a tipificação penal.

Formato de Resposta:
RACIOCINIO: [Sua análise detalhada]
VEREDITO: [FURTO, ROUBO ou ESTELIONATO]
"""
```
