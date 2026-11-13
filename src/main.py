from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.core.database import Base, engine
from src.modules.auth.infrastructure import models_db as auth_models
from src.modules.supliers.infrastructure import models_db as supliers_models
from src.modules.inventory.infrastructure import models_db as inventory_models
from src.modules.kardex.infrastructure import models_db as kardex_models
from src.modules.auth.presentation.router import router as auth_router
from src.modules.supliers.presentation.router import router as supliers_router
from src.modules.inventory.presentation.router import router as inventory_router
from src.modules.kardex.presentation.router import router as kardex_router

app = FastAPI(
    title="Kardex Agrícola API",
    version="1.1.0",
    description="Sistema de gestión agrícola, cosechas e inventario."
)

# Crea las tablas declaradas en los modelos si todavía no existen.
Base.metadata.create_all(bind=engine)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(auth_router)
app.include_router(supliers_router)
app.include_router(inventory_router)
app.include_router(kardex_router)


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", tags=["sistema"])
def health():
    return {"status": "ok", "service": "Kardex Agrícola"}
