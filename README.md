# OLLAMA

## DOWNLOAD OLLAMA

`curl -fsSL https://ollama.com/install.sh | sh`

## COMANDOS OLLAMA

`ollama list` Lista os modelos que já estão baixados

`ollama pull [nome]` Baixa um modelo sem iniciar o chat.

`ollama rm [nome]` Remove um modelo para liberar espaço em disco.

`ollama ps` Mostra quais modelos estão rodando na memória no momento.

## RUN OLLAMA

- Primeiro Modelo a ser utilizado Llama 3.2 (leve)

`ollama run llama3.2`

## ACESSANDO A API

- Caso precise conectar o Ollama com o Python ou LangChain, utilize o comando abaixo para verificar se a API está rodando:

`curl http://localhost:11434/api/tags`

## TÉCNICA ZERO SHOT

No Zero-Shot é fornecida a instrução e a tarefa sem dar nenhum exemplo prévio de "notícia vs. classificação". Confia-se totalmente no conhecimento prévio que o modelo (Qwen 2.5) já possui sobre o que é um crime.

```json
SYSTEM_PROMPT=
"""
Você é um assistente especializado em segurança pública brasileira.
Sua tarefa é ler uma notícia e classificar o crime em uma destas categorias: 
[HOMICIDIO, ROUBO, FURTO, TRAFICO, ESTELIONATO, OUTROS].

Regras:
1. Responda APENAS com um objeto JSON.
2. O JSON deve ter duas chaves: "categoria" e "justificativa".
```

## TÉCNICA FEW SHOT

No Few-Shot "ensinamos" o modelo fornecendo alguns exemplos de entrada e saída esperada dentro do prompt. Essa técnica é utilizada para casos onde o modelo precisa entender a diferença técnica entre crimes (ex: Roubo envolve violência, Furto não).

```json
SYSTEM_PROMPT = """
Você é um assistente especializado em segurança pública brasileira.
Sua tarefa é ler uma notícia e classificar o crime conforme os exemplos abaixo:

Exemplo 1:
Notícia: "Indivíduo levou a carteira da vítima que estava distraída no metrô, sem que ela percebesse."
Resposta: {"categoria": "FURTO", "justificativa": "Subtração de bens sem uso de violência ou ameaça."}

Exemplo 2:
Notícia: "Dois homens armados renderam o motorista e levaram o carro sob graves ameaças."
Resposta: {"categoria": "ROUBO", "justificativa": "Subtração de bem mediante uso de arma e ameaça direta."}

Agora, classifique a notícia fornecida seguindo este padrão de JSON.
Categorias permitidas: [HOMICIDIO, ROUBO, FURTO, TRAFICO, ESTELIONATO, OUTROS].

## TÉCNICA CHAIN OF THOUGHTS (CoT)

- Técnica de Engenharia de Prompt que força o modelo a decompor problemas complexos em etapas intermediárias.
- Ao gerar texto explicando o raciocínio, o modelo cria seu próprio contexto para a resposta final, reduzindo alucinações.

```json
SYSTEM_PROMPT = """
Você é um assistente especializado em segurança pública brasileira.
Sua tarefa é ler uma notícia e classificar o crime.

Siga estes passos de raciocínio:
1. Identifique os fatos principais da notícia.
2. Verifique se houve violência ou ameaça grave.
3. Determine se o bem foi subtraído ou entregue voluntariamente.
4. Classifique o crime.

Formato de Resposta:
{
  "raciocinio": "[Explicação passo a passo]",
  "classificacao": "[Categoria]"
}
"""
```

## TÉCNICA CHAIN OF THOUGHTS (CoT)

- Técnica de Engenharia de Prompt que força o modelo a decompor problemas complexos em etapas intermediárias.
- Ao gerar texto explicando o raciocínio, o modelo cria seu próprio contexto para a resposta final, reduzindo alucinações.

```json
SYSTEM_PROMPT = """
Você é um assistente especializado em segurança pública brasileira.
Sua tarefa é ler uma notícia e classificar o crime.

Siga estes passos de raciocínio:
1. Identifique os fatos principais da notícia.
2. Verifique se houve violência ou ameaça grave.
3. Determine se o bem foi subtraído ou entregue voluntariamente.
4. Classifique o crime.

Formato de Resposta:
{
  "raciocinio": "[Explicação passo a passo]",
  "classificacao": "[Categoria]"
}
"""
```

# VISÃO COMPUTACIONAL

## TÉCNICA MULTIMODAL

Modelos multimodais são sistemas de IA capazes de processar e integrar múltiplas modalidades de dados (texto, imagem, áudio, vídeo) para gerar respostas contextualizadas. Em Prompt Engineering, isso permite que você envie uma imagem junto com uma pergunta em texto e receba uma resposta que considera ambas as informações.

**Exemplos de aplicação:**

- Análise de documentos (extrair texto de faturas, receitas médicas)
- Descrição automática de imagens para acessibilidade
- Detecção de objetos e análise de cenas
- Interpretação de gráficos e diagramas

### VISION TRANSFORMER (ViT)

O **Vision Transformer** (Dosovitskiy et al., 2020) revolucionou a visão computacional ao adaptar a arquitetura Transformer - originalmente criada para processamento de linguagem natural - para processar imagens diretamente, sem depender de redes convolucionais (CNNs).

#### **Arquitetura e Funcionamento**

1. **Divisão em Patches (não pixels individuais)**
   - A imagem é dividida em **patches** (blocos quadrados), tipicamente de 16×16 pixels
   - Exemplo: Uma imagem 224×224 pixels → 196 patches de 16×16 pixels cada
   - Cada patch é "achatado" em um vetor unidimensional de valores numéricos (RGB)

2. **Linear Projection (Projeção Linear)**
   - Cada vetor de patch passa por uma camada linear que o projeta em um **embedding de dimensão fixa** (ex: 768 dimensões)
   - Similar ao embedding de palavras em modelos de linguagem (Word2Vec, BERT)

3. **Positional Embeddings (Codificação Posicional)**
   - Como o Transformer não tem noção de ordem, são adicionados **positional embeddings** aos patches
   - Isso permite que o modelo "saiba" onde cada patch está localizado na imagem original
   - Exemplo: O patch do canto superior esquerdo recebe um embedding diferente do patch central

4. **Self-Attention Mechanism (Mecanismo de Auto-Atenção)**
   - Os patches processados passam por camadas de **self-attention**
   - O modelo aprende a relacionar diferentes regiões da imagem
   - Exemplo: Ao ver uma pessoa segurando um guarda-chuva, o modelo relaciona "mão" + "objeto cilíndrico" + "tecido" para identificar "guarda-chuva"

5. **CLS Token (Token de Classificação)**
   - Um token especial **[CLS]** é adicionado ao início da sequência de patches
   - Após processar todas as camadas Transformer, o estado final do [CLS] contém a representação global da imagem
   - Esse vetor é usado para tarefas de classificação ou conectado a uma LLM

#### **Integração com LLMs (Modelos Multimodais)**

Em modelos multimodais modernos (como GPT-4 Vision, LLaVA, CLIP):

1. **Visual Encoder (ViT)** → Processa a imagem e gera embeddings visuais
2. **Projection Layer** → Traduz os embeddings visuais para o espaço semântico da LLM
3. **LLM** → Recebe os embeddings visuais concatenados com o texto do prompt
4. **Geração de Resposta** → A LLM "lê" a imagem como se fosse texto e gera uma resposta contextualizada

**Analogia didática:**  
Imagine que você está descrevendo uma foto para alguém ao telefone. Você não descreve cada pixel, mas sim "blocos de informação" (patches): "no canto esquerdo há uma árvore, no centro uma pessoa, à direita um carro". O Vision Transformer faz exatamente isso: divide a imagem em blocos significativos e usa atenção para entender como esses blocos se relacionam.

#### **Exemplo Prático com Ollama**

```bash
# Modelo multimodal LLaVA (usa ViT internamente)
ollama pull llava

# Prompt multimodal
ollama run llava
>>> Analise esta imagem e descreva o que você vê: /path/to/imagem.jpg
>>> [A IA processará a imagem via ViT e gerará uma descrição textual]
```

#### **Diferença entre ViT e CNNs tradicionais**

| Aspecto             | CNN (ex: ResNet)                         | Vision Transformer (ViT)                             |
|---------------------|------------------------------------------|------------------------------------------------------|
| Processamento       | Local → Global (camadas convolucionais) | Global desde o início (self-attention)               |
| Inductive Bias      | Forte (assume localidade espacial)      | Fraco (aprende da relação entre patches)             |
| Dados necessários   | Funciona bem com poucos dados           | Requer grandes datasets (ImageNet-21k)               |
| Relações long-range | Difícil (requer muitas camadas)         | Natural (self-attention captura diretamente)         |

#### **Referências**

- Dosovitskiy, A., et al. (2020). *"An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"*. ICLR 2021.
- Vaswani, A., et al. (2017). *"Attention is All You Need"*. NeurIPS 2017.
- Radford, A., et al. (2021). *"Learning Transferable Visual Models From Natural Language Supervision"* (CLIP). ICML 2021.
