# 🚀 Comandos de Execução - Sistema de Predição de Sensação Térmica

Este documento explica todos os comandos necessários para executar o sistema completo de predição de sensação térmica.

## 📋 Pré-requisitos

- **Docker** instalado e em execução
- **Docker Compose** instalado
- **Portas disponíveis**: 8060, 1010, 5000, 8080, 8888, 9000, 9001, 5433

## 🎯 Comandos Principais

### 1. Navegar para o Diretório do Projeto
```bash
cd /home/raf75/quinto-periodo/avd/avd_projeto
```
**O que faz**: Move o terminal para o diretório raiz do projeto onde estão os arquivos Docker.

### 2. Iniciar Todos os Serviços
```bash
docker-compose up -d
```
**O que faz**: 
- Inicia todos os 6 containers em segundo plano (modo detached)
- **postgres**: Banco de dados PostgreSQL na porta 5433
- **minio**: Storage de objetos MinIO nas portas 9000-9001
- **thingsboard**: Plataforma IoT ThingsBoard na porta 8080
- **app**: Aplicação FastAPI + Jupyter nas portas 8060 e 1010
- **mlflow**: MLflow para ML tracking na porta 5000
- **trendz**: Trendz Analytics na porta 8888

### 3. Verificar Status dos Containers
```bash
docker-compose ps
```
**O que faz**: Lista todos os containers e seus status (Running, Exited, etc.)

### 4. Visualizar Logs da Aplicação
```bash
docker logs avd_app
```
**O que faz**: Mostra os logs completos do container da aplicação principal (FastAPI + Jupyter)

### 5. Visualizar Logs em Tempo Real
```bash
docker logs -f avd_app
```
**O que faz**: Mostra os logs da aplicação em tempo real (modo follow)

### 6. Reiniciar um Serviço Específico
```bash
docker-compose restart app
```
**O que faz**: Reinicia apenas o container da aplicação FastAPI/Jupyter

### 7. Parar Todos os Serviços
```bash
docker-compose down
```
**O que faz**: Para e remove todos os containers, mas mantém os volumes de dados

### 8. Parar e Remover Tudo (Incluindo Volumes)
```bash
docker-compose down -v
```
**O que faz**: Para containers, remove networks e volumes (CUIDADO: remove dados!)

## 🔍 Comandos de Verificação

### 9. Testar API REST
```bash
curl -I http://localhost:8060
```
**O que faz**: Testa se a API FastAPI está respondendo (HTTP HEAD request)

### 10. Testar Página Principal
```bash
curl -s http://localhost:8060/
```
**O que faz**: Baixa e exibe o HTML da página principal da aplicação

### 11. Testar Documentação da API
```bash
curl -I http://localhost:8060/docs
```
**O que faz**: Verifica se a documentação Swagger está acessível

### 12. Verificar Conectividade dos Serviços
```bash
curl -I http://localhost:1010  # Jupyter
curl -I http://localhost:5000  # MLflow
curl -I http://localhost:8080  # ThingsBoard
curl -I http://localhost:8888  # Trendz
curl -I http://localhost:9001  # MinIO Console
```
**O que faz**: Testa a conectividade de cada serviço individualmente

## 🐛 Comandos de Debug

### 13. Executar Comandos Dentro do Container
```bash
docker exec -it avd_app bash
```
**O que faz**: Abre um shell interativo dentro do container da aplicação

### 14. Verificar Processos no Container
```bash
docker exec avd_app ps aux
```
**O que faz**: Lista todos os processos rodando dentro do container

### 15. Testar Imports Python no Container
```bash
docker exec avd_app python -c "from app.routers import thermal_comfort"
```
**O que faz**: Testa se os imports Python estão funcionando corretamente

### 16. Verificar Logs de um Serviço Específico
```bash
docker logs avd_postgres    # PostgreSQL
docker logs avd_minio       # MinIO
docker logs avd_thingsboard # ThingsBoard
docker logs avd_mlflow      # MLflow
docker logs avd_trendz      # Trendz
```
**O que faz**: Visualiza logs específicos de cada serviço

## 🌐 URLs de Acesso

Após executar `docker-compose up -d`, os serviços estarão disponíveis em:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **FastAPI** | http://localhost:8060 | API REST principal |
| **Swagger Docs** | http://localhost:8060/docs | Documentação interativa |
| **ReDoc** | http://localhost:8060/redoc | Documentação alternativa |
| **Jupyter Lab** | http://localhost:1010 | Notebooks de análise |
| **MLflow** | http://localhost:5000 | Tracking de ML |
| **ThingsBoard** | http://localhost:8080 | Plataforma IoT |
| **Trendz Analytics** | http://localhost:8888 | Análise avançada |
| **MinIO Console** | http://localhost:9001 | Interface do storage |

## 📊 Testando a API

### 17. Testar Endpoint de Sensação Térmica
```bash
curl -X POST "http://localhost:8060/thermal/calculate" \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 25.0, "umidade": 60.0, "vento": 10.0}'
```
**O que faz**: Envia dados térmicos para calcular a sensação térmica

### 18. Listar Endpoints Disponíveis
```bash
curl -s http://localhost:8060/openapi.json | grep -o '"path":[^,]*' | head -10
```
**O que faz**: Lista os primeiros 10 endpoints disponíveis na API

## 🔧 Comandos de Manutenção

### 19. Limpar Containers Parados
```bash
docker container prune -f
```
**O que faz**: Remove todos os containers parados

### 20. Limpar Imagens Não Utilizadas
```bash
docker image prune -f
```
**O que faz**: Remove imagens Docker não utilizadas

### 21. Rebuild da Aplicação
```bash
docker-compose build app
docker-compose up -d app
```
**O que faz**: 
- Reconstrói a imagem da aplicação
- Reinicia o container com a nova imagem

### 22. Ver Uso de Recursos
```bash
docker stats
```
**O que faz**: Mostra uso de CPU, memória e rede dos containers em tempo real

## 🚨 Resolução de Problemas

### 23. Se a Porta Estiver em Uso
```bash
sudo lsof -i :8060  # Verificar o que usa a porta 8060
sudo kill -9 <PID>  # Matar processo se necessário
```

### 24. Se Houver Problemas de Permissão
```bash
sudo chown -R $USER:$USER /home/raf75/quinto-periodo/avd/avd_projeto
```

### 25. Reset Completo do Sistema
```bash
docker-compose down -v
docker system prune -f
docker-compose up -d
```
**O que faz**: Remove tudo e reinicia limpo (CUIDADO: remove dados!)

## ✅ Sequência de Inicialização Recomendada

1. ```bash
   cd /home/raf75/quinto-periodo/avd/avd_projeto
   ```

2. ```bash
   docker-compose up -d
   ```

3. ```bash
   sleep 30  # Aguardar serviços subirem
   ```

4. ```bash
   docker-compose ps  # Verificar status
   ```

5. ```bash
   curl -I http://localhost:8060  # Testar API
   ```

6. Acessar http://localhost:8060/docs no navegador

## 📈 Monitoramento

### 26. Verificar Logs de Todos os Serviços
```bash
docker-compose logs
```

### 27. Seguir Logs de um Serviço
```bash
docker-compose logs -f app
```

### 28. Ver Últimas 50 Linhas de Log
```bash
docker-compose logs --tail=50 app
```

## 🎯 Comandos Úteis para Desenvolvimento

### 29. Executar Python no Container
```bash
docker exec -it avd_app python
```

### 30. Instalar Dependências Adicionais
```bash
docker exec -it avd_app pip install <pacote>
```

### 31. Acessar Banco PostgreSQL
```bash
docker exec -it avd_postgres psql -U postgres -d postgres
```

---

## 📝 Notas Importantes

- **Sempre aguarde** 15-30 segundos após `docker-compose up -d` para os serviços iniciarem
- **Verifique portas livres** antes de iniciar os serviços
- **Use `docker-compose logs`** para diagnosticar problemas
- **O sistema possui 157.800 registros** de dados térmicos pré-carregados
- **Todos os serviços são stateless** exceto PostgreSQL (que persiste dados)

## 🆘 Suporte

Se encontrar problemas, execute na ordem:
1. `docker-compose ps` (verificar status)
2. `docker-compose logs app` (verificar logs)
3. `curl -I http://localhost:8060` (testar conectividade)
4. Consultar as URLs de acesso na tabela acima

---

**Sistema:** Predição de Sensação Térmica com Machine Learning  
**Última atualização:** Novembro 2025  
**Versão:** 1.0.0