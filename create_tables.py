from empleado_crud.models_sqlalchemy import Base, engine
from empleado_crud.models_sqlalchemy.employee import Employee, DailyHours, Position, PTOStatus
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from django.contrib.auth.models import User

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear una nueva sesión
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Insertar datos en la tabla Position
    new_position1 = Position(id_posicion=1, tipo_posicion="Jefe")
    new_position2 = Position(id_posicion=2, tipo_posicion="Empleado")

    # Agregar las posiciones a la sesión
    session.add(new_position1)
    session.add(new_position2)

    # Realizar el commit para guardar los cambios
    session.commit()

    new_status_pto1 = PTOStatus(id_pto=1, estado_pto="Rechazado")
    new_status_pto2 = PTOStatus(id_pto=2, estado_pto="Pendiente")
    new_status_pto3 = PTOStatus(id_pto=3, estado_pto="Aprobado")

    session.add(new_status_pto1)
    session.add(new_status_pto2)
    session.add(new_status_pto3)

    # Realizar el commit para guardar los cambios
    session.commit()

    # Insertar empleados
    new_employee1 = Employee(nombres="Devy", apellidos="Salomon", correo="devysalomon@gmail.com", id_posicion=1, dias_pto_disponibles=5)
    new_employee2 = Employee(nombres="Jared", apellidos="Rondon", correo="jaredrondon@gmail.com", id_posicion=1, dias_pto_disponibles=5)

    session.add(new_employee1)
    session.add(new_employee2)

    session.commit()

    # Insertar registros de horas
    new_hour1 = DailyHours(
        id_empleado=new_employee1.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-07T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-07T17:30:00")
    )
    new_hour1.total_horas = (new_hour1.hora_salida - new_hour1.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour2 = DailyHours(
        id_empleado=new_employee2.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-07T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-07T17:30:00")
    )
    new_hour2.total_horas = (new_hour2.hora_salida - new_hour2.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour3 = DailyHours(
        id_empleado=new_employee1.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-08T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-08T17:30:00")
    )
    new_hour3.total_horas = (new_hour3.hora_salida - new_hour3.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour4 = DailyHours(
        id_empleado=new_employee2.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-08T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-08T21:30:00")
    )
    new_hour4.total_horas = (new_hour4.hora_salida - new_hour4.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour5 = DailyHours(
        id_empleado=new_employee1.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-09T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-09T17:30:00")
    )
    new_hour5.total_horas = (new_hour5.hora_salida - new_hour5.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour6 = DailyHours(
        id_empleado=new_employee2.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-09T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-09T21:30:00")
    )
    new_hour6.total_horas = (new_hour6.hora_salida - new_hour6.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour7 = DailyHours(
        id_empleado=new_employee1.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-12T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-12T17:30:00")
    )
    new_hour7.total_horas = (new_hour7.hora_salida - new_hour7.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    new_hour8 = DailyHours(
        id_empleado=new_employee2.id_empleado,
        hora_ingreso=datetime.fromisoformat("2024-10-12T09:00:00"),
        hora_salida=datetime.fromisoformat("2024-10-12T17:30:00")
    )
    new_hour8.total_horas = (new_hour8.hora_salida - new_hour8.hora_ingreso).total_seconds() / 3600  # Calcular total_horas en horas

    # Agregar los registros de horas a la sesión
    session.add(new_hour1)
    session.add(new_hour2)
    session.add(new_hour3)
    session.add(new_hour4)
    session.add(new_hour5)
    session.add(new_hour6)
    session.add(new_hour7)
    session.add(new_hour8)

    # Hacer commit de los registros de horas
    session.commit()
    print("Tablas creadas y datos insertados correctamente.")
except Exception as e:
    # En caso de error, hacer rollback
    session.rollback()
    print(f"Error al insertar datos: {e}")
finally:
    # Cerrar la sesión
    session.close()
