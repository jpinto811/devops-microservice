import requests
import os
import jwt
import datetime
import pytest
from unittest.mock import patch
import main

# Definir la URL base
BASE_URL = "http://192.168.49.2:32497"

# Variables de entorno simuladas
API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
SECRET_KEY = "ju3W7bNrqh0Nj8GJoP518wCR7fkIld6ygVKuQaBy4C1AIIOFm7WbgAE1lIyDWyXq2t/JisHNwWMro+qBEDsMbA=="

# Generar un JWT válido
JWT_TOKEN = jwt.encode(
    {
        "sub": "test_user",
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=45),
    },
    SECRET_KEY,
    algorithm="HS512",
)

# ✅ Test 1: Prueba una solicitud válida con API Key y JWT correctos
def test_valid_post_request():
    """Prueba que el endpoint responda correctamente con datos válidos"""
    headers = {
        "X-Parse-REST-API-Key": API_KEY,
        "X-JWT-KWY": JWT_TOKEN
    }
    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = requests.post(f"{BASE_URL}/DevOps", json=data, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {data['to']}, your message will be sent"}

# ✅ Test 2: Prueba si falta la API Key
def test_missing_api_key():
    """Prueba que la API devuelva 401 si falta la API Key"""
    headers = {
        "X-JWT-KWY": JWT_TOKEN  # Falta la API Key
    }
    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = requests.post(f"{BASE_URL}/DevOps", json=data, headers=headers)
    assert response.status_code == 401

# ✅ Test 3: Prueba si falta el JWT
def test_missing_jwt():
    """Prueba que la API devuelva 401 si falta el JWT"""
    headers = {
        "X-Parse-REST-API-Key": API_KEY  # Falta el JWT
    }
    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = requests.post(f"{BASE_URL}/DevOps", json=data, headers=headers)
    assert response.status_code == 401

# ✅ Test 4: Prueba con una API Key inválida
def test_invalid_api_key():
    """Prueba que la API devuelva 401 si la API Key es incorrecta"""
    headers = {
        "X-Parse-REST-API-Key": "invalid-api-key",
        "X-JWT-KWY": JWT_TOKEN
    }
    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = requests.post(f"{BASE_URL}/DevOps", json=data, headers=headers)
    assert response.status_code == 401

# ✅ Test 5: Prueba con un JWT inválido
def test_invalid_jwt():
    """Prueba que la API devuelva 401 si el JWT es inválido"""
    headers = {
        "X-Parse-REST-API-Key": API_KEY,
        "X-JWT-KWY": "invalid.token.value"
    }
    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    response = requests.post(f"{BASE_URL}/DevOps", json=data, headers=headers)
    assert response.status_code == 401

# ✅ Test 6: Prueba que el servidor no permita otros métodos (405)
def test_method_not_allowed():
    """Prueba que la API devuelva 405 si se usa un método no permitido"""
    response = requests.put(f"{BASE_URL}/DevOps")  # Intentar con PUT en lugar de POST
    assert response.status_code == 405
