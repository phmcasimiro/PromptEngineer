# RAG - RETRIEVAL AUGMENTED GENERATION

- Geração Aumentada por Recuperação

## Visão Geral sobre RAG (Geração Aumentada por Recuperação)
----
### Fundamentos e Arquitetura

* **Problemas que o RAG resolve:** Ele aprimora os LLMs (modelos de linguagem) ao fornecer uma busca de conhecimento explícita. Isso permite respostas mais precisas e confiáveis usando documentos reais em vez de depender apenas da memória do modelo.
* **Pipeline básico de ponta a ponta:** Envolve a construção de uma base de conhecimento e o processamento das consultas dos usuários para recuperar informações e gerar respostas com citações.
* **Retriever (Recuperador) vs. Generator (Gerador):** * O **recuperador** busca o contexto para as respostas.
* O **gerador** sintetiza as respostas.
* Eles são acoplados pelo *prompt*, que molda o que o gerador visualiza.


* **Redução de alucinações:** O RAG fornece evidências para os modelos citarem, ancorando as respostas nos textos recuperados. Isso muda o foco de "adivinhação" para a citação de informações presentes.

---

### Dados, Embedding e Indexação

* **Fontes de dados comuns:** Documentos internos, dados operacionais, conteúdo de engenharia e dados web estruturados.
* **Embeddings de Vetores:** São representações numéricas de texto que permitem que a similaridade semântica seja capturada geometricamente, essencial para a busca densa.
* **Banco de Dados Vetorial:** Armazena os *embeddings* e permite buscas rápidas por similaridade, o que é crítico conforme o volume de dados cresce.
* **Chunking (Fragmentação):** Envolve a divisão de documentos em passagens menores para melhor indexação e recuperação, otimizando o tamanho para manter a relevância contextual.
* **Tamanho de Chunk Ideal:** Depende da estrutura dos dados. Chunks médios servem para documentos complexos, enquanto chunks menores são ideais para FAQs.

---

### Otimização e Comparação deMétodos de Recuperação e Busca

* **Recuperação vs. Busca:** A recuperação engloba métodos mais amplos que a correspondência por palavras-chave, incluindo busca vetorial semântica e filtros de metadados.
* **Tipos de Métodos:**
* **Esparso:** Foca em correspondências exatas de palavras (ex: BM25).
* **Denso:** Enfatiza a similaridade semântica.
* **Híbrido:** Combina ambos para estratégias mais abrangentes.


* **Uso do BM25:** É superior à recuperação densa em cenários que exigem correspondência precisa de termos, como números de peças ou cláusulas jurídicas.
* **Re-ranking (Reclassificação):** Refina a precisão ao reordenar os candidatos após a recuperação inicial, garantindo que a informação mais pertinente seja priorizada.

---

### Estratégia e Avaliação

* **Design de Prompt:** Continua crítico pois dita como o texto recuperado é utilizado, garantindo clareza, estrutura e adesão ao contexto.
* **RAG vs. Retreinamento:** O RAG é preferido por permitir atualizações rápidas e econômicas através da atualização de documentos, evitando o processo intensivo de retreinar o modelo.
* **Casos de Uso Reais:** Motores de busca com IA, ferramentas de suporte ao cliente e sistemas de redação de relatórios.
* **Métricas de Recuperação:** São usados indicadores como **Recall@k**, **Precision@k** e **MRR** para medir a qualidade da relevância.
* **Avaliação da Resposta Final:** Envolve verificar a correção, completude, fidelidade, qualidade das citações e utilidade em relação a benchmarks e expectativas do usuário.

---

# QUESTIONÁRIO RAG

## Conceitos Fundamentais e Pipeline

- 1. Que problema o RAG resolve que os LLMs isolados não conseguem?

- O RAG aprimora os LLMs ao fornecer uma busca de conhecimento explícita, permitindo respostas mais precisas e confiáveis usando documentos reais em vez de apenas a memória do modelo.

- 2. Explique um pipeline básico de RAG de ponta a ponta.

- Um pipeline tradicional de RAG inclui a construção de uma base de conhecimento e o processamento de consultas de usuários para recuperar e gerar respostas com citações.

- 3. Quais papéis o recuperador (retriever) e o gerador (generator) desempenham, e como eles são acoplados?

- O recuperador busca o contexto para as respostas, enquanto o gerador sintetiza as respostas, garantindo que o prompt molde o que o gerador visualiza.

- 4. Como o RAG reduz alucinações em comparação com a geração pura?

- O RAG fornece evidências para os modelos citarem, ancorando as respostas aos textos recuperados, o que muda o foco de "adivinhação" para a citação de informações presentes.

## Dados, Embeddings e Armazenamento

- 5. Que tipos de fontes de dados são comumente usados em sistemas RAG?

- Sistemas RAG utilizam várias fontes de dados, incluindo documentos internos, dados operacionais, conteúdo de engenharia e dados web estruturados para aumentar a precisão da resposta.

- 6. O que é um embedding vetorial e por que ele é essencial para a recuperação densa?

- Embeddings representam o texto numericamente, permitindo que a similaridade semântica seja capturada geometricamente, melhorando assim a eficiência da recuperação em cenários de busca densa.

- 7. O que é chunking (fragmentação) e por que o tamanho do chunk importa?

- O chunking envolve dividir documentos em passagens menores para melhor indexação e recuperação, otimizando o tamanho para manter a relevância contextual e evitar a supersaturação.

- 8. Qual é a diferença entre recuperação (retrieval) e busca (search) em contextos de RAG?

- A recuperação abrange métodos mais amplos do que a correspondência de palavras-chave, incluindo busca vetorial semântica e filtros de metadados, determinando assim quais informações são confiáveis para o modelo.

- 9. O que é um banco de dados vetorial e que problema ele resolve?

- Bancos de dados vetoriais armazenam embeddings, permitindo buscas rápidas por similaridade, o que é crítico à medida que os dados escalam, garantindo uma recuperação eficiente sem perder as capacidades de indexação.

## Otimização e Comparação de Métodos

- 10. Por que o design de prompt ainda é crítico mesmo quando a recuperação está envolvida?

- Um design de prompt eficaz dita como o texto recuperado é utilizado, garantindo clareza, estrutura e adesão ao contexto, prevenindo interpretações errôneas e melhorando a qualidade da saída.

- 11. Quais são os casos de uso comuns do RAG no mundo real hoje?

- O RAG alimenta diversas aplicações, incluindo mecanismos de busca de IA, ferramentas de suporte ao cliente e sistemas de elaboração de relatórios, demonstrando sua versatilidade na resolução de problemas reais.

- 12. Em termos simples, por que o RAG é preferido em vez do retreinamento frequente do modelo?

- O RAG permite atualizações rápidas e econômicas ao atualizar o conhecimento por meio de atualizações de documentos, em vez do processo de retreinamento de modelo, que é complexo e consome muitos recursos.

- 13. Compare os métodos de recuperação esparsa, densa e híbrida.

- Métodos esparsos focam em correspondências exatas de palavras; a recuperação densa enfatiza a similaridade semântica; enquanto abordagens híbridas combinam ambos para estratégias de recuperação de informação abrangentes.

- 14. Quando o BM25 superaria a recuperação densa em um sistema RAG?

- O BM25 se destaca em cenários que exigem correspondências precisas de tokens, como números de peças ou cláusulas legais, onde a interpretação semântica pode levar a imprecisões na recuperação.

- 15. Como você decide o tamanho e a sobreposição (overlap) ideais do chunk para um determinado corpus?

- Os tamanhos ideais de chunk dependem da estrutura dos dados, com chunks médios para documentos complexos e menores para FAQs, enquanto os ajustes são feitos com base no desempenho da recuperação.

## Métricas e Avaliação

- 16. Quais métricas de recuperação você usaria para medir a qualidade da relevância?

- Métricas como Recall@k, Precision@k e MRR ajudam a avaliar a eficácia da recuperação, garantindo que informações relevantes sejam capturadas e apresentadas com precisão ao modelo.

- 17. Como você avalia a qualidade da resposta final de um sistema RAG?

- A avaliação da qualidade da resposta envolve verificar a correção, completude, fidelidade, qualidade da citação e utilidade em relação a benchmarks estabelecidos e expectativas do usuário.

- 18. O que é re-ranking (reclassificação) e onde ele se encaixa no pipeline do RAG?

- O re-ranking aumenta a precisão da recuperação ao reordenar as passagens candidatas com base na relevância após a recuperação inicial, garantindo que a informação mais pertinente seja priorizada.

Aqui está o conteúdo das imagens extraído, organizado por tópicos e traduzido para português brasileiro:

