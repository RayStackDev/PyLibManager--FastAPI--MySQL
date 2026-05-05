from fastapi import FastAPI

app = FastAPI(
    title="PyLibManager",
    description="API para Gerenciamento de biblioteca",
    version="1.0.0" 
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Sistema de biblioteca",
        "docs": "/docs"
    }