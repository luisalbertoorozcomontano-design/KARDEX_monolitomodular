from fastapi import FastAPI
from src.core.database import Base, engine
from src.modules.auth.infrastructure import models_db as auth_models
from src.modules.supliers.infrastructure import models_db as supliers_models
from src.modules.inventory.infrastructure import models_db as inventory_models
from src.modules.kardex.infrastructure import models_db as kardex_models
from src.modules.auth.presentation.router import router as auth_router
from src.modules.supliers.presentation.router import router as supliers_router
from src.modules.inventory.presentation.router import router as inventory_router
from src.modules.kardex.presentation.router import router as kardex_router

app = FastAPI(title="Kardex Agricola API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(supliers_router)
app.include_router(inventory_router)
app.include_router(kardex_router)


@app.get("/")
def root():
    return {"msg": "Kardex Agricola API funcionando"}
