-- Script de inicialização do banco de dados
-- Cria databases necessários para o projeto

-- Database para MLflow
CREATE DATABASE IF NOT EXISTS mlflow;

-- Database para dados do projeto (opcional)
CREATE DATABASE IF NOT EXISTS avd_wind_data;

-- Database para ThingsBoard
CREATE DATABASE IF NOT EXISTS thingsboard;

-- Database para Trendz Analytics
CREATE DATABASE IF NOT EXISTS trendz;

-- Usuário para aplicação (já criado via env vars, mas garantindo permissões)
GRANT ALL PRIVILEGES ON DATABASE mlflow TO "user";
GRANT ALL PRIVILEGES ON DATABASE avd_wind_data TO "user";
GRANT ALL PRIVILEGES ON DATABASE thingsboard TO "user";
GRANT ALL PRIVILEGES ON DATABASE trendz TO "user";