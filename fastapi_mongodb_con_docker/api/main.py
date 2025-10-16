from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
import os


class Producto(BaseModel):
    producto: str
    nombre: str
    categoria: str
    cantidad: int
    ubicacion: str

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["almacen"]


@app.get("/")
async def root():
    colecciones = await db.list_collection_names()
    return {"ok": True, "colecciones": colecciones}

# Listar todos los productos
@app.get("/productos", response_description="Lista de productos", response_model=List[Producto])
async def list_productos():
    productos = await db["productos"].find().to_list(100)
    return productos

# Agregar un nuevo producto
@app.post("/producto/", response_description="Agregar un nuevo producto", response_model=Producto)
async def create_producto(producto: Producto):
    producto_dict = producto.dict()
    await db["productos"].insert_one(producto_dict)
    return producto

# Obtener producto por código
@app.get("/producto/{codigo}", response_description="Obtiene un producto específico", response_model=Producto)
async def find_by_codigo_producto(codigo: str):
    producto = await db["productos"].find_one({"producto": codigo})
    if producto:
        return Producto(**producto)
    raise HTTPException(status_code=404, detail=f"Código de producto {codigo} no encontrado.")

# Borrar producto por código
@app.delete("/producto/{codigo}", response_description="Borrar un producto con el código")
async def delete_producto(codigo: str):
    delete_result = await db["productos"].delete_one({"producto": codigo})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Producto con código {codigo} no encontrado.")
    return {"message": "Producto borrado con éxito"}

    