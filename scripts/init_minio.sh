#!/bin/bash

# Script para inicializar o MinIO e criar o bucket necessário
# Aguarda o MinIO estar pronto e então cria o bucket mlflow-artifacts

echo "🪣 Aguardando MinIO estar pronto..."

# Aguardar MinIO estar disponível
until curl -sf http://minio:9000/minio/health/live > /dev/null 2>&1
do
  echo "⏳ MinIO ainda não está pronto, aguardando..."
  sleep 2
done

echo "✅ MinIO está pronto!"

# Instalar cliente mc (MinIO Client) se não existir
if ! command -v mc &> /dev/null; then
    echo "📥 Instalando MinIO Client..."
    curl -o /usr/local/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
    chmod +x /usr/local/bin/mc
fi

# Configurar alias para o MinIO local
echo "🔧 Configurando MinIO Client..."
mc alias set myminio http://minio:9000 minioadmin minioadmin

# Criar bucket se não existir
echo "🪣 Verificando/Criando bucket mlflow-artifacts..."
if mc ls myminio/mlflow-artifacts > /dev/null 2>&1; then
    echo "✅ Bucket mlflow-artifacts já existe!"
else
    mc mb myminio/mlflow-artifacts
    echo "✅ Bucket mlflow-artifacts criado com sucesso!"
fi

# Definir política pública (opcional, para desenvolvimento)
mc anonymous set download myminio/mlflow-artifacts

echo "🎉 MinIO inicializado com sucesso!"
