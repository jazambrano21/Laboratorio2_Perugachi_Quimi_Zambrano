import random
from locust import HttpUser, task, between
from datetime import datetime, timedelta

class Escenario2(HttpUser):
    """
    ESC-PREST-02: Consulta de Préstamos por Usuario con Relaciones
    ID: ESC-PREST-02
    Nombre: Rendimiento en consulta de historial de préstamos con múltiples JOINs
    """
    
    wait_time = between(2, 4)  # Cada usuario realiza una consulta cada 2-4 segundos
    
    def on_start(self):
        """Inicio del escenario - usar datos existentes"""
        print("Iniciando Escenario 2: Consulta de Préstamos por Usuario")
        print("Usando datos existentes en la base de datos.")
        
        pass
    
    @task
    def consultar_prestamos_usuario(self):
        """
        Tarea principal: Consultar historial de préstamos de un usuario específico
        Endpoint: GET /api/usuarios/{id}/prestamos
        """
        # Seleccionar un usuario aleatorio del rango 1-200
        usuario_id = random.randint(1, 200)
        
        with self.client.get(f"/api/usuarios/{usuario_id}/prestamos", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Validar estructura de la respuesta
                    for prestamo in data:
                        if not all(key in prestamo for key in ['id', 'fecha_prestamo', 'titulo', 'isbn', 'anio_publicacion']):
                            response.failure("Estructura de préstamo inválida")
                            return
                    response.success()
                else:
                    response.failure("Respuesta no es una lista de préstamos")
            elif response.status_code == 404:
                # Usuario no encontrado - respuesta válida
                response.success()
            else:
                response.failure(f"Error consultando préstamos: {response.status_code}")
    
    @task(3)
    def consultar_usuarios_con_prestamos(self):
        """
        Consultar usuarios que probablemente tengan préstamos
        """
        # Usuarios más probables de tener préstamos (primeros 100)
        usuario_id = random.randint(1, 100)
        
        with self.client.get(f"/api/usuarios/{usuario_id}/prestamos", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    response.success()
                else:
                    response.failure("Formato inválido")
            elif response.status_code == 404:
                response.success()
            else:
                response.failure(f"Error en consulta: {response.status_code}")
    
    @task(2)
    def consultar_usuarios_sin_prestamos(self):
        """
        Consultar usuarios que probablemente no tengan préstamos
        """
        # Usuarios menos probables de tener préstamos (últimos 100)
        usuario_id = random.randint(101, 200)
        
        with self.client.get(f"/api/usuarios/{usuario_id}/prestamos", catch_response=True) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Error en consulta: {response.status_code}")
    
    @task(1)
    def consultar_usuario_inexistente(self):
        """
        Probar manejo de error con usuario que no existe
        """
        with self.client.get("/api/usuarios/99999/prestamos", catch_response=True) as response:
            if response.status_code == 404:
                response.success()
            else:
                response.failure(f"Debería retornar 404, retornó: {response.status_code}")
    
    @task(1)
    def validar_estructura_respuesta(self):
        """
        Validar que la respuesta contenga todos los campos requeridos
        """
        usuario_id = random.randint(1, 200)
        
        with self.client.get(f"/api/usuarios/{usuario_id}/prestamos", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    for prestamo in data:
                        campos_requeridos = ['id', 'fecha_prestamo', 'fecha_devolucion_prevista', 
                                          'fecha_devolucion_real', 'titulo', 'isbn', 'anio_publicacion']
                        if all(campo in prestamo for campo in campos_requeridos):
                            response.success()
                        else:
                            response.failure("Faltan campos requeridos en préstamo")
                            return
                else:
                    response.failure("Respuesta no es lista")
            else:
                response.failure(f"Error en validación: {response.status_code}")
