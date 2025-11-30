-- Script de inicialização do banco de dados
-- PostgreSQL

-- Database para MLflow (created by POSTGRES_DB env var, but good to ensure)
SELECT 'CREATE DATABASE mlflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mlflow')\gexec

-- Database para dados do projeto
SELECT 'CREATE DATABASE avd_wind_data'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'avd_wind_data')\gexec

-- Database para ThingsBoard
SELECT 'CREATE DATABASE thingsboard'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'thingsboard')\gexec

-- Database para Trendz Analytics
SELECT 'CREATE DATABASE trendz'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'trendz')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mlflow TO "user";
GRANT ALL PRIVILEGES ON DATABASE avd_wind_data TO "user";
GRANT ALL PRIVILEGES ON DATABASE thingsboard TO "user";
GRANT ALL PRIVILEGES ON DATABASE trendz TO "user";
