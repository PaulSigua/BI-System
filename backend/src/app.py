from fastapi import FastAPI
from components.endpoints import router as endpoints_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
    
app = FastAPI(
    title='BI System Backend',
    description='Sistema de administración de información BI de la empresa',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta por defecto
@app.get('/', description='Endpoint por defecto')
async def root():
    return {'message': 'Bienvenido al sistema de administración de información BI'}

app.include_router(endpoints_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=9999)