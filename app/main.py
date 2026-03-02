import os
import time
import psutil
import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import zero_shot, few_shot, chain_of_thought, few_shot_cot, rag, visao

# ── Logs Estruturados (Aula 5) ────────────────────────────────────────────────
# Configura structlog para emitir JSON com timestamp ISO-8601 em cada evento
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

# ── Instância do Aplicativo ────────────────────────────────────────────────────
app = FastAPI(
    title="IntelliDoc - O Escrivão Virtual (Crimes Patrimoniais)",
    description="API especializada em auxiliar delegacias na classificação e análise de crimes contra o patrimônio.",
    version="1.0.0",
)

# ── Métricas Prometheus (Aula 5) ──────────────────────────────────────────────
# Instrumenta todos os endpoints e expõe /metrics para Prometheus/Grafana
Instrumentator().instrument(app).expose(app)

# ── Middleware de CORS ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware de Benchmarking (Aula 4) ────────────────────────────────────────
# Intercepta toda requisição, mede o tempo de resposta e o consumo de RAM e
# injeta as métricas nos headers da resposta para auditoria técnica.
@app.middleware("http")
async def benchmark_middleware(request: Request, call_next):
    process = psutil.Process(os.getpid())
    ram_antes_mb = process.memory_info().rss / 1024 / 1024
    inicio = time.perf_counter()

    response = await call_next(request)

    duracao_s = time.perf_counter() - inicio
    ram_depois_mb = process.memory_info().rss / 1024 / 1024
    delta_ram_mb = ram_depois_mb - ram_antes_mb

    # Injeta métricas nos headers de resposta (visível no Swagger e ferramentas HTTP)
    response.headers["X-Tempo-Inferencia-s"] = f"{duracao_s:.3f}"
    response.headers["X-RAM-Delta-MB"] = f"{delta_ram_mb:.1f}"

    logger.info(
        "requisicao_processada",
        rota=str(request.url.path),
        metodo=request.method,
        tempo_s=round(duracao_s, 3),
        ram_delta_mb=round(delta_ram_mb, 1),
    )
    return response


# ── Tratamento Seguro de Erros (Aula 5) ───────────────────────────────────────
# Captura qualquer exceção não tratada, registra o erro completo no log interno
# e devolve ao usuário uma mensagem genérica sem vazar stacktrace.
@app.exception_handler(Exception)
async def handler_erro_global(request: Request, exc: Exception):
    logger.error(
        "erro_interno_nao_tratado",
        rota=str(request.url.path),
        erro=str(exc),
    )
    return JSONResponse(
        status_code=500,
        content={
            "status": "erro",
            "mensagem": "Falha interna no motor neural. A equipe de TI foi notificada.",
        },
    )


# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(zero_shot.router, prefix="/zero_shot", tags=["Zero-Shot"])
app.include_router(few_shot.router, prefix="/few_shot", tags=["Few-Shot"])
app.include_router(chain_of_thought.router, prefix="/cot", tags=["Chain-of-Thought"])
app.include_router(
    few_shot_cot.router, prefix="/fscot", tags=["Chain-of-Thought + Few-Shot"]
)
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
app.include_router(visao.router, prefix="/visao", tags=["Visão Computacional"])

# ── Frontend Estático ──────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# ── Endpoint Raiz ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Status"])
async def root():
    return {
        "status": "online",
        "servico": "IntelliDoc",
        "especialidade": "Crimes Patrimoniais",
        "docs": "/docs",
        "frontend": "/static/index.html",
        "metricas": "/metrics",
    }


# ── Execução Direta ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
