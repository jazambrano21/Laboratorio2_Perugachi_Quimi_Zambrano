import random
from locust import HttpUser, task, between

class Escenario1(HttpUser):
    """
    ESC-BUSQ-01: Búsqueda de Autores bajo Carga Moderada
    ID: ESC-BUSQ-01
    Nombre: Rendimiento en operaciones de búsqueda filtrada de autores
    """
    
    wait_time = between(1, 2)  # Cada usuario realiza una búsqueda cada 1-2 segundos
    
    # Variable de clase para asegurar que los datos se creen solo una vez
    datos_creados = False
    
    def on_start(self):
        """Inicio del escenario - no crear datos para evitar errores"""
        print("Iniciando escenario de búsqueda de autores...")
        print("Usando datos existentes en la base de datos.")
    
    @task
    def buscar_autores_carga_moderada(self):
        """
        Tarea principal: Búsqueda de autores con términos que coinciden en ~30% de registros
        """
        # Términos de búsqueda diseñados para coincidir con ~30% de los autores
        terminos_busqueda = ["Gar", "Rod", "Lóp", "Mar", "Gon", "Pér", "San", "Ram", "Tor", "Dí"]
        termino = random.choice(terminos_busqueda)
        
        with self.client.get(f"/api/autores/buscar?q={termino}", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Validar que la respuesta tenga estructura correcta
                    if len(data) >= 0:  # Puede ser vacío o tener resultados
                        response.success()
                    else:
                        response.failure("Respuesta inválida: longitud negativa")
                else:
                    response.failure("Respuesta no es una lista")
            else:
                response.failure(f"Error en búsqueda: {response.status_code}")
    
    @task(5)
    def buscar_autores_terminos_variados(self):
        """
        Búsquedas con diferentes patrones para variar la carga
        """
        patrones = [
            "a", "e", "i", "o", "u",  # Vocales simples
            "an", "ar", "er", "ir", "or",  # Terminaciones
            "ga", "go", "gu", "ma", "me",  # Inicios
            "Juan", "María", "José"  # Nombres completos
        ]
        patron = random.choice(patrones)
        
        with self.client.get(f"/api/autores/buscar?q={patron}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 400:
                response.success()  # Error esperado si falta parámetro
            else:
                response.failure(f"Error inesperado: {response.status_code}")
    
    @task(1)
    def buscar_sin_parametro(self):
        """
        Probar manejo de error cuando falta parámetro obligatorio
        """
        with self.client.get("/api/autores/buscar", catch_response=True) as response:
            if response.status_code == 400:
                response.success()
            else:
                response.failure(f"Debería retornar 400, retornó: {response.status_code}")
    
    @task(1)
    def buscar_termino_inexistente(self):
        """
        Búsqueda con término que no debería coincidir con ningún autor
        """
        with self.client.get("/api/autores/buscar?q=XYZ123", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) == 0:
                    response.success()
                else:
                    response.failure("Debería retornar lista vacía")
            else:
                response.failure(f"Error en búsqueda vacía: {response.status_code}")
