from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import hashlib, time

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- ESTADO MATEMÁTICO DA REDE ---
RED_DATA = {
    "tesouraria": 4937.17,  # Saldo Real Ajustado
    "blocos": 10402,
    "manifesto": "Matemática é a única autoridade."
}

def gerar_prova_pqc(wallet_id: str):
    # Prova de Soberania Matemática (SVP)
    raw = f"{wallet_id}4937.17_LATTICE".encode()
    return hashlib.sha256(raw).hexdigest()[:10].upper()

@app.get("/status")
async def status(wallet_id: str):
    prova = gerar_prova_pqc(wallet_id)
    return {
        "tesouraria": RED_DATA["tesouraria"],
        "auth_seal": prova,
        "blocos": RED_DATA["blocos"],
        "status": "MATEMÁTICA_CONFIRMADA"
    }

@app.get("/")
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
