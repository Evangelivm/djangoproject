from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from . import Base

class Employee(Base):
    __tablename__ = "empleado"
    
    id_empleado = Column(Integer, primary_key=True, index=True)
    nombres = Column(String, nullable=False)  
    apellidos = Column(String, nullable=False) 
    correo = Column(String, nullable=False, unique=True) 
    id_posicion = Column(Integer, ForeignKey('posicion.id_posicion'), index=True)  
    dias_pto_disponibles = Column(Integer, nullable=False) 

class DailyHours(Base):  
    __tablename__ = "horas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_empleado = Column(Integer, ForeignKey('empleado.id_empleado'), index=True)  
    hora_ingreso = Column(DateTime, nullable=False) 
    hora_salida = Column(DateTime, nullable=False)   
    total_horas = Column(Integer, nullable=False)  

class Position(Base):
    __tablename__ = "posicion"
    
    id_posicion = Column(Integer, primary_key=True, index=True)
    tipo_posicion = Column(String, nullable=False) 

class PTOStatus(Base):  # Usar enum para el campo "aprobado"
    __tablename__ = "estado_pto"
    
    id_pto = Column(Integer, primary_key=True, index=True)
    estado_pto = Column(String, nullable=False) 

class PTO(Base):
    __tablename__ = "permisos"
    
    id = Column(Integer, primary_key=True, index=True)
    id_empleado = Column(Integer, ForeignKey('empleado.id_empleado'), index=True)
    hora_inicio_pto = Column(DateTime, nullable=False) 
    hora_final_pto = Column(DateTime, nullable=False) 
    numero_dias = Column(Integer, nullable=False)
    aprobado = Column(Integer, ForeignKey('estado_pto.id_pto'), index=True)
