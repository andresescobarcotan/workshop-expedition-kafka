# app.py
from fastapi import FastAPI, Body, HTTPException
from typing import List, Dict, Optional
from aiokafka import AIOKafkaConsumer
import os
import httpx
import sys
import base64
import uvicorn
import asyncio
import json
import time

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Habitante API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------
NOMBRE = os.getenv("HABITANTE_NOMBRE", "Desconocido")
EDAD = int(os.getenv("HABITANTE_EDAD", "0"))
IMAGEN_PATH = os.getenv("HABITANTE_IMAGEN", "imagen.png")  # Ruta opcional a la imagen
PUERTO = int(os.getenv("PORT", 8000))
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
TOPIC_GOMMAGE = "habitantes.gommage"
GROUP_ID = f"habitante-{NOMBRE}-{int(time.time())}"
EDAD_GOMMAGE = 33
# Estado interno
pertenencias: List[str] = []
vivo: bool = True
vecinos: Dict[str, Dict[str, str | bool]] = {}  # {nombre: {"direccion": str, "vivo": bool}}
pintora: bool = bool(os.getenv("HABITANTE_PINTORA", False))
consumer: Optional[AIOKafkaConsumer] = None  # ✅ Declaramos variable global




# ----------------------------
# ENDPOINTS
# ----------------------------


@app.on_event("startup")
async def startup_event():
    print(f"🚀 {NOMBRE} esperando 10s antes de iniciar consumidor...")
    await asyncio.sleep(10)
    """Se lanza cuando el servicio arranca."""
    print(f"🚀 {NOMBRE} iniciando consumidor de gommage en {KAFKA_SERVER}...")
    asyncio.create_task(consumir_gommage())

@app.on_event("shutdown")
async def shutdown_event():
    if consumer:
        print(f"🧹 {NOMBRE} cerrando consumer...")
        try:
            await consumer.stop()
        except Exception as e:
            print(f"⚠️ Error cerrando consumer: {e}")


async def consumir_gommage():
    global EDAD, EDAD_GOMMAGE, NOMBRE, consumer
    global vivo
    consumer = AIOKafkaConsumer(
        TOPIC_GOMMAGE,
        bootstrap_servers=KAFKA_SERVER,
        group_id=GROUP_ID,
        enable_auto_commit=True,
    )

    await consumer.start()
    try:
        async for msg in consumer:
            evento = json.loads(msg.value.decode())
            if(EDAD > EDAD_GOMMAGE):
                vivo = False
                print(f"💀 {NOMBRE} recibió gommage (edad={EDAD}). Saliendo...")
                
            else:
                EDAD += 1
    finally:
        await consumer.stop()
        if not vivo:
            sys.exit(0)

@app.on_event("shutdown")
async def shutdown_event():
    if consumer:
        print(f"🧹 {NOMBRE} cerrando consumer...")
        try:
            await consumer.stop()
        except Exception as e:
            print(f"⚠️ Error cerrando consumer: {e}")

@app.get("/name")
def get_name():
    return {"name": NOMBRE}

@app.get("/edad")
def get_edad():
    return {"edad": EDAD}

@app.get("/imagen")
def get_imagen():
    """Devuelve la imagen del habitante codificada en base64."""
    if not os.path.exists(IMAGEN_PATH):
        raise HTTPException(status_code=404, detail="No se encontró la imagen del habitante.")
    with open(IMAGEN_PATH, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return {"imagen_base64": encoded}

@app.get("/salud")
def get_salud():
    """Devuelve el estado de vida del servicio."""
    return {"estado": "vivo" if vivo else "muerto"}

@app.post("/gommage")
def gommage():
    return {"error": "Es un habitante, no la pintora"}
# ----------------------------
# VECINOS
# ----------------------------

@app.get("/vecinos")
def get_vecinos():
    """Devuelve la lista de vecinos conocidos."""
    return {"vecinos": list(vecinos.keys())}

@app.get("/vecinos/{nombre}")
def get_vecino(nombre: str):
    """Devuelve la información de un vecino (dirección y estado)."""
    if nombre not in vecinos:
        raise HTTPException(status_code=404, detail="Vecino no encontrado.")
    return {"nombre": nombre, **vecinos[nombre]}

@app.patch("/vecinos/{nombre}")
def patch_vecino(nombre: str, data: Dict[str, str | bool] = Body(..., example={"vivo": False})):
    """Actualiza la información de un vecino (por ejemplo, marcarlo como muerto)."""
    if nombre not in vecinos:
        raise HTTPException(status_code=404, detail="Vecino no encontrado.")
    vecinos[nombre].update(data)
    return {"message": "Vecino actualizado", "vecino": vecinos[nombre]}

# ----------------------------
# UTILIDAD PARA REGISTRAR VECINOS (opcional)
# ----------------------------
@app.put("/vecinos")
def add_vecinos(data: Dict[str, Dict[str, str | bool]] = Body(..., example={
    "Marco": {"direccion": "http://localhost:8001", "vivo": True}
})):
    """Permite registrar nuevos vecinos manualmente."""
    vecinos.update(data)
    return {"message": "Vecinos añadidos", "vecinos": vecinos}


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    print(f"🏠 Iniciando habitante {NOMBRE} en puerto {PUERTO}")
    uvicorn.run("app:app", host="0.0.0.0", port=PUERTO)

