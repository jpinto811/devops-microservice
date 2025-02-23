import jwt
import datetime
import os

# Usar el mismo SECRET_KEY que está en Kubernetes
SECRET_KEY = "ju3W7bNrqh0Nj8GJoP518wCR7fkIld6ygVKuQaBy4C1AIIOFm7WbgAE1lIyDWyXq2t/JisHNwWMro+qBEDsMbA=="

# Generar el JWT
payload = {
    "iat": datetime.datetime.now(datetime.timezone.utc),
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

}

jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS512")
print(jwt_token)

