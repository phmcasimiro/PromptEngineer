# Aula 4 — Performance, Fine-Tuning e Engenharia de Produção

## Sumário

1. [Por que medir performance?](#1-por-que-medir-performance)
2. [Benchmark de Modelos de IA](#2-benchmark-de-modelos-de-ia)
   - 2.1 Métricas: tempo de resposta e uso de RAM
   - 2.2 Estimativa de tokens por segundo
   - 2.3 Temperatura e reprodutibilidade
3. [Fine-Tuning e LoRA](#3-fine-tuning-e-lora)
   - 3.1 O que é Fine-Tuning?
   - 3.2 LoRA: ajuste com baixo custo computacional
   - 3.3 Simulando o efeito do Fine-Tuning via Prompt
4. [API de Produção com FastAPI](#4-api-de-produção-com-fastapi)
   - 4.1 Estrutura modular de uma API real
   - 4.2 Zero-Shot vs Few-Shot em produção
   - 4.3 Tratamento de erros com `HTTPException`
   - 4.4 Forçando saída em JSON com `format='json'`
5. [Comparativo Final: Zero-Shot vs Few-Shot](#5-comparativo-final-zero-shot-vs-few-shot)

---

## 1. Por que medir performance?

Escolher um modelo de IA não é só sobre qualidade da resposta — é sobre **velocidade** e **custo de infraestrutura**.

Um modelo que demora 15 segundos para responder é inviável em um sistema policial
que atende ocorrências em tempo real. Da mesma forma, um modelo que consome 16 GB de
RAM não cabe em servidores comuns.

**As três perguntas que toda avaliação de performance deve responder:**

| Pergunta | Métrica |
| :--- | :--- |
| Quão rápido o modelo responde? | Tempo médio de resposta (segundos) |
| Quantas informações ele processa por segundo? | Tokens por segundo |
| Quanto impacto tem na memória do servidor? | Uso de RAM (MB) |

---

## 2. Benchmark de Modelos de IA

### 2.1 Métricas: tempo de resposta e uso de RAM

O script `main4_1.py` implementa um benchmark completo. Ele roda o mesmo prompt
múltiplas vezes (padrão: 3 execuções) para calcular uma média confiável, evitando
distorções de uma execução isolada.

```python
# main4_1.py — medindo o uso real de RAM do processo Python
import psutil
import os

def medir_recursos():
    """Retorna o uso de RAM em MB"""
    process = psutil.Process(os.getpid())  # pega o processo atual
    return process.memory_info().rss / 1024 / 1024  # rss: uso real de RAM
```

> **`psutil`** é a biblioteca padrão para monitorar recursos do sistema (CPU,
> RAM, disco) em Python. O método `rss` (Resident Set Size) retorna a memória
> física efetivamente usada pelo processo.

> **Por que medir APENAS o Python?** O Ollama roda como um processo separado.
> O Python só chama a API do Ollama — então o impacto na RAM do Python é
> pequeno; o consumo real está no processo do servidor Ollama.

### 2.2 Estimativa de tokens por segundo

```python
# main4_1.py — calculando velocidade aproximada
resposta = response.choices[0].message.content
num_tokens = len(resposta.split()) * 1.3  # palavras * 1.3 ≈ tokens

tempos.append(duration)
tokens_totais += num_tokens

# Após todas as execuções:
media_tokens_seg = tokens_totais / sum(tempos)
print(f"Velocidade: {media_tokens_seg:.2f} tokens/segundo")
```

> **Por que multiplicar por 1,3?** Tokens não são palavras. Uma palavra como
> "classificação" pode virar 2 tokens: "classifica" + "ção". A estimativa
> `palavras * 1.3` é uma aproximação prática — a contagem exata exigiria o
> tokenizador específico de cada modelo.

### 2.3 Temperatura e reprodutibilidade

```python
# main4_1.py — temperatura 0.0 para benchmark
response = client.chat.completions.create(
    model=MODELO,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0   # ← determinstico: sempre a mesma resposta
)
```

**Por que usar `temperature=0.0` no benchmark?**

| `temperature` | Comportamento | Uso ideal |
| :---: | :--- | :--- |
| `0.0` | Determinístico — sempre escolhe o token mais provável | Benchmarks, análises jurídicas |
| `0.5` | Equilibrado — alguma variação criativa | Assistentes gerais |
| `1.0+` | Alta criatividade — respostas bem variadas | Escrita criativa, brainstorm |

Num benchmark, precisamos que todas as execuções processem a **mesma carga de
trabalho** para que as métricas de tempo sejam comparáveis.

---

## 3. Fine-Tuning e LoRA

### 3.1 O que é Fine-Tuning?

Um modelo de linguagem como o `llama3.2` é treinado com bilhões de textos da
internet — ele sabe um pouco de tudo. O **Fine-Tuning** é um segundo treinamento
especializado, usando dados do **seu domínio específico** (ex: laudos policiais,
textos jurídicos).

```
Modelo Base (genérico)
        ↓
   Fine-Tuning
   (treino com seus dados)
        ↓
Modelo Especializado (fala "polícia fluente")
```

**Custo do Fine-Tuning completo:**
- Requer hardware de nível industrial (GPUs de datacenter)
- Horas a dias de processamento
- Inviável para a maioria das empresas

### 3.2 LoRA: ajuste com baixo custo computacional

**LoRA** (Low-Rank Adaptation) é uma técnica que **não muda os pesos originais** do
modelo — ela insere pequenas "camadas adaptadoras" que aprendem o novo domínio.

```
Modelo Base (pesos congelados, gigabytes)
     +
Adaptador LoRA (pesos treináveis, megabytes)
     =
Modelo Especializado (comportamento = base + domínio)
```

**Vantagens:**
- Treina apenas os adaptadores (muito menos parâmetros)
- O modelo base original é preservado e reutilizável
- Pode-se ter múltiplos adaptadores para domínios diferentes

> **Analogia:** Um médico generalista (modelo base) que faz uma especialização
> em cardiologia (LoRA). Ele não se esquece de tudo que aprendeu antes — apenas
> adiciona conhecimento específico.

### 3.3 Simulando o efeito do Fine-Tuning via Prompt

O script `main4_2.py` mostra na prática a diferença entre um modelo genérico e
um modelo "especializado" (simulado via System Prompt com glossário).

**Texto de entrada (cheio de jargões policiais):**

```python
# main4_2.py
texto_policial = """
A VTR 345 em patrulhamento visualizou um indivíduo em atitude suspeita.
Após abordagem, foi encontrado um simulacro. O QTH foi preservado até a chegada da perícia.
O meliante foi conduzido para a DP para lavratura do APF.
"""
```

**Modelo Genérico (sem especialização):**

```python
# 1. Modelo base: não conhece os termos técnicos
prompt_generico = "Você é um assistente útil. Explique o texto para um leigo."
```

→ O modelo vai tentar explicar "VTR", "QTH" e "APF" como pode, mas provavelmente
errará ou simplificará demais.

**Modelo Especializado (simulando LoRA via contexto):**

```python
# 2. Modelo com glossário injetado no prompt — efeito equivalente ao LoRA
prompt_especializado = """
Você é um Especialista em Terminologia Policial da PCDF (Modelo Fine-Tuned).
Glossário Interno:
- VTR: Viatura
- Simulacro: Arma falsa
- QTH: Local da ocorrência (jargão de radioamador adotado pela polícia)
- APF: Auto de Prisão em Flagrante
- DP: Delegacia de Polícia
Traduza o relato mantendo o tom jurídico.
"""
```

→ Com o glossário, a resposta será precisa e técnica.

> **Limitação deste método:** A injeção de glossário via prompt tem limite de
> contexto (o modelo esquece em conversas longas). O LoRA real "grava" o
> conhecimento permanentemente nos pesos do adaptador.

---

## 4. API de Produção com FastAPI

Os scripts `main_a.py` (Zero-Shot) e `main_b.py` (Few-Shot) mostram como
implementar uma API de classificação de crimes pronta para produção.

### 4.1 Estrutura modular de uma API real

```python
# main_a.py — estrutura base de qualquer endpoint de IA

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama, json

# 1️⃣ Cria o servidor
app = FastAPI(title="Classificador de Crimes")

# 2️⃣ Define o formato de entrada (validação automática)
class Noticia(BaseModel):
    text: str

# 3️⃣ Define o comportamento da IA (o "cérebro")
SYSTEM_PROMPT = """..."""

# 4️⃣ Cria o endpoint
@app.post("/classificar")
async def classificar_noticia(noticia: Noticia):
    ...
```

**Por que separar o `SYSTEM_PROMPT` do código?**

O prompt é o "código da IA" — ele define o comportamento. Deixá-lo como
constante no topo do arquivo facilita:
- Editar sem mexer na lógica do endpoint
- Trocar a instrução sem afetar o resto do código
- Versionar separadamente (ex: `SYSTEM_PROMPT_v2`)

### 4.2 Zero-Shot vs Few-Shot em produção

**Zero-Shot (`main_a.py`)** — instrução direta sem exemplos:

```python
# main_a.py
SYSTEM_PROMPT = """
Você é um assistente especializado em segurança pública brasileira.
Classifique o crime em: [HOMICIDIO, ROUBO, FURTO, TRAFICO, ESTELIONATO, OUTROS].

Regras:
1. Responda APENAS com um objeto JSON.
2. O JSON deve ter: "categoria" e "justificativa".
"""
```

**Few-Shot (`main_b.py`)** — instrução com exemplos concretos:

```python
# main_b.py
SYSTEM_PROMPT = """
Você é um assistente especializado em segurança pública.
Classifique conforme os exemplos:

Exemplo 1:
Notícia: "Indivíduo levou a carteira da vítima distraída no metrô..."
Resposta: {"categoria": "FURTO", "justificativa": "Subtração sem violência."}

Exemplo 2:
Notícia: "Dois homens armados renderam o motorista..."
Resposta: {"categoria": "ROUBO", "justificativa": "Subtração com ameaça."}

Agora classifique a notícia fornecida.
"""
```

> **Regra prática:** Use Zero-Shot para triagem rápida. Use Few-Shot quando a
> classificação precisa ser consistente e a precisão é crítica (ex: laudos policiais).

### 4.3 Tratamento de erros com `HTTPException`

```python
# main_a.py e main_b.py
@app.post("/classificar")
async def classificar_noticia(noticia: Noticia):
    try:
        response = ollama.chat(...)
        resultado_ia = json.loads(response['message']['content'])
        return {"status": "sucesso", "classificacao": resultado_ia}

    except Exception as e:
        # Se qualquer coisa der errado (Ollama offline, JSON inválido...),
        # retorna um erro HTTP padronizado com código 500
        raise HTTPException(status_code=500, detail=f"Erro ao processar IA: {str(e)}")
```

**Por que usar `HTTPException` em vez de `print` ou `return` normal?**

Em uma API web, erros precisam ser comunicados com **códigos HTTP padronizados**:

| Código | Significado | Quando usar |
| :---: | :--- | :--- |
| `200` | Sucesso | Resposta normal |
| `400` | Requisição inválida | Dados de entrada incorretos |
| `500` | Erro interno do servidor | Falha no processamento da IA |

### 4.4 Forçando saída em JSON com `format='json'`

```python
# main_a.py e main_b.py
response = ollama.chat(
    model='qwen2.5:3b',
    messages=[...],
    format='json'  # ← instrui o Ollama a garantir saída JSON válida
)

# Convertendo a string JSON em dicionário Python
resultado_ia = json.loads(response['message']['content'])
```

> **Problema comum sem `format='json'`:** A IA pode retornar o JSON dentro de
> um bloco de código Markdown (` ```json ... ``` `), quebrando o `json.loads()`.
> O parâmetro `format='json'` instrui o modelo a não adicionar esses adornos.

---

## 5. Comparativo Final: Zero-Shot vs Few-Shot

| Critério | Zero-Shot | Few-Shot |
| :--- | :---: | :---: |
| Tamanho do prompt | Menor | Maior |
| Velocidade | ⚡ Mais rápido | 🐢 Mais lento |
| Precisão em casos típicos | Boa | **Excelente** |
| Consistência do formato | Razoável | **Alta** |
| Custo de tokens | Baixo | Médio |
| Melhor para | Triagem, protótipos | Produção, laudos |

**Resumo da aula em uma frase:**

> *Medir performance te diz **qual** modelo usar; o Fine-Tuning/LoRA te diz
> **como** especializá-lo; e a arquitetura de API garante que ele funcione
> **em produção** com confiabilidade.*
