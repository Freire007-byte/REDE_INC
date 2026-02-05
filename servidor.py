from fastapi import FastAPI
from fastapi.responses import FileResponse
import time, os

app = FastAPI()
START_TIME = 1738756800

@app.get('/')
async def read_index():
    return FileResponse('index.html')

@app.get('/api/nano_status')
async def nano_status():
    agora = time.time()
    saldo = round((agora - START_TIME) * 0.01, 2)
    integridade = round(99.90 + (agora % 0.08), 2)
    return {'saldo': saldo, 'integridade': integridade}
