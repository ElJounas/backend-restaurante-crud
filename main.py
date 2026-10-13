from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Restaurante - Sistema de Comandos ADSO",
    description="API RESTful para la gestión del menú de restaurante (Módulo Plato)",
    version="1.0.0"
)

# Modelo Pydantic con validaciones de campos clave
class Plato(BaseModel):
    id: int
    nombre_plato: str
    categoria: str  # Entrada, Fuerte, Postre, Bebida
    precio_cop: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    apto_vegetarianos: bool

# Modelo para actualizar datos del plato
class PlatoUpdate(BaseModel):
    nombre_plato: str
    categoria: str
    precio_cop: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    apto_vegetarianos: bool

# Base de datos en memoria (Simulada)
db_platos: List[Plato] = [
    Plato(
        id=1,
        nombre_plato="Bandeja Paisa",
        categoria="Fuerte",
        precio_cop=35000.0,
        apto_vegetarianos=False
    ),
    Plato(
        id=2,
        nombre_plato="Ensalada César Vegetariana",
        categoria="Entrada",
        precio_cop=18000.0,
        apto_vegetarianos=True
    )
]

# --- ENDPOINTS DE LA API ---

# 1. READ ALL: Listar menú completo
@app.get("/api/v1/platos", response_model=List[Plato], status_code=status.HTTP_200_OK)
def obtener_todos_los_platos():
    return db_platos

# 2. READ ONE: Consultar un plato por ID
@app.get("/api/v1/platos/{plato_id}", response_model=Plato, status_code=status.HTTP_200_OK)
def obtener_plato_por_id(plato_id: int):
    for plato in db_platos:
        if plato.id == plato_id:
            return plato
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El plato con ID {plato_id} no existe en el menú."
    )

# 3. CREATE: Registrar un nuevo plato
@app.post("/api/v1/platos", response_model=Plato, status_code=status.HTTP_201_CREATED)
def crear_nuevo_plato(plato: Plato):
    for p in db_platos:
        if p.id == plato.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de registro: Ya existe un plato registrado con el ID {plato.id}."
            )
    db_platos.append(plato)
    return plato

# 4. UPDATE: Actualizar datos de un plato
@app.put("/api/v1/platos/{plato_id}", response_model=Plato, status_code=status.HTTP_200_OK)
def actualizar_plato(plato_id: int, datos_actualizados: PlatoUpdate):
    for index, plato in enumerate(db_platos):
        if plato.id == plato_id:
            plato_modificado = Plato(
                id=plato_id,
                nombre_plato=datos_actualizados.nombre_plato,
                categoria=datos_actualizados.categoria,
                precio_cop=datos_actualizados.precio_cop,
                apto_vegetarianos=datos_actualizados.apto_vegetarianos
            )
            db_platos[index] = plato_modificado
            return plato_modificado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El plato con ID {plato_id} no fue encontrado."
    )

# 5. DELETE: Eliminar un plato del menú
@app.delete("/api/v1/platos/{plato_id}", status_code=status.HTTP_200_OK)
def eliminar_plato(plato_id: int):
    for index, plato in enumerate(db_platos):
        if plato.id == plato_id:
            db_platos.pop(index)
            return {"mensaje": f"El plato con ID {plato_id} fue eliminado del menú exitosamente."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El plato con ID {plato_id} no existe."
    )