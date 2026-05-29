from fastapi import FastAPI
from app.routers import user_routes, book_routes, loan_routes, auth_routes

app = FastAPI(title="PyLibManager")

app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(loan_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Sistema de biblioteca",
        "docs": "/docs"
    }