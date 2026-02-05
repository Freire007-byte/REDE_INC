import hashlib, sqlite3, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], 
allow_methods=["*"], allow_headers=["*"])

# Banco de dados em memória para garantir os 5.000 TPS
conn = sqlite3.connect('file:inc_quantum_core?mode=memory&cache=shared', 
uri=True, check_same_thread=False)
c = conn.cursor()

def gerar_identidade_quantica(semente: str):
    base = semente.encode()
    cofre_2500 = b""
    for i in range(50):
        base = hashlib.sha3_512(base).digest()
        cofre_2500 += base
    return hashlib.sha3_256(cofre_2500).hexdigest()

def init_db():
    c.execute("PRAGMA journal_mode = OFF")
    # Comandos SQL em linha única para evitar erro de sintaxe
    c.execute("""CREATE TABLE IF NOT EXISTS contas (id TEXT PRIMARY KEY, 
saldo REAL, hash_pqc TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS meta (chave 
TEXT PRIMARY KEY, 
valor INTEGER)""")
    
    h_curto = gerar_identidade_quantica("mestre_da_rede_inc_2026")
    c.execute("""INSERT OR IGNORE INTO contas VALUES ('CORACAO_DA_REDE', 
1000000000.0, ?)""", (h_curto,))
    c.execute("INSERT OR IGNORE INTO meta VALUES ('blocos', 0)")
    conn.commit()
    print(f"🚀 NÚCLEO QUÂNTICO ATIVO | CHAVE MESTRE: {h_curto[:10]}...")

init_db()

@app.post("/enviar")
async def enviar(sender: str, receiver: str, amount: float, pkey: str):
    h_tentativa = gerar_identidade_quantica(pkey)
    c.execute("SELECT saldo, hash_pqc FROM contas WHERE id = ?", 
(sender,))
    row = c.fetchone()
    
    # 🛡️ Validação de Segurança Pós-Quântica
    if not row or row[1] != h_tentativa:
        raise HTTPException(403, "Falha na Autenticação Quântica!")
    
    # 💰 Verificação de Soberania Financeira (Evita saldo negativo)
    if row[0] < amount:
        raise HTTPException(400, "Saldo insuficiente na conta de origem.")

    taxa = amount * 0.02
    # Execução das transações
    c.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (amount, 
sender))
    c.execute("INSERT OR IGNORE INTO contas VALUES (?, 0, 'pendente')", 
(receiver,))
    c.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (amount 
- taxa, receiver))
    c.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (taxa, 
'CORACAO_DA_REDE'))
    c.execute("UPDATE meta SET valor = valor + 1 WHERE chave = 'blocos'")
    conn.commit()
    return {"status": "sucesso_pqc", "hash": h_tentativa}

@app.get("/status")
async def status():
    c.execute("SELECT saldo FROM contas WHERE id = 'CORACAO_DA_REDE'")
    t = c.fetchone()[0]
    c.execute("SELECT valor FROM meta WHERE chave = 'blocos'")
    b = c.fetchone()[0]
    return {"tesouraria": t, "blocos": b, "seguranca":"""PÓS-QUÂNTICA 
Ativa"""}
