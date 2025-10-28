# app.py
from fastapi import FastAPI, Body, HTTPException
from typing import List, Dict, Optional
from aiokafka import AIOKafkaProducer
import os, time, json, asyncio, httpx
import base64, uvicorn, asyncio

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
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
TOPIC_GOMMAGE = "habitantes.gommage"
NOMBRE = os.getenv("HABITANTE_NOMBRE", "Desconocido")
EDAD = int(os.getenv("HABITANTE_EDAD", "0"))
IMAGEN_PATH = os.getenv("HABITANTE_IMAGEN", "imagen.png")  # Ruta opcional a la imagen
PUERTO = int(os.getenv("PORT", 8000))
EDAD_GOMMAGE = 33
# Estado interno
pertenencias: List[str] = []
vivo: bool = True
vecinos: Dict[str, Dict[str, str | bool]] = {}  # {nombre: {"direccion": str, "vivo": bool}}
pintora: bool = bool(os.getenv("HABITANTE_PINTORA", False))
producer: Optional[AIOKafkaProducer] = None


# ----------------------------
# ENDPOINTS
# ----------------------------

async def start_producer():
    """Inicializa el productor Kafka de forma robusta."""
    global producer
    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
            await producer.start()
            print("🎨 La Pintora conectada a Kafka.")
            producer_ready.set()
            break
        except Exception as e:
            print(f"⚠️ Esperando a Kafka... ({e})")
            await asyncio.sleep(3)


async def send_gommage():
    payload = {"ts": int(time.time())}
    try:
        await producer.send_and_wait(TOPIC_GOMMAGE, json.dumps(payload).encode("utf-8"))
        await producer.flush()
    except Exception as e:
        print(f"❌ Error al enviar gommage: {e}")
        raise HTTPException(status_code=500, detail="Kafka no disponible")

@app.on_event("startup")
async def on_start():
    asyncio.create_task(start_producer())

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
async def gommage():
    global pintora
    if(pintora):
        await send_gommage()
    return {"ok": "gommage enviado"}


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

