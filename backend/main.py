import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.services import adlogin, list_vms, login, register, vm_cloner, vm_creator, vm_events, vm_state_manager

load_dotenv()

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:8080,http://127.0.0.1:8080,http://localhost,http://127.0.0.1",
)
origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()]

allow_credentials = True
if "*" in origins:
    allow_credentials = False

app = FastAPI(
    title="KVM Server API",
    version="1.1.0",
    description="API for managing KVM servers",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vm_cloner.router, tags=["vm"])
app.include_router(vm_creator.router, tags=["vm"])
app.include_router(vm_state_manager.router, tags=["vm"])
app.include_router(vm_events.router, tags=["vm"])
app.include_router(list_vms.router, tags=["vm"])
app.include_router(login.router, tags=["auth"])
app.include_router(adlogin.router, tags=["auth"])
app.include_router(register.router, tags=["user"])


@app.get("/")
def read_root():
    return {"message": "KVM Server API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
