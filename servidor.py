from fastapi import FastAPI
from fastapi.responses import FileResponse
import time

app = FastAPI()

# PROTOCOLO DE GÊNESE - VALORES TOTAIS E IMUTÁVEIS
MAX_SUPPLY = 10000000.00
# A rede nasce com o saldo que você já acumulou, o resto é reserva de emissão
SALDO_ATUAL = 789442.10 
RESERVA_GOV = 16104.62
START_TIME = 1738784193

@app.get('/')
async def read_index():
    return FileResponse('index.html')

@app.get('/api/nano_status')
async def nano_status():
    agora = time.time()
    # Mineração constante até atingir o teto de 10M
    minerado = (agora - START_TIME) * 0.015
    total_circulante = min(SALDO_ATUAL + minerado, MAX_SUPPLY)
    
    return {
        'circulante': round(total_circulante, 2),
        'reserva_gov': round(RESERVA_GOV + (minerado * 0.02), 2),
        'disponivel_emissao': round(MAX_SUPPLY - total_circulante, 2),
        'percent_emitido': round((total_circulante / MAX_SUPPLY) * 100, 2),
        'status': 'GENESIS_BLOCK_LOCKED'
    }
