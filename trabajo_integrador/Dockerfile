FROM python:3.11-slim

# Evita que Python guarde configuraciones en el contenedor 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos las librerías necesarias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la app
COPY app/ /app/

# Exponemos el puerto de la aplicación
EXPOSE 5000

# Iniciamos el servidor de Python
CMD ["python", "app.py"]
