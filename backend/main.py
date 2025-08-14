from fastapi import FastAPI
from backend.src.services import list_vms, login, register, vm_cloner, vm_creator, vm_state_manager
from backend.src.auth import check_token
from fastapi.middleware.cors import CORSMiddleware

# Allow frontend origin
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app = FastAPI(
    title="KVM Server api",
    version="1.0.0",
    description="API for managing KVM-Server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (defined in app/api/*.py)
app.include_router(vm_cloner.router, tags=["vm"])
app.include_router(vm_creator.router, tags=["vm"])
app.include_router(vm_state_manager.router, tags=["vm"])
app.include_router(list_vms.router, tags=["vm"])
app.include_router(login.router, tags=["vm"])
app.include_router(register.router, tags=["vm"])
app.include_router(check_token.router, tags=["vm"])

# Optionally: Add root health check
@app.get("/")
def read_root():
    return {"message": ""}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

