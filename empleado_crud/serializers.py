from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date  # Asegúrate de importar datetime


class EmployeePydanticModel(BaseModel):
    nombres: str
    apellidos: str
    correo: str
    id_posicion: int  # Cambiamos 'posicion' a 'id_posicion' para reflejar el nuevo modelo

    class Config:
        orm_mode = True

class HoursPydanticModel(BaseModel):
    id_empleado: int  # Se debe agregar el tipo de dato aquí
    hora_ingreso: datetime
    hora_salida: datetime

    class Config:
        orm_mode = True


class PTOPydanticViewModel(BaseModel):
    nombres: str
    apellidos: str
    hora_inicio_pto: date
    hora_final_pto: date
    numero_dias: int
    aprobado: str

class PTOPydanticModel(BaseModel):
    id_empleado: int
    hora_inicio_pto: datetime
    hora_final_pto: datetime

class PTOPydanticUpdateModel(BaseModel):
    aprobado: int