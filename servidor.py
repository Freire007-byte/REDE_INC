from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core.atomo import NucleoAtomico
import os

app = FastAPI()
nucleo = NucleoAtomico()
cofre_alexandre = 0.0

@app.get("/", response_class=HTMLResponse)
async def home():
    # Caminho dinâmico para funcionar no seu Mac e na Vercel
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "web", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/nano_status")
async def nano_status():
    global cofre_alexandre
    valor = nucleo.calcular_entropia()
    if valor >= 99.98:
        cofre_alexandre += 0.05
    return {"integridade": valor, "saldo": round(cofre_alexandre, 2)}
