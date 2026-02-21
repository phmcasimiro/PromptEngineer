# RAG - RETRIEVAL AUGMENTED GENERATION

## GERAÇÃO AUMENTADA POR RECUPERAÇÃO (DE CONTEXTO)

**QUANDO USAR O RAG?**
- Usar RAG é uma decisão Estratégica que visa resolver problemas específicos de qualidade de resposta, como alucinações e respostas imprecisas.
- Tanto o RAG quanto o FINE TUNING são estratégias usadas para especializar um LLM em uma área de conhecimento específica para resolver problemas específicos, mas o fazem de maneiras diferentes com consequências de custo, agilidade e manutenção distintas.
- O Cenário de aplicaçao do RAG envolve bases de conhecimentos voláteis, isto é, que são atualizadas com frequência, como documentos, dados operacionais, conteúdo de engenharia e dados web estruturados.
- O RAG é preferido por permitir atualizações rápidas e econômicas através da atualização de documentos, evitando o processo intensivo de retreinar o modelo.
- A aplicação do RAG neste contexto se justifica pela distinção entre a "inteligência do modelo" (a capacidade de ler e interpretar o texto) e o "conhecimento" (os documentos e dados que o modelo tem acesso) que ele pode usar para gerar respostas.
- Ao atualizar o conhecimento, as respostas serão atualizadas pelo modelo, sem a necessidade de retreinar o modelo.
- Com relação ao custo e complexidade, a implementação de um RAG consiste em "conectar" componentes de software, por exemplo, um conjunto de documentos, um modelo de embedding e um banco de vetores. A atualização do conhecimento é uma simples operação de escrita em um banco de dados, algo trivial em termos de custo computacional.
- Já o Fine-Tuning, por mais poderoso que seja para alterar o comportamento de um modelo, é um processo computacionalmente intensivo, isto é, exige a preparação de datasets massivos que serão usados como exemplos, um poder de processamento considerável (geralmente múltiplas GPUs de ponta rodando por horas ou dias) e um conhecimento técnico aprofundado para ajustar os hiperparâmetros e evitar problemas como o "catastrophic forgetting", isto é, a perda de conhecimento adquirido durante o treinamento. Seria como reformar a fundação de um prédio.
- Em resumo, se o seu objetivo é injetar conhecimento factual, específico e volátil, o RAG é a melhor opção. Se o seu objetivo é alterar o comportamento de um modelo, o Fine-Tuning é a melhor opção.

---.

### Fundamentos e Arquitetura

- **Problema que o RAG resolve:** 
  - O RAG aprimora os LLMs (modelos de linguagem) ao fornecer uma base explícita para busca de conhecimento, permitindo respostas mais precisas e confiáveis, baseadas em documentos reais em vez de depender apenas da memória do modelo.

- **Redução de alucinações:** 
  - O RAG fornece evidências para os modelos citarem, ancorando as respostas nos conteúdos recuperados. Isso muda o foco de "adivinhação" para a citação de informações presentes.

- **PIPELINE BÁSICO:** 
  - Um pipeline tradicional de RAG envolve a construção de um CORPUS DE TEXTOS, a indexação, a busca vetorial e o processamento das consultas dos usuários para recuperar informações e gerar respostas com citações.

- **RETRIEVER (Recuperador) vs. GENERATOR (Gerador):** 
    - O **recuperador** busca o contexto para as respostas.
    - O **gerador** sintetiza as respostas.
    - Ambos são acoplados pelo *prompt*, que molda o que o gerador visualiza.

- **CORPUS DE TEXTOS:**
  - É uma coleção organizada de documentos que serve como base de conhecimento para o sistema
  - Por exemplo: Documentos, dados operacionais, conteúdo de engenharia e dados web estruturados.

- **EMBEDDINGS DE VETORES:**
  - São representações numéricas de texto que permitem que a similaridade semântica seja capturada geometricamente, essencial para a busca densa.

- **BANCO DE DADOS VETORIAL:**
  - Armazena os *embeddings* e permite buscas rápidas por similaridade, o que é crítico conforme o volume de dados cresce.

- **CHUNKING (FRAGMENTAÇÃO):**
  - Envolve a divisão de documentos em passagens menores para melhor indexação e recuperação, otimizando o tamanho para manter a relevância contextual.

- **TAMANHO IDEAL DO CHUNK:**
  - Depende da estrutura dos dados. Chunks médios servem para documentos complexos, enquanto chunks menores são ideais para FAQs.

---

### OTIMIZAÇÃO E COMPARAÇÃO DE MÉTODOS DE RECUPERAÇÃO E BUSCA

- **Recuperação (Retrieval) vs. Busca (Search):**
  
  - **Busca Tradicional (Keyword Search):**
    - É o famoso `Ctrl+F`. Busca por correspondência exata de caracteres, isto é, se você digitar "carro", ele encontrará "carro", mas não encontrará "automóvel" ou "veículo".

  - **Recuperação Semântica (Semantic Retrieval) - Aprofundamento:**
    - A IA entende o *significado* e o *contexto* transformando texto em números (vetores).

    #### **1. O que são Embeddings de Vetores?**
    - Imagine que cada palavra ou frase pode ser transformada em uma lista de números (coordenadas GPS do significado).
    - **Rei** pode ser: `[0.9, 0.1, 0.5]`
    - **Rainha** pode ser: `[0.9, 0.8, 0.5]` (Note que os números são quase iguais, mudando apenas a dimensão de gênero).
    - **Maçã** seria: `[0.1, 0.9, 0.1]` (Totalmente diferente).
    - Esses números são gerados por modelos de Embedding (como `nomic-embed-text` ou `text-embedding-3-small`).

    #### **2. O Espaço Vetorial (O Mapa de Conceitos)**
    - O banco de dados vetorial funciona como um mapa 3D gigante.
    - Frases com significados parecidos ficam fisicamente próximas umas das outras nesse mapa.
    - Exemplo de proximidade vetorial:
      - "O cachorro latiu" fica muito perto de "O cão fez barulho".
      - Já "O mercado financeiro caiu" fica muito longe.

    #### **3. Como a Busca Funciona (Similaridade de Cosseno)**
    - Quando o usuário faz uma pergunta, o sistema:
      1. Converte a pergunta em números (Embedding da Pergunta).
      2. Calcula a distância matemática (Cosseno) para todos os documentos no banco.
      3. Retorna os documentos que estão "mais perto" no mapa.

    #### **4. Por que usar Banco de Dados Vetorial (Vector DB)?**
    - Um banco SQL tradicional teria que comparar linha por linha (lento).
    - Um Vector DB (como ChromaDB, Pinecone, pgvector) usa índices matemáticos (HNSW) para achar os vizinhos mais próximos em milissegundos, mesmo com milhões de documentos.
  - **Exemplo Prático de Recuperação:**
    - **Pergunta:** "Como proteger minha casa de invasores?"
    - **Busca Tradicional:** Procura documentos com as palavras "proteger", "casa", "invasores". Pode falhar se o documento falar sobre "sistemas de segurança residencial".
    - **Recuperação Semântica:** Encontra documentos sobre "câmeras de vigilância", "alarmes", "trancas biométricas" e "segurança patrimonial", pois o modelo sabe que esses conceitos estão semanticamente ligados à intenção de "proteger a casa", mesmo que as palavras exatas não estejam lá.

- **TIPOS DE MÉTODOS:**
  - **Esparso:** Foca em correspondências exatas de palavras (ex: BM25).
  - **Denso:** Enfatiza a similaridade semântica.
  - **Híbrido:** Combina ambos para estratégias mais abrangentes.

- **USO DO BM25 (ESPARSO):**
  - É superior à recuperação densa em cenários que exigem correspondência precisa de termos.
  - **Exemplo:** Buscar por códigos específicos como "Erro 0x800f081f" ou nomes próprios exatos "Dr. Pedro Casimiro". A busca densa poderia se confundir e trazer "Falha de sistema" ou "Médico genérico", perdendo a especificidade necessária.

- **USO DA RECUPERAÇÃO DENSA (VETORIAL):**
  - Captura o significado mesmo sem as palavras exatas.
  - **Exemplo:**
    - *Pergunta:* "Meu computador não liga a tela."
    - *Resultado:* O sistema encontra um manual técnico sobre "Falha no monitor" ou "Ausência de sinal de vídeo".
    - *Por que funciona:* O modelo de embedding sabe que "tela não liga" é semanticamente similar a "ausência de vídeo", mesmo que não compartilhem palavras.

- **USO DA RECUPERAÇÃO HÍBRIDA:**
  - Combina o melhor dos dois mundos (BM25 + Vetorial) usando algoritmos de fusão (como RRF - Reciprocal Rank Fusion).
  - **Exemplo Prático (E-commerce):**
    - *Pergunta:* "Iphone 15 Pro Max barato com câmera boa"
    - *BM25:* Garante que o produto seja exatamente o "Iphone 15 Pro Max" (filtro exato).
    - *Vetorial:* Garante que o resultado entenda o conceito de "barato" (preço baixo) e "câmera boa" (qualidade de imagem).
    - *Resultado:* A busca híbrida traz o modelo exato, ordenado pelo melhor custo-benefício, superando qualquer método isolado.

- **RE-RANKING (RECLASSIFICAÇÃO):** 
  - Refina a precisão ao reordenar os candidatos após a recuperação inicial, garantindo que a informação mais pertinente seja priorizada.

---

### Estratégia e Avaliação

* **Design de Prompt:** Continua crítico pois dita como o texto recuperado é utilizado, garantindo clareza, estrutura e adesão ao contexto.
* **RAG vs. Retreinamento:** O RAG é preferido por permitir atualizações rápidas e econômicas através da atualização de documentos, evitando o processo intensivo de retreinar o modelo.
* **Casos de Uso Reais:** Motores de busca com IA, ferramentas de suporte ao cliente e sistemas de redação de relatórios.
* **Métricas de Recuperação:** São usados indicadores como **Recall@k**, **Precision@k** e **MRR** para medir a qualidade da relevância.
* **Avaliação da Resposta Final:** Envolve verificar a correção, completude, fidelidade, qualidade das citações e utilidade em relação a benchmarks e expectativas do usuário.

