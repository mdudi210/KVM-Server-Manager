from pydantic import BaseModel
from enum import StrEnum, auto

class ChangeState(BaseModel):
    state: str
    name: str

class CloneRequest(BaseModel):
    vmtoinstall: str
    name: str

class NewVmRequest(BaseModel):
    vmtoinstall: str
    name: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Roles(StrEnum):
    user = auto()
    admin = auto()

class NewUser(BaseModel):
    username: str
    password: str
    role : str