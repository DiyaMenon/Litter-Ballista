from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Litter Ballista Backend", version="2.0.0")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # To run with relative imports, execute from the root directory using:
    # uvicorn backend.app:app --reload
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)