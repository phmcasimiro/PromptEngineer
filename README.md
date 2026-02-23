# 🏛️ IntelliDoc — O Escrivão Virtual de Crimes Patrimoniais

**Disciplina:** Prompt Engineering Avançado — Prof. Dr. Wandré Nunes de Pinho Veloso
**Aluno:** Pedro Casimiro

---

## 📖 O que é este projeto?

O **IntelliDoc** é uma **API web com Inteligência Artificial** especializada em auxiliar delegacias na classificação e análise de **crimes contra o patrimônio** (Furto, Roubo, Estelionato, entre outros).

A IA atua como um **"Escrivão Virtual"** da PCDF: você envia um relato de crime como texto (ou uma imagem de evidência), e ela retorna uma análise técnica com a tipificação penal correta, fundamentada no Código Penal Brasileiro.

> **O que é uma API?** É um programa que roda como um servidor e responde a chamadas externas. Neste caso, você manda um relato e recebe de volta uma análise em formato JSON.

---

## 🗂️ Estrutura do Projeto

```
4_PromptEng/
│
├── app/                        ← 📌 APLICAÇÃO PRINCIPAL
│   ├── main.py                 ← Ponto de entrada: inicializa o servidor
│   ├── config.py               ← Configurações (modelos, URLs, banco)
│   ├── routers/
│   │   ├── zero_shot.py        ← Endpoint 1: classificação rápida
│   │   ├── few_shot.py         ← Endpoint 2: classificação com exemplos
│   │   ├── chain_of_thought.py ← Endpoint 3: análise passo a passo
│   │   ├── rag.py              ← Endpoint 4: pesquisa no Código Penal
│   │   └── visao.py            ← Endpoint 5: análise de imagens
│   ├── static/
│   │   └── index.html          ← 🖥️ INTERFACE WEB (Frontend)
│   └── scripts/
│       └── index_cp.py         ← Script para criar o banco de artigos de lei
│
├── aulas/                      ← 📚 Exercícios das aulas (Aula 1 a 4)
│   ├── aula1/                  ← FastAPI básico, Zero-Shot, Few-Shot, CoT
│   ├── aula2/                  ← Visão Computacional
│   ├── aula3/                  ← RAG e Sumarização
│   └── aula4/                  ← Benchmark de performance
│
├── banco_vetorial/             ← 🗃️ Banco de dados ChromaDB (artigos do CP)
├── docs/                       ← 📄 Documentos de referência
│   ├── CrimesPatrimonio_CP.md  ← Código Penal formatado para IA
│   ├── CrimesPatrimonio_Simulado.md ← Questões de concurso para teste
│   ├── ollama.md               ← Guia do Ollama
│   └── PromptEng.md            ← Material teórico de Prompt Engineering
│
├── img/                        ← 🖼️ Imagens para testar o endpoint de visão
├── requirements.txt            ← 📦 Lista de pacotes Python necessários
└── README.md                   ← Este arquivo!
```

---

## 🖥️ Interface Web (Frontend)

O projeto inclui uma interface gráfica completa, acessível pelo navegador, sem precisar instalar nenhum programa extra. Com o servidor rodando, acesse:

> **[http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)**

### O que você encontrará na interface:

| Módulo | O que faz | Como usar |
| :--- | :--- | :--- |
| ⚡ **Zero-Shot** | Classificação rápida | Digite o relato e clique em Analisar |
| 📋 **Few-Shot** | Tipificação com exemplos | Digite o relato e veja a tipificação fundamentada |
| 🧠 **Raciocínio (CoT)** | Análise jurídica passo a passo | Para casos complexos ou ambíguos |
| 📚 **Código Penal (RAG)** | Consulta ao CP com citação de artigos | Digite uma pergunta ou descreva o caso |
| 📷 **Visão** | Análise de fotos de evidências | Faça upload de uma imagem JPG ou PNG |

> **Dica:** Use `Ctrl + Enter` para enviar o texto rapidamente em qualquer campo.


---

## 🛠️ Pré-requisitos

Antes de começar, você precisa ter instalado:

1. **Python 3.10+** — a linguagem de programação usada.
2. **Ollama** — motor local para rodar modelos de IA gratuitamente.
3. **Git** — para clonar o projeto.

---

## 🚀 Instalação e Configuração (Passo a Passo)

### Passo 1 — Instale o Ollama

O Ollama roda os modelos de linguagem localmente no seu computador. Acesse [ollama.ai](https://ollama.ai) e siga as instruções de instalação para Linux/macOS.

Após instalar, baixe os modelos necessários:

```bash
# Modelo de texto (análise e classificação de crimes)
ollama pull qwen2.5:3b

# Modelo de visão (análise de imagens de evidências)
ollama pull qwen3-vl:8b

# Modelo de embeddings (busca semântica no Código Penal)
ollama pull nomic-embed-text
```

> ⏳ **Atenção:** O download pode demorar alguns minutos dependendo da sua conexão.

### Passo 2 — Instale as dependências Python

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

### Passo 3 — Crie o banco de artigos do Código Penal (RAG)

Este passo converte o arquivo `docs/CrimesPatrimonio_CP.md` em vetores matemáticos
armazenados no ChromaDB. Isso permite que a IA pesquise os artigos da lei por
significado semântico.

```bash
python3 app/scripts/index_cp.py
```

Você deverá ver:
```
Abrindo docs/CrimesPatrimonio_CP.md...
Total de 29 blocos identificados para indexação.
Sucesso! 29 documentos indexados na coleção 'crimes_patrimonio'.
```

> **Só precisa rodar uma vez!** O banco fica salvo na pasta `banco_vetorial/`.

### Passo 4 — Inicie o servidor

```bash
uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

A flag `--reload` faz o servidor reiniciar automaticamente quando você edita o código.

---

## 🔍 Como usar a API

Acesse a **documentação interativa** em: [http://localhost:8000/docs](http://localhost:8000/docs)

Lá você pode testar cada endpoint direto pelo navegador, sem precisar de outros programas.

---

## 🧠 Os 5 Endpoints Explicados

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
  "gravidade": "MÉDIA",
  "resumo_curto": "Subtração de bem móvel com escalada de obstáculo."
}
```

---

### 2. Few-Shot: classificação com exemplos

**Rota:** `POST /few_shot/analisar`
**Arquivo:** `app/routers/few_shot.py`

A IA recebe o relato junto com **3 exemplos de crimes já resolvidos** dentro do prompt. Isso aumenta a precisão para crimes comuns (Furto, Roubo, Estelionato).

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

---

### 3. Chain-of-Thought (CoT): análise passo a passo

**Rota:** `POST /cot/analisar_cot`
**Arquivo:** `app/routers/chain_of_thought.py`

Para casos **complexos ou ambíguos** (ex: furto mediante fraude vs estelionato), a IA é forçada a raciocinar em etapas antes de dar um veredito. É como um Delegado que pensa em voz alta.

O prompt instrui a IA a responder 4 perguntas antes de concluir:
1. **Fatos** — O que aconteceu objetivamente?
2. **Violência/Ameaça** — Houve força física ou ameaça?
3. **Inversão da Posse** — Como o bem saiu da vítima?
4. **Qualificadoras** — Há agravantes?

**Exemplo de resposta:**
```json
{
  "analise_detalhada": {
    "fatos": "Motorista de app recebeu encomendas mas não as entregou.",
    "violencia": "Não houve violência ou ameaça.",
    "posse": "O bem foi entregue voluntariamente ao agente (detentor).",
    "qualificadoras": "Abuso de confiança na relação de trabalho."
  },
  "veredito": {
    "crime": "APROPRIAÇÃO INDÉBITA",
    "artigo": "Art. 168, caput",
    "fundamentacao_juridica": "O agente tinha posse lícita do bem e inverteu..."
  }
}
```

---

### 4. RAG: pesquisa no Código Penal

**Rota:** `POST /rag/tipificar_caso`
**Arquivo:** `app/routers/rag.py`

RAG significa **Retrieval-Augmented Generation** — Geração Aumentada por Recuperação.

**Como funciona em 3 etapas:**

```
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
  "analise_baseada_no_cp": "Com base no Art. 155, § 4º, II, configura-se furto qualificado pois...",
  "fontes_consultadas": [
    {"source": "Código Penal", "title": "Art. 155 — Furto"},
    {"source": "Código Penal", "title": "Art. 157 — Roubo"}
  ]
}
```

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

## ⚙️ Como a IA funciona por baixo dos panos

```
Seu relato (texto)
       │
       ▼
 ┌─────────────┐    HTTP Request    ┌─────────────┐
 │  Seu       │ ─────────────────► │  FastAPI    │
 │  Navegador │                    │  (app/)     │
 └─────────────┘                   └──────┬──────┘
                                          │ Formata o prompt_sistema
                                          │ e chama o Ollama
                                          ▼
                                   ┌─────────────┐
                                   │   Ollama    │  ← roda localmente
                                   │ qwen2.5:3b  │     no seu PC
                                   └──────┬──────┘
                                          │ Resposta em JSON
                                          ▼
                                   ┌─────────────┐
                                   │  FastAPI    │  ← devolve para
                                   │  retorna    │     você
                                   └─────────────┘
```

O **Prompt de Sistema** (`prompt_sistema`) é o "manual de instruções" que diz para a IA
qual persona assumir ("Você é um Escrivão da PCDF...") e como formatar a resposta (JSON).

---

## 📦 Pacotes Python usados (requirements.txt)

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

---

## 📚 Material de Apoio (pasta `docs/`)

| Arquivo | Conteúdo |
| :--- | :--- |
| `ollama.md` | Guia completo do Ollama com cheat sheet de comandos |
| `PromptEng.md` | Teoria de todas as técnicas de Prompt Engineering |
| `RAG.md` | Explicação detalhada de como funciona o RAG |
| `CrimesPatrimonio_CP.md` | Código Penal (Arts. 155–183) formatado para IA |
| `CrimesPatrimonio_Simulado.md` | Questões de concurso para validar os endpoints |

---

## 📝 Requisitos do Trabalho Final

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
