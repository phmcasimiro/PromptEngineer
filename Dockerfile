# ── Etapa 1: Imagem Base ───────────────────────────────────────────────────────
# Imagem enxuta do Linux com Python 3.11 pré-instalado
FROM python:3.11-slim

# ── Etapa 2: Diretório de Trabalho ────────────────────────────────────────────
WORKDIR /app

# ── Etapa 3: Cache Trick (Instalar dependências antes do código-fonte) ─────────
# Copiamos apenas requirements.txt primeiro para aproveitar o cache do Docker.
# Se o código mudar mas as libs não, esta camada não é reconstruída.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Etapa 4: Código-Fonte ──────────────────────────────────────────────────────
COPY app/ ./app/
COPY docs/ ./docs/

# ── Etapa 5: Porta ────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Etapa 6: Comando de Inicialização ─────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
