from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import hashlib, sqlite3, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = "inc_quantum.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS contas (id TEXT PRIMARY KEY, saldo REAL, hash_pqc TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS meta (chave TEXT PRIMARY KEY, valor INTEGER)")
    # SALDO OFICIAL SOLICITADO
    c.execute("INSERT OR IGNORE INTO contas VALUES ('CORACAO_DA_REDE', 75283.03, 'ROOT_MASTER')")
    c.execute("INSERT OR IGNORE INTO meta VALUES ('blocos', 0)")
    conn.commit()
    conn.close()

init_db()

@app.get("/status")
async def status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT saldo FROM contas WHERE id = 'CORACAO_DA_REDE'")
    res = c.fetchone()
    c.execute("SELECT valor FROM meta WHERE chave = 'blocos'")
    blocos = c.fetchone()[0]
    conn.close()
    return {"tesouraria": res[0] if res else 0.0, "blocos": blocos, "status": "OPERACIONAL"}

@app.post("/enviar")
async def enviar(destinatario: str, valor: float):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    taxa = valor * 0.02
    c.execute("UPDATE contas SET saldo = saldo - ? WHERE id = 'CORACAO_DA_REDE'", (valor,))
    c.execute("UPDATE meta SET valor = valor + 1 WHERE chave = 'blocos'")
    conn.commit()
    conn.close()
    return {"status": "sucesso"}
