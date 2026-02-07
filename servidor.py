from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Dados voláteis (Resetam ao reiniciar a função na Vercel Free)
ledger_data = {"accounts": {"TESOURARIA_MESTRE": 1000000000.0}, "blocos": 10402}

@app.get("/status")
async def status(wallet_id: str):
    if wallet_id not in ledger_data["accounts"]:
        ledger_data["accounts"][wallet_id] = 0.0
    return {
        "user_balance": ledger_data["accounts"].get(wallet_id, 0.0),
        "treasury": ledger_data["accounts"]["TESOURARIA_MESTRE"],
        "blocos": ledger_data["blocos"],
        "price_inc": 5.29,
        "status": "VALIDATED"
    }

@app.post("/api/faucet")
async def faucet(wallet_id: str):
    if ledger_data["accounts"]["TESOURARIA_MESTRE"] >= 10:
        ledger_data["accounts"][wallet_id] += 10
        ledger_data["accounts"]["TESOURARIA_MESTRE"] -= 10
        ledger_data["blocos"] += 1
        return {"status": "success"}
    return {"status": "error"}

@app.get("/")
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
