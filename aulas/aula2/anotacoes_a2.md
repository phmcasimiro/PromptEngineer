# Aula 2: Raciocínio Estruturado Avançado e Visão Computacional

## Objetivo da Aula
Esta aula avançou as técnicas de Engenharia de Prompt, saindo da classificação textual simples para dois domínios complexos: forçar a IA a redigir laudos jurídicos detalhados usando "Chain of Thought" forçado e introduzir o poder dos Modelos Multimodais (Visão Computacional) para análise de evidências fotográficas.

---

## Conceitos e Ferramentas Apresentadas

### 1. Chain of Thought (CoT) com Estrutura Estrita (`main2_1.py`)
* **O Problema Clássico:** Na Aula 1, o CoT era genérico. Quando lidamos com crimes difíceis de diferenciar (como Furto Mediante Fraude vs. Estelionato), a IA precisa de rigor metodológico.
* **A Evolução Direcional:** O prompt deixa de ser um "pedido" e vira um "algoritmo mental estruturado".
* **Benefício:** A técnica garante explicabilidade ("Explainable AI").

Exemplo de código forçando a estrutura de pensamento:
```python
prompt_sistema = """
Analise o relato como um Delegado de Policia, especialista em direito penal. 
Siga ESTRICTAMENTE estes passos:

PASSO 1 - Analise os Fatos com base nas palavras chave do relato
PASSO 2 - Violência: Analise se houve violência física ou psíquica e/ou grave ameaça
PASSO 3 - Vontade: Analise se a entrega do bem foi espontânea (mesmo que por engano) ou forçada
PASSO 4 - Tipificação: Cruzes os passos 2 e 3 para definir o crime.

Saída:
RACIOCINIO: [Resumo objetivo com base no direito penal brasileiro]
VEREDITO: [nome do crime]
"""
```

### 2. Visão Computacional / Modelos Multimodais (`main2_2.py`)
* **Conceito Multimodal:** LLMs tradicionais são limitados a texto. Modelos Multimodais (M-LLMs) conseguem processar imagens correlacionando-as com base linguística.
* **Tratamento de Dados de Imagem (Base64):** O script usa a biblioteca `base64` do Python para converter a foto em texto.

Exemplo de codificação Base64 no Python:
```python
def encode_image(file_content): # Codifica em Base64
    return base64.b64encode(file_content).decode("utf-8") # Decodifica para UTF-8

# Codificação durante o endpoint POST:
conteudo = await arquivo.read() # Lê o arquivo
img_b64 = encode_image(conteudo) # Codifica em Base64
```

- **Engenharia de Prompt para Visão e "JSON Forcing":** 
  - **O Problema da Verbosidade:** 
    - LLMs (especialmente os treinados em chat) tentam ser "educados" por padrão, respondendo de forma prolixa *"Certamente! Analisando a imagem, posso ver..."*. 
    - Se este tipo de resposta for direcionada para o frontend de um site ou para o banco de dados da polícia, o código (o *parser*) vai quebrar porque sites e aplicativos web não "leem conversa", eles só sabem ler variáveis estritas enviadas por computadores em um padrão fixo (JSON).
  - **A Solução (JSON Forcing):** 
    - Na engenharia de prompt avançada, não basta dizer para a IA que ela é um perito, é necessário que ela se comporte como uma **API previsível**, ou seja, deve-se anular sua personalidade tagarela. 
    - Limitando e forçando formato (`"Responda APENAS um objeto JSON válido..."`), você assegura que o sistema receberá sempre as chaves `[classificacao_cena]`, `[objetos_principais]` e `[detalhes_tecnicos]`, sem lixo textual ao redor.
    - Isso permite automatização sistêmica cruzada (como colocar o Laudo na tela web e enviar a variável "fogo no recinto" para o serviço do corpo de bombeiros simultaneamente).

Exemplo do prompt aplicando JSON Forcing:
```python
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
```

* **Técnicas de Sanitização de Saída (Output Parsing):**
- Geralmente, as respostas dos modelos incluem marcações de código markdown (` ```json `). 
- É necessário limpar essas marcações para que o sistema possa processar a resposta.

Exemplo prático de Parsing:
```python
# Remove marcações de código markdown
resposta_texto = ( 
    response.choices[0] # Pega a primeira resposta
    .message.content.replace("```json", "") # Remove marcações JSON de código markdown
    .replace("```", "") # Remove marcações de texto de código markdown
    .strip() # Remove espaços em branco
)
```

### 3. Integração Total: Texto e Imagem (`main2_3.py`)
- A integração utiliza um fluxo em dois modelos diferentes: 
- Inicialmente, um modelo de visão (`moondream`) descreve a imagem;
- Depois, um modelo de linguagem (`llama3.2`) cruza essa descrição com o depoimento para validar consistência.

Exemplo de prompt cruzando análises:
```python
prompt_analise = f"""
Você é um perito criminal. Verifique a coerência das provas.

RELATO DA VÍTIMA: "{relato}"
O QUE A PERÍCIA (IA) VIU NA FOTO: "{descricao_visual}"

TAREFA:
Compare o relato com a foto. Existe contradição?
VEREDITO: [CONSISTENTE / INCONSISTENTE]
JUSTIFICATIVA: [Explique por quê]
"""
```
