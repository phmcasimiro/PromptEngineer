# IntelliDoc — O Escrivão Virtual de Crimes Patrimoniais

**Disciplina:** Prompt Engineering Avançado —

**Professor:** Dr. Wandré Nunes de Pinho Veloso

**Aluno:** Pedro Casimiro

**Descrição do Projeto:** Material de estudo e projeto final da disciplina de Prompt Engineering Avançado.

---

O **IntelliDoc** é uma **API web com Inteligência Artificial** especializada em auxiliar delegacias na classificação e análise de **crimes contra o patrimônio** (Furto, Roubo, Estelionato, entre outros).

A IA atua como um **"Escrivão Virtual"**: O usuário envia um relato de crime como texto (ou uma imagem de evidência), e ela retorna uma análise técnica com a tipificação penal correta, fundamentada no Código Penal Brasileiro.

Neste projeto foram utilizados modelos de linguagem de código aberto, disponíveis no Ollama, como o llama3.2:1b, qwen3-vl:8b e nomic-embed-text. Para construção da API foi utilizado o FastAPI e para o FrontEnd foi utilizado HTML, CSS e JavaScript.

> **OBS:** **API** é uma interface de programa que roda como um servidor e responde a chamadas externas. Neste caso, o usuário manda um relato e recebe de volta uma análise em formato JSON.

---

## Estrutura da Disciplina e do Projeto Final

```text
4_PromptEng/
│
├── app/                             ← APLICAÇÃO PRINCIPAL
│   ├── main.py                      ← Ponto de entrada: inicializa o servidor
│   ├── config.py                    ← Configurações (modelos, URLs, banco)
│   ├── routers/
│   │   ├── zero_shot.py             ← Endpoint 1: classificação rápida
│   │   ├── few_shot.py              ← Endpoint 2: classificação com exemplos
│   │   ├── chain_of_thought.py      ← Endpoint 3: análise passo a passo (Zero-Shot)
│   │   ├── few_shot_cot.py          ← Endpoint 4: análise guiada por gabarito (FS-CoT)
│   │   ├── rag.py                   ← Endpoint 5: pesquisa no Código Penal
│   │   └── visao.py                 ← Endpoint 5: análise de imagens
│   ├── static/
│   │   └── index.html               ← INTERFACE WEB (Frontend)
│   └── scripts/
│       └── index_cp.py              ← Script para criar o banco vetorial de crimes patrimoniais
│
├── aulas/                           ← Exercícios das aulas (Aula 1 a 5)
│   ├── aula1/                       ← FastAPI básico, Zero-Shot, Few-Shot, CoT
│   │   ├── anotacoes_a1.md          ← Anotações teóricas da Aula 1
│   │   ├── main1_1.py               ← Servidor FastAPI básico
│   │   ├── main1_2.py               ← Zero-Shot Prompting
│   │   ├── main1_3.py               ← Few-Shot Prompting
│   │   └── main1_4.py               ← Chain-of-Thought Prompting
│   ├── aula2/                       ← JSON Forcing e Parsers de Saída
│   │   ├── anotacoes_a2.md          ← Anotações teóricas da Aula 2
│   │   ├── main2_1.py               ← JSON Forcing básico
│   │   ├── main2_2.py               ← Parser com regex
│   │   └── main2_3.py               ← Parser com ast.literal_eval
│   ├── aula3/                       ← RAG e Sumarização (Map-Reduce / RLM)
│   │   ├── anotacoes_a3.md          ← Anotações teóricas da Aula 3
│   │   ├── main3_1.py               ← Chunking e indexação no ChromaDB
│   │   ├── main3_2.py               ← Consulta RAG ao banco vetorial
│   │   └── main3_3.py               ← Sumarização Map-Reduce (RLM)
│   ├── aula4/                       ← Benchmark de performance e otimização
│   │   ├── anotacoes_a4.md          ← Anotações teóricas da Aula 4
│   │   ├── main4_1.py               ← Benchmark de tempo e RAM (TPS)
│   │   ├── main4_2.py               ← Simulação de LoRA via prompt
│   │   ├── main_a.py                ← Ollama nativo com format='json'
│   │   └── main_b.py                ← Variação de classificação com ollama
│   └── aula5/                       ← Preparação para Produção
│       ├── anotacoes_a5.md          ← Anotações teóricas da Aula 5
│       ├── main5_1.py               ← API com structlog e Prometheus
│       └── docker.yml               ← Docker Compose para orquestração
│
├── banco_vetorial/                  ← Banco de dados ChromaDB (artigos do CP)
│
├── docs/                            ← Documentos de referência
│   ├── CrimesPatrimonio_CP.md       ← Código Penal (Arts. 155–183) formatado para IA
│   ├── CrimesPatrimonio_Comentarios.md ← Doutrina PCDF hiper-condensada (base do RAG)
│   ├── ollama.md                    ← Guia do Ollama com cheat sheet de comandos
│   ├── PromptEng.md                 ← Material teórico de Prompt Engineering
│   ├── RAG.md                       ← Guia detalhado de RAG
│   ├── proj1.md                     ← Especificação do trabalho da Aula 1
│   └── projeto_final.md             ← Especificação do Projeto Final
│
├── img/                             ← Imagens para testar o endpoint de visão
│   ├── brasao_pcdf.png              ← Brasão da PCDF
│   ├── carrosbatidos1.jpeg          ← Evidência de acidente para teste
│   ├── carrosbatidos2.jpeg          ← Evidência de acidente para teste
│   ├── jogador.jpg                  ← Imagem de pessoa para teste
│   ├── mulher_bolsa.jpeg            ← Imagem de cena para teste
│   └── convert_to_jpeg.py           ← Script utilitário de conversão de imagens
│
├── pdf/                             ← Slides e materiais em PDF da disciplina
│   ├── Aulas1_2_3.pdf               ← Slides das aulas 1, 2 e 3
│   ├── Aulas_1_2_3_4_5.pdf          ← Slides completos da disciplina
│   ├── 2025_RAG.pdf                 ← Artigo acadêmico sobre RAG
│   ├── CrimesPatrimonio_simulado.pdf ← Questões de concurso (base de testes)
│   └── Instrução da Atividade.pdf   ← Enunciado oficial do trabalho final
│
├── inquerito_exemplo.txt            ← Texto de inquérito real para testes de inferência
├── requirements.txt                 ← Lista de pacotes Python necessários
└── README.md                        ← Este arquivo!
```

---

## Requisitos do Trabalho Final

**Objetivo:** Personalizar e demonstrar o funcionamento da API IntelliDoc com pelo menos **3 endpoints funcionais** para um tema de especialização escolhido.

### 1. A Personalidade (System Prompt)

Altere o `prompt_sistema` dos endpoints para criar um especialista no tema
escolhido — com regras de formatação (JSON) e instruções específicas de classificação.

### 2. O Raciocínio (Chain-of-Thought)

Crie um caso complexo/ambíguo relacionado ao seu tema e demonstre como o endpoint
`/cot/analisar_cot` mostra o raciocínio jurídico passo a passo para resolvê-lo.

### 3. A Memória (RAG)

Indexe documentos específicos do seu tema (leis, portarias, jurisprudência) no
ChromaDB e demonstre que a IA recupera e cita essas fontes nas respostas.

### 4. A Visão

Analise imagens relacionadas ao seu tema usando o endpoint `/visao/analisar_evidencia`.

### Entrega

Até **03/03**: Relatório (.pdf ou .md) + Vídeo de demonstração (máx. 5 min).

---

## Pré-requisitos

Antes de começar, você precisa ter instalado:

1. **Python 3.10+** — a linguagem de programação usada.
2. **Ollama** — motor local para rodar modelos de IA gratuitamente.
3. **Git** — para clonar o projeto.

---

## Instalação e Configuração (Passo a Passo)

### Passo 1 — Instale o Ollama

O Ollama roda os modelos de linguagem localmente no seu computador. Acesse [ollama.ai](https://ollama.ai) e siga as instruções de instalação para Linux/macOS.

Após instalar, baixe os modelos necessários:

```bash
# Modelo de texto hiper-leve (análise e classificação de crimes)
ollama pull llama3.2:1b

# Modelo de visão (análise de imagens de evidências)
ollama pull qwen3-vl:8b

# Modelo de embeddings (busca semântica no Código Penal)
ollama pull nomic-embed-text
```

> **Atenção:** O download pode demorar alguns minutos dependendo da sua conexão.

### Passo 2 — Instale as dependências Python

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

### Passo 3 — Crie o banco de doutrina do Código Penal (RAG)

Este passo converte o arquivo hiper-condensado `docs/CrimesPatrimonio_Comentarios.md` em vetores matemáticos armazenados no ChromaDB. Isso permite que a IA pesquise a doutrina jurídica por significado semântico, com alta densidade informacional.

```bash
python3 app/scripts/index_cp.py
```

Você deverá ver:
```text
Abrindo docs/CrimesPatrimonio_Comentarios.md (Doutrina PCDF)...
  12 chunks identificados.

Total: 12 chunks para indexar.
Sucesso! 12 documentos indexados na coleção 'crimes_patrimonio'.
```

> **Só precisa rodar uma vez!** O banco fica salvo na pasta `banco_vetorial/`.

### Passo 4 — Inicie o servidor (Backend FastAPI)

No terminal, estando na raiz do projeto (`4_PromptEng/`), levante o servidor via Uvicorn:

```bash
uvicorn app.main:app --reload
```

O servidor estará rodando silenciosamente na porta 8000: `http://localhost:8000`.
A flag `--reload` faz o servidor reiniciar automaticamente quando você edita qualquer código na pasta `app/`.

### Passo 5 — Acesse a Aplicação (Frontend Visual)

Com o servidor rodando no terminal, abra seu navegador de internet (Chrome, Firefox, Safari) e acesse a página visual do Escrivão Virtual:

> **[http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)**

A interface gráfica de testes permite que você conecte o relato transcrito às rotas da API com apenas um clique, visualizando as formatações JSON traduzidas em cards visuais.

---

## Como usar a API

Acesse a **documentação interativa** em: [http://localhost:8000/docs](http://localhost:8000/docs)

Lá você pode testar cada endpoint direto pelo navegador, sem precisar de outros programas.

---

## Os 6 Endpoints Explicados

### 1. Zero-Shot: classificação rápida

**Rota:** `POST /zero_shot/classificar`
**Arquivo:** `app/routers/zero_shot.py`

A IA recebe um relato e classifica o crime **sem receber nenhum exemplo prévio**. É como perguntar para um especialista que apenas usa seu próprio conhecimento.

**Exemplo de uso:**
```json
POST /zero_shot/classificar
{
  "texto": "Um homem pulou o muro e levou minha bicicleta"
}
```

**Exemplo de resposta:**
```json
{
  "crime_provavel": "FURTO QUALIFICADO",
  "resumo_curto": "Subtração de bem móvel com escalada de obstáculo."
}
```

---

### 2. Few-Shot: classificação com exemplos

**Rota:** `POST /few_shot/analisar`
**Arquivo:** `app/routers/few_shot.py`

A IA recebe o relato junto com **4 categorias macro de crimes** (Furto, Roubo, Extorsão e Estelionato) como exemplos dentro do prompt. Isso ensina o modelo a diferenciar a mecânica de cada tipificação de maneira estruturada.

**Exemplo de corpo da requisição (JSON):**
```json
{
  "texto": "Recebi uma ligação de um falso gerente bancário que pediu meu token e esvaziou minha conta."
}
```

**Exemplo de resposta:**
```json
{
  "tipificacao": "ESTELIONATO ELETRÔNICO",
  "base_legal": "Art. 171, § 2º-A",
  "explicacao": "Obtenção de vantagem ilícita induzindo a vítima a erro via meio eletrônico."
}
```

#### 🚧 Estudo de Caso: Por que agrupamos 15 crimes em apenas 4 exemplos genéricos?

Inicialmente, testamos catalogar todos os 15 tipos penais detalhados diretamente no System Prompt do Few-Shot. No entanto, essa abordagem extensiva gerou um *Hardcoding Contextual* problemático e ensinou três lições críticas:

1. **Latência e Velocidade de Processamento (Degradação Severa)**
O maior impacto imediato é o Tempo até o Primeiro Token (Time to First Token - TTFT). Toda vez que uma nova requisição bate na rota `/few_shot/analisar`, o Ollama não "lembra" do prompt anterior. A GPU (ou CPU) precisa mastigar, calcular embeddings e processar as matrizes de atenção de todos os 15 exemplos do zero antes de sequer começar a ler o "Relato do Usuário".
   * **De:** ~400 tokens (macro categorias) → Resposta em 1 a 2 segundos.
   * **Para:** ~3.000 tokens (15 exemplos detalhados) → Resposta pode saltar para 8 a 15 segundos ou mais.

2. **Efeito "Lost in the Middle" (Diluição de Atenção do LLM)**
Modelos paramétricos muito pequenos (como da classe de 1 Bilhão) têm uma capacidade atencional "frágil". O fenômeno conhecido como *Lost in the Middle* (Perdido no Meio) atesta que:
   * LLMs prestam muita atenção no INÍCIO do prompt (sua persona de Escrivão).
   * LLMs prestam muita atenção no FINAL do prompt (a instrução JSON e o relato do usuário).
   * **O "Meio" é borrado:** Com 15 exemplos, o modelo estatisticamente ignora ou confunde crimes mapeados no "meio da lista". Isso causa "alucinação" e tipificação errada porque a janela de atenção "esquece" os pesos textuais do meio do prompt.

3. **Escalabilidade e Consumo de RAM (Gargalo de Hardware)**
Cada token consumido no prompt de entrada preenche a memória RAM/VRAM de forma quadrática na operação de *Self-Attention*. Em um cenário de produção em que dezenas de viaturas/delegacias usem a API simultaneamente, empurrar 3.000 tokens repetidos a cada requisição esgota a memória da máquina hospedada em questão de segundos (OOM - *Out of Memory*).

> **A Solução Adotada:** Ensinar a "física do crime" com 4 exemplos curtos (com/sem violência, fraude, etc) e delegar o peso do sumário legal profundo para o banco de dados vetorial via **RAG**.

---

### 3. Chain-of-Thought (CoT): análise passo a passo

**Rota:** `POST /cot/analisar_cot`
**Arquivo:** `app/routers/chain_of_thought.py`

Para casos **complexos ou ambíguos** (ex: furto mediante fraude vs estelionato), a IA é forçada a raciocinar em etapas antes de dar um veredito. É como um Delegado que pensa em voz alta.

O prompt instrui a IA a responder 3 perguntas antes de concluir:
1. **Fatos** — O que aconteceu objetivamente?
2. **Violência/Ameaça** — Houve força física ou ameaça?
3. **Inversão da Posse** — Como o bem saiu da vítima?

**Exemplo de resposta:**
```json
{
  "analise_detalhada": {
    "fatos": "Motorista de app recebeu encomendas mas não as entregou.",
    "violencia": "Não houve violência ou ameaça.",
    "posse": "O bem foi entregue voluntariamente ao agente (detentor)."
  },
  "veredito": {
    "crime": "APROPRIAÇÃO INDÉBITA"
  }
}
```

---

### 4. Few-Shot CoT: Análise Guiada por Exemplo Estruturado

**Rota:** `POST /fscot/analisar`
**Arquivo:** `app/routers/few_shot_cot.py`

A técnica **Few-Shot Chain-of-Thought (FS-CoT)** combina a instrução de raciocínio passo a passo com a injeção prévia de um exemplo resolvido no *System Prompt*. Esta abordagem objetiva otimizar a confiabilidade de *Large Language Models (LLMs)* com baixo número de parâmetros (como o modelo de 1B utilizado neste projeto).

A limitação primária da técnica *Zero-Shot CoT* (aplicada no Endpoint 3) em modelos pequenos reside na instabilidade durante a geração: o modelo frequentemente falha em deduzir as etapas lógicas de forma autônoma ou gera saídas JSON malformadas (alucinação sintática).

Para mitigar essa degradação, o FS-CoT injeta um caso referencial resolvido (apresentando os Fatos, a Violência, a Posse e o Veredito) no formato estrito do JSON esperado. O fornecimento deste padrão condiciona o cálculo probabilístico do modelo, forçando-o a replicar a mesma estrutura lógica e formal ao processar o novo texto de entrada (input do usuário), garantindo assim conformidade com a tipificação do Código Penal.

**Como o prompt guia o modelo por baixo dos panos:**

```python
prompt_fscot = """
Aja como um Delegado da PCDF. Analise o caso seguindo este roteiro mental:

PASSO 1: Fatos - Liste objetivamente o que aconteceu.
PASSO 2: Violência/Ameaça - Houve emprego de violência física ou grave ameaça?
PASSO 3: Inversão da Posse - Como o bem saiu da vítima?

EXEMPLO DE RACIOCÍNIO ESPERADO (FEW-SHOT):
Ocorrência: "Um sujeito puxou a bolsa da mulher. Ela resistiu, ele deu um tapa e fugiu."
{
    "analise_detalhada": {
        "fatos": "Homem avistou uma mulher, subtraiu sua bolsa e a agrediu fisicamente...",
        "violencia": "Sim. Houve emprego de violência física (tapa).",
        "posse": "A coisa saiu da vítima por meio de força física."
    },
    ...
```

---

### 5. RAG: pesquisa no Código Penal

**Rota:** `POST /rag/tipificar_caso`
**Arquivo:** `app/routers/rag.py`

RAG significa **Retrieval-Augmented Generation** — Geração Aumentada por Recuperação.

**Como funciona em 3 etapas:**

```text
1. VOCÊ envia um relato de crime
       ↓
2. A IA pesquisa no banco vetorial (ChromaDB) os artigos do CP mais relevantes
       ↓
3. A IA gera a resposta usando APENAS os artigos encontrados como base
```

Isso garante que a resposta seja **fundamentada em lei real**, não em "achismos" do modelo.

**Exemplo de resposta:**
```json
{
  "tipificacao": "{\n  \"crime\": \"Roubo\",\n  \"artigo\": \"Art. 157, §2º, VII, CP\"\n}",
  "fontes_consultadas": [
    {
      "titulo": "Art. 157",
      "fonte": "Doutrina_PCDF",
      "crime": "Roubo"
    }
  ]
}
```

#### 🚧 Histórico de Implementação e Desafios (Estudo de Caso)
Durante o desenvolvimento deste endpoint, enfrentamos e documentamos três categorias de erros comuns em sistemas RAG, que servem como aprendizado:

1. **Tentativa 1: Indexação Grosseira (Timeout e Poluição)**
   * **O que foi feito:** O Código Penal puro (`CrimesPatrimonio_CP.md`) e a Doutrina PCDF original (500 linhas) foram indexados juntos, fatiados por separador `---`. Solicitamos ao ChromaDB o retorno de `n_results=8`.
   * **O Falso Positivo (Ruído):** Relatos coloquiais como *"Bateram e levaram o celular"* geravam embeddings que o ChromaDB aproximava de artigos irrelevantes do CP (ex: Art. 165 - Dano em Coisa de Valor Histórico), jogando o chunk correto de "Roubo" para fora do top 8. 
   * **O Timeout:** Injetar 8 chunks imensos no prompt do modelo `qwen2.5:3b` fez o tempo de inferência subir para absurdos **8 minutos e meio**.

2. **Tentativa 2: Filtro Duplo Ineficiente**
   * **O que foi feito:** Ajustamos o código para buscar 4 chunks restritos à "Doutrina PCDF" e 2 chunks apenas dos Arts. 155-160 do CP puro.
   * **A Falha da Extensão:** Como os textos originais da doutrina eram longos (muita introdução didática e "gordura" textual), o sumário de "Furto" monopolizou os 4 resultados da busca. O chunk específico detalhando Roubo nunca chegava ao LLM. Mantivemos o erro de classificação do modelo retornando `NAO IDENTIFICADO`.

3. **Tentativa 3: A Solução Otimizada (Sucesso Absoluto)**
   * **Otimização Extrema da Base Documental:** O arquivo `CrimesPatrimonio_Comentarios.md` foi reescrito para formato *hyper-condensado* (de 500 para ~130 linhas), agrupando regras afins (ex: "Coisa, Alheia, Móvel" num único parágrafo listado).
   * **Abandono do CP Puro:** Configuramos o `index_cp.py` para ignorar a lei seca, acabando com a competição de falsos-positivos. Só a Doutrina hiper-densa foi indexada (gerando 12 chunks vitais em vez de 66 ruidosos).
   * **Redução Contextual:** O endpoint `rag.py` foi ajustado para `n_results=3`. Com chunks densos e ricos, 3 resultados contêm toda a informação necessária.
   * **Troca Direcionada de Modelo:** Trocamos o modelo de inferência de `qwen2.5:3b` para o mais leve `llama3.2:1b` (`app/config.py`).
   * **Few-Shot Prompting no RAG:** Inserimos um *exemplo real de JSON* nas instruções do prompt do sistema em `rag.py` para forçar o modelo leve de 1B a estabilizar a resposta nas chaves corretas.
   * **Resultado:** O tempo de inferência despencou de **8.5 minutos para 90 segundos**. O modelo de 1B alinhou perfeitamente os relatos coloquiais aos crimes de Roubo e Roubo Majorado sem "alucinar".

---

### 5. Visão Computacional: análise de imagens

**Rota:** `POST /visao/analisar_evidencia`
**Arquivo:** `app/routers/visao.py`

Envia uma **foto** (JPG/PNG) e a IA — usando o modelo multimodal `qwen3-vl:8b` — descreve tecnicamente o que vê: danos em portas, ferramentas de arrombamento, dispositivos fraudulentos em caixas eletrônicos, etc.

**Exemplo de resposta:**
```json
{
  "descricao_da_evidencia": "Porta metálica com marcas de arrombamento na região da fechadura.",
  "danos_identificados": "Rompimento do cilindro da fechadura por instrumento pontiagudo.",
  "objetos_relevantes": ["gazua", "marcas de ferramenta", "fechadura danificada"],
  "classificacao_da_cena": "Arrombamento de residência"
}
```

---

## Como a IA funciona por baixo dos panos

```text
Seu relato (texto)
       │
       ▼
 ┌─────────────┐    HTTP Request    ┌─────────────┐
 │  Seu        │ ─────────────────► │  FastAPI    │
 │  Navegador  │                    │  (app/)     │
 └─────────────┘                   └──────┬──────┘
                                          │ Formata o prompt_sistema
                                          │ e chama o Ollama
                                          ▼
                                   ┌─────────────┐
                                   │   Ollama    │  ← roda localmente
                                   │ llama3.2:1b │     no seu PC
                                   └──────┬──────┘
                                          │ Resposta em JSON
                                          ▼
                                   ┌─────────────┐
                                   │  FastAPI    │  ← devolve para
                                   │  retorna    │     você
                                   └─────────────┘
```

O **Prompt de Sistema** (`prompt_sistema`) é o "manual de instruções" que diz para a IA qual persona assumir ("Você é um Escrivão da PCDF...") e como formatar a resposta (JSON).

---

## Interface Web (Frontend)

O projeto inclui uma interface gráfica completa, acessível pelo navegador, sem precisar instalar nenhum programa extra. Na etapa de Instalação, após ligar o servidor, basta acessar a URL lá indicada.

### O que você encontrará na interface:

| Módulo | O que faz | Como usar |
| :--- | :--- | :--- |
| **Zero-Shot** | Classificação rápida | Digite o relato e clique em Analisar |
| **Few-Shot** | Tipificação com exemplos | Digite o relato e veja a tipificação fundamentada |
| **COT** | Análise jurídica purista | Força o LLM a pensar sem gabaritos prévios |
| **COT (Few-Shot)** | Few-Shot CoT com gabarito | Mais preciso e formatado para modelos pequenos |
| **Código Penal (RAG)** | Consulta com citação de artigos | Descreva o caso para buscar fundamentação |
| **Visão** | Análise de fotos de evidências | Faça upload de uma imagem JPG ou PNG |

> **Dica:** Use `Ctrl + Enter` para enviar o texto rapidamente em qualquer campo.

---

## Pacotes Python usados (requirements.txt)

| Pacote | Para que serve |
| :--- | :--- |
| `fastapi` | Cria o servidor web e as rotas da API |
| `uvicorn` | Motor que executa o servidor FastAPI |
| `ollama` | Comunica com os modelos de IA locais |
| `chromadb` | Banco de dados vetorial para o RAG |
| `python-dotenv` | Carrega variáveis de configuração (.env) |
| `python-multipart` | Permite receber arquivos (imagens) via API |
| `openai` | Client compatível com a API do Ollama |
| `pypdf` | Leitura de arquivos PDF |
| `psutil` | Monitora uso de memória e CPU |
| `structlog` | Gerador avançado de logs estruturados em formato JSON |
| `prometheus-fastapi-instrumentator` | Exportador de métricas de tráfego e latência para o ecossistema Grafana |

---

## Material de Apoio (pasta `docs/`)

| Arquivo | Conteúdo |
| :--- | :--- |
| `ollama.md` | Guia completo do Ollama com cheat sheet de comandos |
| `PromptEng.md` | Teoria de todas as técnicas de Prompt Engineering |
| `RAG.md` | Explicação detalhada de como funciona o RAG |
| `CrimesPatrimonio_CP.md` | Código Penal (Arts. 155–183) formatado para IA |
| `CrimesPatrimonio_Simulado.md` | Questões de concurso para validar os endpoints |
