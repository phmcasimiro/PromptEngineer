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

