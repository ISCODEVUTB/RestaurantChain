from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from datetime import datetime

app = FastAPI()

MONGODB_URL = "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantChainDBy"
client = AsyncIOMotorClient(MONGODB_URL)
db = client["Restaurant"]
payment_methods = db["payment_methods"]

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API"}

def str_id(id):
    if isinstance(id, ObjectId):
        return str(id)
    return id

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Id Invalida")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: JsonSchemaValue, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string"}

class PaymentMethodCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class PaymentMethod(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class Config:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    schema_extra = {
        "example": {
            "name": "Tarjeta de crédito",
            "description": "Pago mediante tarjeta de crédito",
            "is_active": True,
            "created_at": "2024-04-28T12:00:00",
            "updated_at": "2024-04-28T12:00:00"
        }
    }

@app.post("/payment-methods", response_model=PaymentMethod)
async def create_payment_method(payment_method: PaymentMethodCreate):
    now = datetime.utcnow()
    payment_data = payment_method.dict()
    payment_data.update({"created_at": now, "updated_at": now})
    result = await payment_methods.insert_one(payment_data)
    created_payment = await payment_methods.find_one({"_id": result.inserted_id})
    return created_payment

@app.get("/payment-methods", response_model=List[PaymentMethod])
async def get_payment_methods():
    methods = await payment_methods.find().to_list(1000)
    return methods

@app.get("/payment-methods/{payment_method_id}", response_model=PaymentMethod)
async def get_payment_method(payment_method_id: str):
    method = await payment_methods.find_one({"_id": ObjectId(payment_method_id)})
    if not method:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")
    return method

@app.put("/payment-methods/{payment_method_id}", response_model=PaymentMethod)
async def update_payment_method(payment_method_id: str, updated_data: PaymentMethodCreate):
    updated = {
        "$set": {
            "name": updated_data.name,
            "description": updated_data.description,
            "is_active": updated_data.is_active,
            "updated_at": datetime.utcnow()
        }
    }
    result = await payment_methods.update_one(
        {"_id": ObjectId(payment_method_id)}, updated
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")
    method = await payment_methods.find_one({"_id": ObjectId(payment_method_id)})
    return method

@app.delete("/payment-methods/{payment_method_id}")
async def delete_payment_method(payment_method_id: str):
    result = await payment_methods.delete_one({"_id": ObjectId(payment_method_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")
    return {"message": "Metodo de pago eliminado"}