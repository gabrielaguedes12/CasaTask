from fastapi import FastAPI

from .database import engine, Base
from .routers import pessoas, tarefas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CasaTask API")

app.include_router(pessoas.router)
app.include_router(tarefas.router)


@app.get("/")
def raiz():
    return {"mensagem": "CasaTask API rodando!"}