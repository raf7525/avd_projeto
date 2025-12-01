from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Optional
from datetime import datetime, timedelta
import json
import sys
import os
import pandas as pd
from pydantic import BaseModel
from app.services.storage_service import StorageService
from app.services.database import get_db_connection

router = APIRouter()
storage_service = StorageService()

class ThermalDataInput(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    wind_velocity: float
    pressure: float
    solar_radiation: float

class ThermalDataOutput(BaseModel):
    id: int
    timestamp: datetime
    temperature: float
    humidity: float
    wind_velocity: float
    pressure: float
    solar_radiation: float
    thermal_sensation: float
    comfort_zone: str
    created_at: datetime

class ThermalDataBatch(BaseModel):
    data: List[ThermalDataInput]

class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict = None

thermal_data_storage: List[dict] = []

@router.post("/", response_model=APIResponse)
async def create_thermal_data(thermal_data: ThermalDataInput):
    try:
        new_id = len(thermal_data_storage) + 1
        
        data_dict = thermal_data.dict()
        
        thermal_sensation = calculate_thermal_sensation(
            thermal_data.temperature,
            thermal_data.humidity, 
            thermal_data.wind_velocity,
            thermal_data.pressure,
            thermal_data.solar_radiation
        )
        
        comfort_zone = get_comfort_zone(thermal_sensation)
        
        data_dict.update({
            "id": new_id,
            "created_at": datetime.now(),
            "thermal_sensation": thermal_sensation,
            "comfort_zone": comfort_zone
        })
        
        # Save to In-Memory Storage
        thermal_data_storage.append(data_dict)

        # Save to MinIO (S3)
        try:
            s3_path = storage_service.save_json(data_dict)
            data_dict["s3_path"] = s3_path
        except Exception as e:
            print(f"Failed to save to S3: {e}")

        # Save to PostgreSQL
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO thermal_measurements 
                    (timestamp, temperature, humidity, wind_velocity, pressure, solar_radiation, thermal_sensation, comfort_zone, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        data_dict["timestamp"],
                        data_dict["temperature"],
                        data_dict["humidity"],
                        data_dict["wind_velocity"],
                        data_dict["pressure"],
                        data_dict["solar_radiation"],
                        data_dict["thermal_sensation"],
                        data_dict["comfort_zone"],
                        data_dict["created_at"]
                    )
                )
                db_id = cur.fetchone()['id']
                data_dict["db_id"] = db_id
                conn.commit()
                cur.close()
                conn.close()
        except Exception as e:
            print(f"Failed to save to DB: {e}")
        
        return APIResponse(
            success=True,
            message="Dados térmicos criados com sucesso",
            data=data_dict
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=APIResponse)
async def create_thermal_data_batch(batch_data: ThermalDataBatch):
    try:
        created_records = []
        
        for thermal_data in batch_data.data:
            new_id = len(thermal_data_storage) + 1
            
            data_dict = thermal_data.dict()
            
            thermal_sensation = calculate_thermal_sensation(
                thermal_data.temperature,
                thermal_data.humidity,
                thermal_data.wind_velocity, 
                thermal_data.pressure,
                thermal_data.solar_radiation
            )
            
            comfort_zone = get_comfort_zone(thermal_sensation)
            
            data_dict.update({
                "id": new_id,
                "created_at": datetime.now(),
                "thermal_sensation": thermal_sensation,
                "comfort_zone": comfort_zone
            })
            
            thermal_data_storage.append(data_dict)
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
async def get_thermal_data(
    limit: int = Query(default=100, description="Número máximo de registros"),
    offset: int = Query(default=0, description="Número de registros para pular"),
    start_date: Optional[datetime] = Query(default=None, description="Data inicial"),
    end_date: Optional[datetime] = Query(default=None, description="Data final"),
    min_temp: Optional[float] = Query(default=None, description="Temperatura mínima"),
    max_temp: Optional[float] = Query(default=None, description="Temperatura máxima"),
    comfort_zone: Optional[str] = Query(default=None, description="Zona de conforto")
):
    try:
        filtered_data = thermal_data_storage.copy()
        
        if start_date or end_date:
            filtered_data = [
                record for record in filtered_data
                if (not start_date or record["timestamp"] >= start_date) and
                   (not end_date or record["timestamp"] <= end_date)
            ]
        
        if min_temp is not None:
            filtered_data = [
                record for record in filtered_data
                if record["temperature"] >= min_temp
            ]
            
        if max_temp is not None:
            filtered_data = [
                record for record in filtered_data
                if record["temperature"] <= max_temp
            ]
            
        if comfort_zone:
            filtered_data = [
                record for record in filtered_data
                if record["comfort_zone"].lower() == comfort_zone.lower()
            ]
        
        total_records = len(filtered_data)
        paginated_data = filtered_data[offset:offset + limit]
        
        return APIResponse(
            success=True,
            message="Dados recuperados com sucesso",
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

@router.get("/{thermal_id}", response_model=APIResponse)
async def get_thermal_data_by_id(thermal_id: int):
    try:
        record = next((r for r in thermal_data_storage if r["id"] == thermal_id), None)
        
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

@router.delete("/{thermal_id}", response_model=APIResponse)
async def delete_thermal_data(thermal_id: int):
    try:
        record_index = None
        for i, record in enumerate(thermal_data_storage):
            if record["id"] == thermal_id:
                record_index = i
                break
        
        if record_index is None:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        
        deleted_record = thermal_data_storage.pop(record_index)
        
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
async def get_thermal_stats():
    try:
        if not thermal_data_storage:
            return APIResponse(
                success=True,
                message="Nenhum dado disponível",
                data={
                    "total_records": 0,
                    "stats": None
                }
            )
        
        temperatures = [record["temperature"] for record in thermal_data_storage]
        thermal_sensations = [record["thermal_sensation"] for record in thermal_data_storage]
        humidities = [record["humidity"] for record in thermal_data_storage]
        
        stats = {
            "total_records": len(thermal_data_storage),
            "temperature": {
                "min": min(temperatures),
                "max": max(temperatures),
                "avg": sum(temperatures) / len(temperatures),
                "count": len(temperatures)
            },
            "thermal_sensation": {
                "min": min(thermal_sensations),
                "max": max(thermal_sensations),
                "avg": sum(thermal_sensations) / len(thermal_sensations)
            },
            "humidity": {
                "min": min(humidities),
                "max": max(humidities),
                "avg": sum(humidities) / len(humidities)
            },
            "comfort_zones": {
                zone: len([r for r in thermal_data_storage if r["comfort_zone"] == zone])
                for zone in set(record["comfort_zone"] for record in thermal_data_storage)
            }
        }
        
        return APIResponse(
            success=True,
            message="Estatísticas calculadas com sucesso",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-comfort")
async def predict_thermal_comfort(data: List[ThermalDataInput]):
    try:
        predictions = []
        
        for item in data:
            thermal_sensation = calculate_thermal_sensation(
                item.temperature,
                item.humidity,
                item.wind_velocity,
                item.pressure,
                item.solar_radiation
            )
            
            comfort_zone = get_comfort_zone(thermal_sensation)
            
            predictions.append({
                "timestamp": item.timestamp,
                "predicted_thermal_sensation": thermal_sensation,
                "predicted_comfort_zone": comfort_zone,
                "input_data": item.dict()
            })
        
        return APIResponse(
            success=True,
            message=f"{len(predictions)} previsões calculadas",
            data={"predictions": predictions}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_thermal_sensation(temp, humidity, wind_speed, pressure=None, solar_radiation=None):
    import math
    
    if temp < 27:
        if wind_speed > 1.79:
            wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind_speed * 3.6)**0.16 + 0.3965 * temp * (wind_speed * 3.6)**0.16
            return round(wind_chill, 2)
        return round(temp, 2)
    
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 0.002211732
    c8 = 0.00072546
    c9 = -0.000003582
    
    heat_index = (c1 + (c2 * temp) + (c3 * humidity) + 
                 (c4 * temp * humidity) + (c5 * temp**2) + 
                 (c6 * humidity**2) + (c7 * temp**2 * humidity) + 
                 (c8 * temp * humidity**2) + (c9 * temp**2 * humidity**2))
    
    if wind_speed > 0:
        wind_factor = 1 - (wind_speed * 0.05)
        wind_factor = max(wind_factor, 0.7)
        heat_index *= wind_factor
    
    if solar_radiation is not None and solar_radiation > 200:
        solar_factor = 1 + (solar_radiation - 200) / 2000
        heat_index *= solar_factor
    
    return round(heat_index, 2)

def get_comfort_zone(thermal_sensation):
    if thermal_sensation < 16:
        return "Frio"
    elif thermal_sensation < 20:
        return "Fresco" 
    elif thermal_sensation < 26:
        return "Confortável"
    elif thermal_sensation < 30:
        return "Quente"
    else:
        return "Muito Quente"