from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import zero_shot, few_shot, chain_of_thought, rag, visao

app = FastAPI(
    # Instanciamento da API IntelliDoc
    # Título da API
    title="IntelliDoc - O Escrivão Virtual (Crimes Patrimoniais)",
    # Descrição da API
    description="API especializada em auxiliar delegacias na classificação e análise de crimes contra o patrimônio.",
    # Versão da API
    version="1.0.0",
)

# Middleware de CORS — permite que o frontend (HTML/JS) se comunique com a API
# Adiciona o middleware de CORS
app.add_middleware(
    # Middleware de CORS
    CORSMiddleware,         
    # Permite requisições de qualquer origem
    allow_origins=["*"],    
    # Permite o envio de credenciais
    allow_credentials=True, 
    # Permite todos os métodos HTTP
    allow_methods=["*"],    
    # Permite todos os headers
    allow_headers=["*"],    
)

# Inclusão dos Routers
# Inclusão do Router Zero-Shot
app.include_router(zero_shot.router, prefix="/zero_shot", tags=["Zero-Shot"])
# Inclusão do Router Few-Shot
app.include_router(few_shot.router, prefix="/few_shot", tags=["Few-Shot"])
# Inclusão do Router Chain-of-Thought
app.include_router(chain_of_thought.router, prefix="/cot", tags=["Chain-of-Thought"])
# Inclusão do Router RAG
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
# Inclusão do Router Visão Computacional
app.include_router(visao.router, prefix="/visao", tags=["Visão Computacional"])

# Servindo os arquivos estáticos do frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Inclusão do endpoint raiz
@app.get("/")
async def root():
    return {
        "status": "online",
        "servico": "IntelliDoc",
        "especialidade": "Crimes Patrimoniais",
        "docs": "/docs",
        "frontend": "/static/index.html",
    }


# Execução da API
if __name__ == "__main__":
    import uvicorn

    # Execução da API
    uvicorn.run(app, host="0.0.0.0", port=8000)
