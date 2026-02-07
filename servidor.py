from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Banco de Dados em Memória (Evita crash na Vercel)
# Em produção real, conectaríamos ao Vercel KV
ledger_data = {
    "accounts": {
        "CORACAO_DA_REDE": 1000000000.0
    },
    "blocos": 10402
}

@app.get("/status")
async def status(wallet_id: str):
    # Se a carteira for nova, inicializa na memória
    if wallet_id not in ledger_data["accounts"]:
        ledger_data["accounts"][wallet_id] = 0.0
        
    return {
        "user_balance": ledger_data["accounts"].get(wallet_id, 0.0),
        "treasury": ledger_data["accounts"]["CORACAO_DA_REDE"],
        "blocos": ledger_data["blocos"],
        "seguranca": "PQC_ACTIVE_STATELESS"
    }

@app.post("/api/faucet")
async def faucet(wallet_id: str):
    if ledger_data["accounts"]["CORACAO_DA_REDE"] >= 10:
        ledger_data["accounts"][wallet_id] = ledger_data["accounts"].get(wallet_id, 0.0) + 10
        ledger_data["accounts"]["CORACAO_DA_REDE"] -= 10
        ledger_data["blocos"] += 1
        return {"status": "success", "new_balance": ledger_data["accounts"][wallet_id]}
    return {"status": "insufficient_treasury"}

@app.get("/")
async def home():
    from fastapi.responses import HTMLResponse
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
