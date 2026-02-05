from fastapi import FastAPI
from fastapi.responses import FileResponse
import time
import os

app = FastAPI()

# Marco Zero da REDE INC (5 de Fev de 2026)
START_TIME = 1738756800 

@app.get("/")
async def read_index():
    # Localiza a pasta 'web' de forma absoluta para evitar tela branca
    base_path = os.path.dirname(os.path.realpath(__file__))
    path_to_file = os.path.join(base_path, 'web', 'index.html')
    return FileResponse(path_to_file)

@app.get("/api/nano_status")
async def nano_status():
    agora = time.time()
    # Mineração constante: 0.01 INC por segundo
    saldo_calculado = (agora - START_TIME) * 0.01 
    # Oscilação da Entropia (Simulação de vida do núcleo)
    integridade = 99.90 + (time.time() % 0.08)
    
    return {
        "saldo": round(saldo_calculado, 2),
        "integridade": round(integridade, 2)
    }

# Linha de comando para rodar no MacBook
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
