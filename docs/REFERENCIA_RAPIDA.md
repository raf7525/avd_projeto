# 🚀 Referência Rápida - Sistema de Predição de Sensação Térmica

## ⚡ Comandos Essenciais

### Iniciar Sistema Completo
```bash
# Opção 1: Script automatizado (RECOMENDADO)
./executar.sh

# Opção 2: Docker Compose manual
docker-compose up -d
```

### Verificar Status
```bash
# Opção 1: Script
./executar.sh status

# Opção 2: Docker Compose
docker-compose ps
```

### Parar Sistema
```bash
# Opção 1: Script
./executar.sh stop

# Opção 2: Docker Compose
docker-compose down
```

## 🌐 URLs Principais

| Serviço | URL | Função |
|---------|-----|---------|
| **API Principal** | http://localhost:8060 | Interface principal |
| **Documentação** | http://localhost:8060/docs | Swagger UI |
| **Jupyter** | http://localhost:1010 | Notebooks |
| **MLflow** | http://localhost:5000 | ML Tracking |

## 🔧 Comandos do Script

```bash
./executar.sh start    # Iniciar sistema
./executar.sh stop     # Parar sistema
./executar.sh restart  # Reiniciar sistema
./executar.sh status   # Ver status
./executar.sh logs     # Ver logs
./executar.sh test     # Testar conectividade
./executar.sh clean    # Limpeza completa
./executar.sh help     # Ajuda
```

## 🆘 Solução Rápida de Problemas

```bash
# Sistema não inicia?
./executar.sh clean && ./executar.sh start

# API não responde?
docker-compose restart app

# Ver erros?
docker logs avd_app

# Testar conectividade?
./executar.sh test
```

## 📊 Testar API

```bash
# Teste básico
curl http://localhost:8060

# Calcular sensação térmica
curl -X POST "http://localhost:8060/thermal/calculate" \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 25.0, "umidade": 60.0, "vento": 10.0}'
```

## ✅ Checklist de Inicialização

1. ✅ Docker rodando?
2. ✅ Portas livres? (8060, 1010, 5000, 8080, 8888, 9000, 9001, 5433)
3. ✅ Executar: `./executar.sh`
4. ✅ Aguardar 30 segundos
5. ✅ Acessar: http://localhost:8060/docs

---

**💡 Dica**: Use `./executar.sh` para tudo! Ele automatiza verificações e fornece feedback colorido.