from fastapi import FastAPI, Header, HTTPException
import jwt
import datetime
import uuid
import os
from pydantic import BaseModel, Field


# Cargar las variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

if not SECRET_KEY:
    raise RuntimeError("ERROR: SECRET_KEY no está definido en las variables de entorno.")
API_KEY = os.getenv("API_KEY", "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c")

app = FastAPI()

# Modelo para validar la entrada del JSON
class MessageRequest(BaseModel):
    message: str
    to: str
    from_: str = Field(alias="from")
    timeToLifeSec: int


@app.post("/DevOps")
def devops_endpoint(
    request: MessageRequest,
    x_parse_rest_api_key: str = Header(default=None),  # Ahora permite que falte el header
    x_jwt_kwy: str = Header(default=None)  # Ahora permite que falte el header
):
    # Validar API Key
    if not x_parse_rest_api_key or x_parse_rest_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="ERROR: Invalid API Key")
    
    # Validar JWT
    if not x_jwt_kwy:
        raise HTTPException(status_code=401, detail="ERROR: Invalid JWT")

    try:
        decoded_jwt = jwt.decode(x_jwt_kwy, SECRET_KEY, algorithms=["HS512"])
        
        # Verificar si el token ha expirado
        if datetime.datetime.now(datetime.timezone.utc) > datetime.datetime.fromtimestamp(decoded_jwt["exp"], tz=datetime.timezone.utc):
            raise HTTPException(status_code=401, detail="ERROR: JWT Expired")
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="ERROR: JWT Expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="ERROR: Invalid JWT")

    return {"message": f"Hello {request.to}, your message will be sent"}

# Manejar otros métodos HTTP no permitidos
@app.api_route("/DevOps", methods=["GET", "PUT", "DELETE"])
def not_allowed():
    raise HTTPException(status_code=405, detail="ERROR")

print(f"SECRET_KEY en backend: {SECRET_KEY}")
