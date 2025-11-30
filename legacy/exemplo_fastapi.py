"""
Exemplo Educacional - FastAPI Básico
====================================

Este arquivo mostra como FastAPI funciona na prática.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 1. CRIAR A APLICAÇÃO
app = FastAPI(title="Exemplo Educacional FastAPI")

# 2. MODELO DE DADOS (Pydantic)
class Pessoa(BaseModel):
    nome: str
    idade: int
    email: Optional[str] = None

class PessoaResposta(BaseModel):
    id: int
    nome: str
    idade: int
    email: Optional[str]
    criado_em: datetime

# 3. "BANCO DE DADOS" SIMULADO
pessoas_db: List[dict] = []

# 4. ENDPOINTS

# GET simples
@app.get("/")
def pagina_inicial():
    """Página inicial da API"""
    return {"mensagem": "Bem-vindo à API de Pessoas!"}

# GET com parâmetro na URL
@app.get("/pessoa/{pessoa_id}")
def obter_pessoa(pessoa_id: int):
    """Buscar pessoa por ID"""
    for pessoa in pessoas_db:
        if pessoa["id"] == pessoa_id:
            return pessoa
    
    # Se não encontrou, retorna erro 404
    raise HTTPException(status_code=404, detail="Pessoa não encontrada")

# GET com query parameters
@app.get("/pessoas")
def listar_pessoas(
    limite: int = Query(10, description="Número máximo de pessoas"),
    idade_minima: Optional[int] = Query(None, description="Idade mínima")
):
    """Listar pessoas com filtros"""
    pessoas_filtradas = pessoas_db.copy()
    
    # Aplicar filtro de idade
    if idade_minima:
        pessoas_filtradas = [p for p in pessoas_filtradas if p["idade"] >= idade_minima]
    
    # Aplicar limite
    return pessoas_filtradas[:limite]

# POST com validação automática
@app.post("/pessoas", response_model=PessoaResposta)
def criar_pessoa(pessoa: Pessoa):
    """Criar nova pessoa"""
    
    # FastAPI automaticamente:
    # 1. Valida se os dados estão corretos
    # 2. Converte JSON para objeto Pessoa
    # 3. Verifica tipos (str, int, etc.)
    
    nova_pessoa = {
        "id": len(pessoas_db) + 1,
        "nome": pessoa.nome,
        "idade": pessoa.idade,
        "email": pessoa.email,
        "criado_em": datetime.now()
    }
    
    pessoas_db.append(nova_pessoa)
    
    return nova_pessoa

# PUT para atualizar
@app.put("/pessoa/{pessoa_id}")
def atualizar_pessoa(pessoa_id: int, pessoa: Pessoa):
    """Atualizar dados da pessoa"""
    for i, p in enumerate(pessoas_db):
        if p["id"] == pessoa_id:
            pessoas_db[i].update({
                "nome": pessoa.nome,
                "idade": pessoa.idade,
                "email": pessoa.email
            })
            return pessoas_db[i]
    
    raise HTTPException(status_code=404, detail="Pessoa não encontrada")

# DELETE
@app.delete("/pessoa/{pessoa_id}")
def deletar_pessoa(pessoa_id: int):
    """Deletar pessoa"""
    for i, pessoa in enumerate(pessoas_db):
        if pessoa["id"] == pessoa_id:
            pessoa_deletada = pessoas_db.pop(i)
            return {"mensagem": f"Pessoa {pessoa_deletada['nome']} deletada"}
    
    raise HTTPException(status_code=404, detail="Pessoa não encontrada")

# Para testar: python exemplo_fastapi.py
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando exemplo FastAPI em http://localhost:8061")
    print("📖 Documentação em: http://localhost:8061/docs")
    uvicorn.run(app, host="0.0.0.0", port=8061)