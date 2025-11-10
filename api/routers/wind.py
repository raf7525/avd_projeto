"""
Wind Data Router
===============

Endpoints para gerenciamento de dados de vento.
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Optional
from datetime import datetime, timedelta
import json

from api.models.schemas import (
    WindDataInput, WindDataOutput, WindDataBatch, 
    APIResponse
)

router = APIRouter()

# Simulação de dados (em produção seria banco de dados)
wind_data_storage: List[dict] = []

@router.post("/", response_model=APIResponse)
async def create_wind_data(wind_data: WindDataInput):
    """
    📊 **Criar novo registro de dados de vento**
    
    Adiciona uma nova medição de vento ao sistema.
    """
    try:
        # Simular ID incremental
        new_id = len(wind_data_storage) + 1
        
        # Converter para dicionário e adicionar campos extras
        data_dict = wind_data.dict()
        data_dict.update({
            "id": new_id,
            "created_at": datetime.now(),
            "direction_cardinal": degrees_to_cardinal(wind_data.direction)
        })
        
        # Armazenar dados
        wind_data_storage.append(data_dict)
        
        return APIResponse(
            success=True,
            message="Dados de vento criados com sucesso",
            data=data_dict
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=APIResponse)
async def create_wind_data_batch(batch_data: WindDataBatch):
    """
    📊 **Criar múltiplos registros de vento em lote**
    
    Permite inserção eficiente de muitas medições.
    """
    try:
        created_records = []
        
        for wind_data in batch_data.data:
            new_id = len(wind_data_storage) + 1
            
            data_dict = wind_data.dict()
            data_dict.update({
                "id": new_id,
                "created_at": datetime.now(),
                "direction_cardinal": degrees_to_cardinal(wind_data.direction)
            })
            
            wind_data_storage.append(data_dict)
            created_records.append(data_dict)
        
        return APIResponse(
            success=True,
            message=f"{len(created_records)} registros criados com sucesso",
            data={
                "created_count": len(created_records),
                "records": created_records
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=APIResponse)
async def get_wind_data(
    limit: int = Query(default=100, description="Número máximo de registros"),
    offset: int = Query(default=0, description="Número de registros para pular"),
    start_date: Optional[datetime] = Query(default=None, description="Data inicial"),
    end_date: Optional[datetime] = Query(default=None, description="Data final"),
    min_velocity: Optional[float] = Query(default=None, description="Velocidade mínima"),
    max_velocity: Optional[float] = Query(default=None, description="Velocidade máxima")
):
    """
    📋 **Listar dados de vento com filtros**
    
    Recupera dados de vento com opções de filtragem e paginação.
    """
    try:
        # Aplicar filtros
        filtered_data = wind_data_storage.copy()
        
        # Filtro por data
        if start_date or end_date:
            filtered_data = [
                record for record in filtered_data
                if (not start_date or record["timestamp"] >= start_date) and
                   (not end_date or record["timestamp"] <= end_date)
            ]
        
        # Filtro por velocidade
        if min_velocity is not None:
            filtered_data = [
                record for record in filtered_data
                if record["velocity"] >= min_velocity
            ]
            
        if max_velocity is not None:
            filtered_data = [
                record for record in filtered_data
                if record["velocity"] <= max_velocity
            ]
        
        # Aplicar paginação
        total_records = len(filtered_data)
        paginated_data = filtered_data[offset:offset + limit]
        
        return APIResponse(
            success=True,
            message=f"Dados recuperados com sucesso",
            data={
                "records": paginated_data,
                "pagination": {
                    "total": total_records,
                    "limit": limit,
                    "offset": offset,
                    "has_next": offset + limit < total_records
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{wind_id}", response_model=APIResponse)
async def get_wind_data_by_id(wind_id: int):
    """
    🔍 **Obter dados de vento por ID**
    
    Recupera um registro específico de dados de vento.
    """
    try:
        # Buscar registro por ID
        record = next((r for r in wind_data_storage if r["id"] == wind_id), None)
        
        if not record:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        return APIResponse(
            success=True,
            message="Registro encontrado",
            data=record
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{wind_id}", response_model=APIResponse)
async def delete_wind_data(wind_id: int):
    """
    🗑️ **Deletar dados de vento**
    
    Remove um registro específico de dados de vento.
    """
    try:
        # Buscar índice do registro
        record_index = None
        for i, record in enumerate(wind_data_storage):
            if record["id"] == wind_id:
                record_index = i
                break
        
        if record_index is None:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        # Remover registro
        deleted_record = wind_data_storage.pop(record_index)
        
        return APIResponse(
            success=True,
            message="Registro deletado com sucesso",
            data=deleted_record
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary", response_model=APIResponse)
async def get_wind_stats():
    """
    📊 **Estatísticas resumidas dos dados de vento**
    
    Retorna métricas estatísticas dos dados armazenados.
    """
    try:
        if not wind_data_storage:
            return APIResponse(
                success=True,
                message="Nenhum dado disponível",
                data={
                    "total_records": 0,
                    "stats": None
                }
            )
        
        velocities = [record["velocity"] for record in wind_data_storage]
        directions = [record["direction"] for record in wind_data_storage]
        
        stats = {
            "total_records": len(wind_data_storage),
            "velocity": {
                "min": min(velocities),
                "max": max(velocities),
                "avg": sum(velocities) / len(velocities),
                "count": len(velocities)
            },
            "direction": {
                "min": min(directions),
                "max": max(directions),
                "avg": sum(directions) / len(directions)
            },
            "time_range": {
                "start": min(record["timestamp"] for record in wind_data_storage),
                "end": max(record["timestamp"] for record in wind_data_storage)
            }
        }
        
        return APIResponse(
            success=True,
            message="Estatísticas calculadas com sucesso",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Funções auxiliares
def degrees_to_cardinal(degrees: float) -> str:
    """Converter graus para direção cardinal."""
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    
    # Normalizar graus para 0-360
    degrees = degrees % 360
    
    # Calcular índice (16 direções, cada uma com 22.5 graus)
    index = int((degrees + 11.25) // 22.5)
    
    return directions[index % 16]