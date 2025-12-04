# Dockerfile para o projeto de análise de padrões de vento
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de requirements
COPY requirements.txt .

# Instalar uv
RUN pip install uv

# Instalar dependências Python com uv (mais rápido)
RUN uv pip install --system --no-cache -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta para FastAPI
EXPOSE 8060

# Expor porta para MLflow (se necessário)
EXPOSE 5000

# Expor porta para Jupyter Notebook
EXPOSE 1010

# Comando padrão (pode ser sobrescrito no docker-compose)
CMD ["python", "-c", "print('Container iniciado! Use docker-compose para serviços específicos.')"]