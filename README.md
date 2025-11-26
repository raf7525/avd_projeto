# avd_projeto
# PROBLEMA SELECIONADO
Agrupar Padrões de Vento
Objetivo: Agrupar horários ou dias com comportamentos semelhantes de vento.
Dados: Direção e velocidade do vento.
Visualização: Rosa dos ventos colorida por cluster + painel com médias por grupo.

## 🚀 CONFIGURAÇÃO RÁPIDA TRENDZ ANALYTICS

### Executar configuração automática:
```bash
./setup-trendz.sh
```

### Acesso aos serviços:
- **Trendz Analytics**: http://localhost:8888 (tenant@thingsboard.org / tenant)
- **ThingsBoard**: http://localhost:8080 (tenant@thingsboard.org / tenant)

📖 **Guia completo**: [docs/trendz-setup-guide.md](docs/trendz-setup-guide.md)


# PORTAS
como requisitado no projeto as portas são essas:
 FastAPI:         http://localhost:8060
 Jupyter:         http://localhost:1010
 MLflow:          http://localhost:5000
 Trendz Analytics: http://localhost:8888
 ThingsBoard:     http://localhost:8080
  MinIO Console:    http://localhost:9001 (admin/minioadmin)
 PostgreSQL:      localhost:5433 (user/password)

# passos fastapi
 Autenticação: JWT tokens, OAuth2
 Banco real: Trocar simulação por PostgreSQL
 ML Pipeline: Integrar modelos de clustering
 Dashboard: Endpoints para visualizações
 Deploy: Containerizar e publicar