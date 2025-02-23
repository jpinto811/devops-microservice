# Usar una imagen de Python ligera
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias y luego instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el codigo fuente al contenedor
COPY . .

# Exponer el puerto 8000 para la API
EXPOSE 8000

# Comando para ejecutar la aplicacion
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]