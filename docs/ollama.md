# OLLAMA: IA Generativa no seu Computador

O Ollama é uma ferramenta *open-source* que simplifica radicalmente a execução de Grandes Modelos de Linguagem (LLMs) localmente. Ele funciona como um gerenciador de modelos, permitindo que você baixe, execute e interaja com IAs potentes (como Llama 3, Mistral, Gemma e Qwen) diretamente no seu hardware, sem depender de nuvens externas.

### Por que rodar localmente?
- **Privacidade**: Seus dados nunca saem da sua máquina. Ideal para processar informações sensíveis ou corporativas.
- **Custo Zero**: Você não paga por token ou mensalidade de API; o custo é apenas o processamento do seu hardware.
- **Latência**: Respostas rápidas sem depender da conexão com a internet ou instabilidades de servidores externos.
- **Customização**: Facilidade para criar e ajustar modelos personalizados (Modelfiles).

---

## 📥 Instalação (Linux)

Para instalar o Ollama no Linux via script oficial:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 🚀 Como Iniciar

O Ollama utiliza uma arquitetura cliente-servidor. Ao instalar, o serviço geralmente inicia automaticamente em segundo plano.

### 1. Rodando seu primeiro modelo
Para baixar e iniciar um chat imediatamente com o Llama 3.2 (um modelo leve e eficiente):

```bash
ollama run llama3.2
```

### 2. Acessando via API
O Ollama expõe automaticamente uma API local na porta `11434`. Você pode integrá-lo com Python, Node.js ou ferramentas como Open WebUI e LangChain.

---

## 📑 Cheat Sheet (Guia de Comandos)

| Comando | Descrição | Exemplo |
| :--- | :--- | :--- |
| `ollama serve` | Inicia o servidor do Ollama manualmente | `ollama serve` |
| `ollama run` | Baixa (se necessário) e inicia o chat com um modelo | `ollama run llama3.2` |
| `ollama list` | Lista os modelos instalados no seu disco | `ollama list` |
| `ollama pull` | Baixa ou atualiza um modelo sem iniciar o chat | `ollama pull qwen2.5` |
| `ollama push` | Envia um modelo customizado para a biblioteca Ollama | `ollama push user/modelo` |
| `ollama rm` | Remove um modelo para liberar espaço em disco | `ollama rm mistral` |
| `ollama ps` | Mostra quais modelos estão carregados na RAM/VRAM | `ollama ps` |
| `ollama cp` | Cria um novo modelo a partir de um existente | `ollama cp llama3 meu-modelo` |
| `ollama show` | Exibe informações técnicas (Modelfile, parâmetros) | `ollama show llama3.2` |

---

## 💡 Dicas de Performance
- **GPU**: O Ollama detecta automaticamente GPUs NVIDIA e AMD. Rodar na placa de vídeo é significativamente mais rápido que na CPU.
- **Quantização**: Os modelos no Ollama já vêm quantizados (geralmente 4-bit), o que reduz drasticamente o uso de memória sem perda proporcional de inteligência.
- **Pruning**: Se o espaço em disco for um problema, use `ollama rm` em modelos que você não utiliza com frequência.