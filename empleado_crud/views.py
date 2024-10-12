from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models_sqlalchemy import SessionLocal
from .models_sqlalchemy.employee import Employee, DailyHours, PTO, PTOStatus
from .serializers import EmployeePydanticModel, HoursPydanticModel, PTOPydanticViewModel, PTOPydanticModel, PTOPydanticUpdateModel
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from pydantic import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Crear empleado
class EmployeeCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Creacion de empleados",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del empleado'),
                'apellidos': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del empleado'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo electrónico'),
                'id_posicion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tipo de empleado (1: Jefe, 2: Empleado)'),
            },
            required=['nombre', 'apellidos', 'correo', 'id_posicion'],
        ),

    )

    def post(self, request):
        session = SessionLocal()
        try:
            # Obtener los datos de la petición y asegurarnos de que sean un diccionario
            data = request.data

            # Validar los datos de la petición con Pydantic
            employee_data = EmployeePydanticModel.model_validate(data)

            # Crear una instancia de Employee con los datos validados
            new_employee = Employee(
                nombres=employee_data.nombres,
                apellidos=employee_data.apellidos,
                correo=employee_data.correo,
                id_posicion=employee_data.id_posicion,
            )

            # Guardar el nuevo empleado en la base de datos
            session.add(new_employee)
            session.commit()
            session.refresh(new_employee)

            # Serializar el nuevo empleado con Pydantic para devolverlo en la respuesta
            employee_serialized = EmployeePydanticModel.model_validate(new_employee.__dict__)

            return Response(employee_serialized.model_dump(), status=status.HTTP_201_CREATED)

        except Exception as e:
            session.rollback()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()


# Leer todos los empleados
class EmployeeListView(APIView):
    @swagger_auto_schema(
        operation_description="Visualizacion de empleados"
    )

    def get(self, request):
        session = SessionLocal()
        try:
            # Consultar todos los empleados
            employees = session.query(Employee).all()

            # Serializar los empleados usando Pydantic después de convertir a diccionario
            employees_serialized = [EmployeePydanticModel.model_validate(emp.__dict__).model_dump() for emp in employees]

            return Response(employees_serialized, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()


# Actualizar empleado
class EmployeeUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Actualiza la informacion de un empleado",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del empleado'),
                'apellidos': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del empleado'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo electrónico'),
                'id_posicion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tipo de empleado (1: Jefe, 2: Empleado)'),
            },

        ),
        responses={200: "Empleado actualizado", 400: "Error en la solicitud"}
    )


    def put(self, request, id_empleado):  # Cambia employee_id por id
        session = SessionLocal()
        try:
            # Obtener el empleado por ID
            employee = session.query(Employee).filter(Employee.id == id_empleado).first()  # Cambia employee_id por id

            if not employee:
                return Response({"error": "Empleado no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Crear un diccionario con los datos actuales del empleado y actualizar con los nuevos valores
            employee_data = {
                "id": employee.id,  # Incluir el id existente
                "nombres": request.data.get("nombres", employee.nombres),
                "apellidos": request.data.get("apellidos", employee.apellidos),
                "correo": request.data.get("correo", employee.correo),
                "posicion": request.data.get("posicion", employee.posicion),
                "horas_trabajadas": request.data.get("horas_trabajadas", employee.horas_trabajadas),
            }

            # Validar los datos proporcionados usando Pydantic (partial update)
            employee_validated = EmployeePydanticModel.model_validate(employee_data)

            # Actualizar el empleado
            employee.nombres = employee_validated.nombres
            employee.apellidos = employee_validated.apellidos
            employee.correo = employee_validated.correo
            employee.posicion = employee_validated.posicion
            employee.horas_trabajadas = employee_validated.horas_trabajadas

            session.commit()

            # Serializar los datos actualizados usando Pydantic
            employee_serialized = EmployeePydanticModel.model_validate(employee_validated)

            return Response(employee_serialized.model_dump(), status=status.HTTP_200_OK)
        except Exception as e:
            session.rollback()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()



# Eliminar empleado
class EmployeeDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Eliminacion de empleados"
    )


    def delete(self, request, id_empleado):
        session = SessionLocal()
        try:
            # Obtener el empleado por ID
            employee = session.query(Employee).filter(Employee.id == id_empleado).first()

            if not employee:
                return Response({"error": "Empleado no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Eliminar el empleado
            session.delete(employee)
            session.commit()

            return Response({"message": "Empleado eliminado exitosamente"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            session.rollback()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()


# Crear horas
class HoursCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Registra el dia y horas de ingreso y salida de un empleado",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_empleado': openapi.Schema(type=openapi.TYPE_STRING, description='ID del empleado'),
                'hora_ingreso': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de entrada'),
                'hora_salida': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de salida'),
            },
            required=['id_empleado', 'hora_ingreso', 'hora_salida'],
        ),
        responses={200: "Horario de trabajo registrado", 400: "Error en la solicitud"}
    )

    def post(self, request):
        session = SessionLocal()
        try:
            # Obtener los datos de la petición y asegurarnos de que sean un diccionario
            data = request.data

            # Validar los datos de la petición con Pydantic, excluyendo 'total_horas'
            hours_data = HoursPydanticModel.model_validate(data)

            # Calcular total_horas (diferencia entre hora_ingreso y hora_salida en horas)
            hora_ingreso = datetime.fromisoformat(hours_data.hora_ingreso.isoformat())
            hora_salida = datetime.fromisoformat(hours_data.hora_salida.isoformat())
            total_horas = (hora_salida - hora_ingreso).seconds // 3600

            #  # Verificar si total_horas es mayor a 8 horas
            # if total_horas > 8:
            #     return Response(
            #         {"error": "El total de horas trabajadas no puede ser mayor a 8 horas."},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )

            # Crear una instancia de DailyHours con los datos validados y el total de horas calculado
            new_hour = DailyHours(
                id_empleado=hours_data.id_empleado,
                hora_ingreso=hours_data.hora_ingreso,
                hora_salida=hours_data.hora_salida,
                total_horas=total_horas  # Asignar total_horas calculado
            )

            # Guardar el nuevo registro en la base de datos
            session.add(new_hour)
            session.commit()
            session.refresh(new_hour)

            # Serializar el nuevo registro con Pydantic para devolverlo en la respuesta
            hours_serialized = HoursPydanticModel.model_validate(new_hour.__dict__)

            return Response(hours_serialized.model_dump(), status=status.HTTP_201_CREATED)

        except Exception as e:
            session.rollback()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()

from sqlalchemy import func

# Reporte semanal de horas trabajadas por empleado (incluyendo horas extras)
class WeeklyReportView(APIView):
    @swagger_auto_schema(
        operation_description="Muestra el reporte semanal de horas laborales realizadas, indicando si se hicieron horas extras",
    )


    def get(self, request):
        session = SessionLocal()
        try:
            # Establecer la fecha actual
            today = datetime.now()

            # Calcular el inicio de la semana (lunes a las 00:00:00)
            start_of_week = today - timedelta(days=today.weekday())
            start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

            # Calcular el fin de la semana (domingo a las 23:59:59)
            end_of_week = start_of_week + timedelta(days=6)
            end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Consultar cada registro de horas trabajado por cada empleado en la semana
            report = (
                session.query(
                    Employee.nombres,
                    Employee.apellidos,
                    func.date(DailyHours.hora_ingreso).label("fecha"),  # Obtener solo la fecha de hora_ingreso
                    DailyHours.total_horas
                )
                .join(DailyHours, Employee.id_empleado == DailyHours.id_empleado)
                .filter(
                    DailyHours.hora_ingreso >= start_of_week,
                    DailyHours.hora_salida <= end_of_week
                )
                .order_by(func.date(DailyHours.hora_ingreso)) 
                .all()
            )

            # Serializar el reporte adecuadamente
            report_serialized = [
                {
                    "nombres": emp.nombres,
                    "apellidos": emp.apellidos,
                    "fecha": emp.fecha.strftime("%Y-%m-%d"),  # Formatear la fecha
                    "total_horas": emp.total_horas,
                    "horas_extras": "SI" if emp.total_horas > 8 else "NO"  # Verificar si hay horas extras
                }
                for emp in report
            ]

            return Response(report_serialized, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()


class PTOCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Registra el PTO para su aprobacion",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_empleado': openapi.Schema(type=openapi.TYPE_STRING, description='ID del empleado'),
                'hora_inicio_pto': openapi.Schema(type=openapi.TYPE_STRING, description='Dia de inicio'),
                'hora_final_pto': openapi.Schema(type=openapi.TYPE_STRING, description='Dia de final'),
            },
            required=['id_empleado', 'hora_inicio_pto', 'hora_final_pto'],
        ),
        responses={200: "PTO registrado", 400: "Error en la solicitud"}
    )

    def post(self, request):
        session = SessionLocal()
        try:
            # Obtener los datos de la petición
            data = request.data

            # Validar los datos de la petición con Pydantic
            pto_data = PTOPydanticModel.model_validate(data)

            # Obtener el empleado por ID
            empleado = session.query(Employee).filter_by(id_empleado=pto_data.id_empleado).first()

            if not empleado:
                return Response({"error": "Empleado no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Calcular el número de días basado en la diferencia entre hora_inicio_pto y hora_final_pto
            fecha_inicio = pto_data.hora_inicio_pto
            fecha_final = pto_data.hora_final_pto

            # Diferencia en días (incluyendo posibles fracciones de día)
            diferencia_dias = (fecha_final - fecha_inicio).days + 1  # Sumar 1 para incluir el día de inicio

            # Obtener el total de días de PTO aprobados previamente (aprobado = 3)
            pto_aprobado = session.query(PTO).filter_by(id_empleado=pto_data.id_empleado, aprobado=3).all()
            total_dias_aprobados = sum([pto.numero_dias for pto in pto_aprobado])

            # Verificar si el empleado tiene suficientes días disponibles, considerando los días aprobados previamente
            if empleado.dias_pto_disponibles < (total_dias_aprobados + diferencia_dias):
                return Response(
                    {"error": "El empleado no tiene suficientes días de PTO disponibles considerando los ya aprobados"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Actualizar los días disponibles del empleado
            empleado.dias_pto_disponibles -= diferencia_dias

            # Crear una instancia de PTO con los datos validados y el número de días calculado
            new_pto = PTO(
                id_empleado=pto_data.id_empleado,
                hora_inicio_pto=fecha_inicio,
                hora_final_pto=fecha_final,
                numero_dias=diferencia_dias,  # Usar la diferencia de días calculada
                aprobado=2  # Establecer el campo "aprobado" en 2
            )

            # Guardar el nuevo PTO y actualizar los días disponibles del empleado en la base de datos
            session.add(new_pto)
            session.commit()
            session.refresh(new_pto)

            # Serializar el nuevo PTO con Pydantic para devolverlo en la respuesta
            pto_serialized = PTOPydanticModel.model_validate(new_pto.__dict__)

            return Response(pto_serialized.model_dump(), status=status.HTTP_201_CREATED)

        except Exception as e:
            session.rollback()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()



class PTOListView(APIView):
    @swagger_auto_schema(
        operation_description="Muestra el reporte de PTO realizados",
    )

    def get(self, request):
        session = SessionLocal()
        try:
            # Consultar todos los PTOs y hacer joins con las tablas PTOStatus y Employee para obtener los nombres y apellidos
            ptos = (
                session.query(PTO)
                .join(PTOStatus, PTO.aprobado == PTOStatus.id_pto)
                .join(Employee, PTO.id_empleado == Employee.id_empleado)
                .all()
            )

            # Serializar los PTOs y reemplazar "aprobado" con el valor del estado, y "id_empleado" con "nombres" y "apellidos"
            ptos_serialized = []
            for pto in ptos:
                pto_data = pto.__dict__.copy()
                
                # Reemplazar el ID del estado por el valor del estado
                pto_data['aprobado'] = session.query(PTOStatus).filter_by(id_pto=pto.aprobado).first().estado_pto
                
                # Reemplazar el ID del empleado por los nombres y apellidos
                employee = session.query(Employee).filter_by(id_empleado=pto.id_empleado).first()
                pto_data['nombres'] = employee.nombres
                pto_data['apellidos'] = employee.apellidos
                del pto_data['id_empleado']  # Eliminar el campo id_empleado

                # Convertir hora_inicio_pto y hora_final_pto a solo fecha
                pto_data['hora_inicio_pto'] = pto.hora_inicio_pto.date()  # Extraer solo la fecha
                pto_data['hora_final_pto'] = pto.hora_final_pto.date()  # Extraer solo la fecha
                
                # Validar y serializar usando Pydantic
                serialized_pto = PTOPydanticViewModel.model_validate(pto_data).model_dump()
                ptos_serialized.append(serialized_pto)

            return Response(ptos_serialized, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()


# Actualizar PTO
class PTOUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Registra la aprobacion del PTO",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'aprobado': openapi.Schema(type=openapi.TYPE_INTEGER, description='Estado de aprobacion (1:Denegado, 2:Pendiente, 3:Aprobado)'),
            },
            required=['aprobado'],
        ),
        responses={200: "PTO registrado", 400: "Error en la solicitud"}
    )


    def put(self, request, id):
        session = SessionLocal()
        try:
            # Obtener el PTO por ID
            pto = session.query(PTO).filter(PTO.id == id).first()

            if not pto:
                return Response({"error": "PTO no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Obtener el campo "aprobado" del request
            aprobado = request.data.get("aprobado")

            # Validar el campo "aprobado" usando Pydantic
            if aprobado is not None:
                # Validar el dato con el serializer Pydantic
                pto_validated = PTOPydanticUpdateModel(aprobado=aprobado)

                # Actualizar el campo aprobado
                pto.aprobado = pto_validated.aprobado
                session.commit()

                # Serializar solo el campo que ha cambiado y devolver la respuesta
                return Response({"aprobado": pto.aprobado}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "El campo 'aprobado' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            session.rollback()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        finally:
            session.close()

