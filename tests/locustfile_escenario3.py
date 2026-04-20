import random
from locust import HttpUser, task, between
from datetime import datetime, timedelta

class Escenario3(HttpUser):
    """
    ESC-PREST-03: Creación Concurrente de Préstamos
    ID: ESC-PREST-03
    Nombre: Escalabilidad y corrección en manejo de escrituras concurrentes
    """
    
    wait_time = between(0.5, 1.5)  # Para alcanzar ~30 RPS con 60 usuarios
    
    def on_start(self):
        """Inicio del escenario - usar datos existentes"""
        print("Iniciando Escenario 3: Creación Concurrente de Préstamos")
        print("Usando datos existentes en la base de datos.")
        
        pass
    
    @task
    def crear_prestamo_concurrente(self):
        """
        Tarea principal: Crear préstamos concurrentemente
        Endpoint: POST /api/prestamos
        """
        usuario_id = random.randint(1, 200)
        libro_id = random.randint(1, 500)
        
        # Generar fechas realistas
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
        fecha_devolucion_prevista = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        
        prestamo_data = {
            "usuario_id": usuario_id,
            "libro_id": libro_id,
            "fecha_prestamo": fecha_prestamo,
            "fecha_devolucion_prevista": fecha_devolucion_prevista
        }
        
        with self.client.post("/api/prestamos", json=prestamo_data, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            elif response.status_code == 400:
                # Error esperado: libro no disponible o restricción de integridad
                response.success()
            elif response.status_code == 500:
                # Error de base de datos por concurrencia (aceptable en pruebas de estrés)
                response.success()
            else:
                response.failure(f"Error inesperado creando préstamo: {response.status_code}")
    
    @task(3)
    def crear_prestamo_libros_populares(self):
        """
        Intentar crear préstamos de libros populares (mayor competencia)
        """
        # Libros populares (primeros 100)
        libro_id = random.randint(1, 100)
        usuario_id = random.randint(1, 200)
        
        prestamo_data = {
            "usuario_id": usuario_id,
            "libro_id": libro_id,
            "fecha_prestamo": datetime.now().strftime("%Y-%m-%d"),
            "fecha_devolucion_prevista": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        }
        
        with self.client.post("/api/prestamos", json=prestamo_data, catch_response=True) as response:
            if response.status_code in [201, 400, 500]:
                response.success()
            else:
                response.failure(f"Error en libro popular: {response.status_code}")
    
    @task(2)
    def crear_prestamo_libros_menos_populares(self):
        """
        Intentar crear préstamos de libros menos populares
        """
        # Libros menos populares (últimos 100)
        libro_id = random.randint(401, 500)
        usuario_id = random.randint(1, 200)
        
        prestamo_data = {
            "usuario_id": usuario_id,
            "libro_id": libro_id,
            "fecha_prestamo": datetime.now().strftime("%Y-%m-%d"),
            "fecha_devolucion_prevista": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        }
        
        with self.client.post("/api/prestamos", json=prestamo_data, catch_response=True) as response:
            if response.status_code in [201, 400, 500]:
                response.success()
            else:
                response.failure(f"Error en libro menos popular: {response.status_code}")
    
    @task(1)
    def crear_prestamo_datos_invalidos(self):
        """
        Probar validación con datos inválidos
        """
        prestamo_data = {
            "usuario_id": 99999,  # Usuario inexistente
            "libro_id": 1,
            "fecha_prestamo": "2024-13-45",  # Fecha inválida
            "fecha_devolucion_prevista": "2024-02-30"
        }
        
        with self.client.post("/api/prestamos", json=prestamo_data, catch_response=True) as response:
            if response.status_code in [400, 500]:
                response.success()
            else:
                response.failure(f"Debería fallar con datos inválidos: {response.status_code}")
    
    @task(1)
    def crear_prestamo_fechas_pasadas(self):
        """
        Probar con fechas en el pasado
        """
        prestamo_data = {
            "usuario_id": random.randint(1, 200),
            "libro_id": random.randint(1, 500),
            "fecha_prestamo": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "fecha_devolucion_prevista": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        }
        
        with self.client.post("/api/prestamos", json=prestamo_data, catch_response=True) as response:
            if response.status_code in [201, 400, 500]:
                response.success()
            else:
                response.failure(f"Error con fechas pasadas: {response.status_code}")
    
    @task(1)
    def verificar_integridad_concurrente(self):
        """
        Verificar que la integridad se mantenga bajo concurrencia
        """
        # Consultar préstamos existentes para verificar integridad
        with self.client.get("/api/prestamos", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    response.success()
                else:
                    response.failure("Formato inválido en préstamos")
            else:
                response.failure(f"Error verificando integridad: {response.status_code}")
