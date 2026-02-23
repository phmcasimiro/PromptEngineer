# TRABALHO FINAL: Operação IntelliDoc - O Escrivão Especialista

## Descrição

Durante o curso, construímos a estrutura do IntelliDoc, uma API de Inteligência Artificial para a PCDF. Agora, cada aluno deve criar a sua versão especializada desse sistema. Você não será apenas um programador, mas o "Engenheiro de Conhecimento" responsável por adaptar o modelo genérico para uma delegacia ou especialidade específica.

**Objetivo:** Personalizar, rodar e demonstrar o funcionamento da API IntelliDoc, utilizando endpoints de Texto, Raciocínio (CoT), Visão Computacional e Memória (RAG).

## O Desafio (Passo a Passo)

Você deverá entregar uma implementação funcional da API contendo pelo menos 3 endpoints funcionais, adaptados para um **Tema de Especialização** à sua escolha (Ex: Homicídios, Crimes Cibernéticos, Tráfico, Maria da Penha, Crimes Ambientais, etc.).

---

## 1. A Personalidade (System Prompt)

Nos códigos das primeiras aulas, altere o `prompt_sistema` do endpoint de análise textual.

- **O que fazer:** Em vez de um "Assistente Geral", transforme a IA em um especialista do seu tema escolhido.
- **Requisito:** O prompt deve conter regras de formatação (JSON) e instruções específicas sobre como classificar crimes daquela área.

---

## 2. O Raciocínio (Chain of Thought - CoT)

Utilize o endpoint `/analisar_cot` (ou equivalente).

- **O que fazer:** Crie um caso complexo/ambíguo relacionado ao seu tema (ex: se seu tema é Cibercrimes, crie um relato de "Golpe do Pix" que pareça furto mas é estelionato).
- **Requisito:** Mostre a IA "pensando passo a passo" para chegar à conclusão correta, provando que seu prompt de CoT funciona.

---

## 3. A Memória (RAG)

Utilize o endpoint de RAG (Aula 3) com o ChromaDB.

- **O que fazer:** Faça o upload de um pequeno documento texto ou PDF relacionado ao seu tema (pode ser uma lei específica, uma portaria fictícia ou um relatório de inteligência inventado).
- **Requisito:** Faça uma pergunta à API que só possa ser respondida com a informação contida nesse documento (provando que a IA não está alucinando, mas lendo a "memória").

---

## O Que Entregar (Formato de Envio)

A entrega será composta por dois arquivos:

### 1. O Relatório de Inteligência (PDF simples - Máx 2 páginas)

Deve conter:

- Nome e Tema Escolhido
- **Print 1:** O seu System Prompt modificado no código VS Code
- **Print 2:** O resultado do Swagger (`/docs`) mostrando a resposta do CoT
- **Print 3:** O resultado do Swagger mostrando a resposta do RAG baseada no documento

### 2. Vídeo Curto ou Link

- Um vídeo de tela de no máximo 2 minutos
- **Conteúdo:** Se apresente, mostre o terminal rodando o uvicorn, abra o Swagger, faça uma requisição e mostre a resposta chegando
- **Nota:** Não precisa editar. Grave a tela, narre brevemente ("Aqui é o aluno X, tema Y, rodando o endpoint Z") e envie. Não é necessário que você apareça na gravação, mas, se quiser, fique à vontade.

---

## Critérios de Avaliação (Rubrica Simplificada)

A nota (0 a 10) será composta por:

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Personalização** | 4,0 pts | O aluno adaptou os prompts para o tema escolhido ou apenas usou o código genérico da aula? O System Prompt está bem construído (com restrições e clareza)? |
| **Funcionalidade** | 4,0 pts | Os endpoints demonstrados no vídeo/prints funcionaram corretamente? (A IA respondeu o que foi pedido) |
| **Complexidade do Teste** | 2,0 pts | O caso de teste (o input usado) foi criativo/desafiador ou foi apenas um "Olá Mundo"? |

---

## Dicas para o Aluno

- Você pode e deve usar os códigos fornecidos nas aulas. O trabalho não é reescrever o Python do zero, é **saber configurar a IA** (Engenharia de Prompt e Contexto)
- Se seu computador for lento, use os modelos menores (`llama3.2` e `moondream` ou mais básicos ainda)
- Para o RAG, use um arquivo `.txt` simples criado no Bloco de Notas para facilitar a ingestão

---

**Prazo de Entrega:** 03/03/2026

**Forma de Envio:** Plataforma Atlas