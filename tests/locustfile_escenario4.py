import random
from locust import HttpUser, task, between
from datetime import datetime, timedelta

class Escenario4(HttpUser):
    """
    ESC-INTEGR-04: Integración de Operaciones Mixtas bajo Carga Máxima
    ID: ESC-INTEGR-04
    Nombre: Comportamiento del sistema con operaciones simultáneas de lectura y escritura
    """
    
    wait_time = between(0.1, 0.8)  # Espera mínima para máxima carga
    
    def on_start(self):
        """Precargar dataset grande: 1000 usuarios, 2000 libros, 5000 préstamos"""
        print("Iniciando precarga de datos para escenario de integración...")
        
        # Crear 1000 usuarios
        for i in range(1, 1001):
            usuario_data = {
                "nombre": f"Usuario{i:04d}",
                "apellido": f"Test{i:04d}",
                "correo": f"usuario{i:04d}@biblioteca.edu",
                "tipo_usuario": random.choice(["lector", "lector", "lector", "bibliotecario"])
            }
            self.client.post("/api/usuarios", json=usuario_data)
        
        # Crear autores variados
        autores_variados = [
            ("Fyodor", "Dostoevsky"), ("Leo", "Tolstoy"), ("Victor", "Hugo"),
            ("Homer", "Simpson"), ("Ernest", "Hemingway"), ("Virginia", "Woolf"),
            ("James", "Joyce"), ("Marcel", "Proust"), ("Franz", "Kafka"),
            ("Jorge", "Borges"), ("Pablo", "Neruda"), ("Gabriel", "Márquez"),
            ("William", "Shakespeare"), ("Jane", "Austen"), ("Charles", "Dickens"),
            ("George", "Orwell"), ("Aldous", "Huxley"), ("Ray", "Bradbury"),
            ("Isaac", "Asimov"), ("Arthur", "Clarke"), ("Robert", "Heinlein")
        ]
        
        for nombre, apellido in autores_variados:
            autor_data = {
                "nombre": nombre,
                "apellido": apellido,
                "fecha_nacimiento": f"{random.randint(1800, 1950)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "nacionalidad": random.choice(["Estadounidense", "Británico", "Ruso", "Francés", "Chileno", "Colombiano", "Argentino"]),
                "correo_electronico": f"{nombre.lower()}.{apellido.lower()}@literatura.com"
            }
            self.client.post("/api/autores", json=autor_data)
        
        # Crear 2000 libros
        titulos_variados = [
            "Cien Años de Soledad", "Don Quijote", "La Odisea", "1984", "Ulises",
            "El Principito", "El Señor de los Anillos", "Crimen y Castigo",
            "Guerra y Paz", "Los Miserables", "Orgullo y Prejuicio", "Hamlet",
            "Un Mundo Feliz", "Fahrenheit 451", "Fundación", "2001: Una Odisea Espacial",
            "Tétralogía", "El Extranjero", "El Proceso", "La Metamorfosis",
            "El Aleph", "Rayuela", "Sobre Héroes y Tumbas", "El Túnel"
        ]
        
        for i in range(1, 2001):
            libro_data = {
                "titulo": f"{random.choice(titulos_variados)} #{i}",
                "isbn": f"978-{random.randint(1000000000, 9999999999)}",
                "anio_publicacion": random.randint(1900, 2023),
                "edicion": f"{random.choice(['Primera', 'Segunda', 'Tercera', 'Cuarta', 'Quinta'])} Edición",
                "autor_id": random.randint(1, len(autores_variados))
            }
            self.client.post("/api/libros", json=libro_data)
        
        # Crear 5000 préstamos históricos
        for i in range(5000):
            usuario_id = random.randint(1, 1000)
            libro_id = random.randint(1, 2000)
            
            # Generar fechas distribuidas en los últimos 2 años
            dias_atras = random.randint(1, 730)
            fecha_prestamo = datetime.now() - timedelta(days=dias_atras)
            fecha_devolucion_prevista = fecha_prestamo + timedelta(days=15)
            
            # 70% históricos (devueltos), 30% activos
            if random.random() < 0.7:
                # Histórico
                dias_prestamo = random.randint(1, 30)
                fecha_devolucion_real = fecha_prestamo + timedelta(days=dias_prestamo)
                prestamo_data = {
                    "usuario_id": usuario_id,
                    "libro_id": libro_id,
                    "fecha_prestamo": fecha_prestamo.strftime("%Y-%m-%d"),
                    "fecha_devolucion_prevista": fecha_devolucion_prevista.strftime("%Y-%m-%d"),
                    "fecha_devolucion_real": fecha_devolucion_real.strftime("%Y-%m-%d")
                }
            else:
                # Activo
                prestamo_data = {
                    "usuario_id": usuario_id,
                    "libro_id": libro_id,
                    "fecha_prestamo": fecha_prestamo.strftime("%Y-%m-%d"),
                    "fecha_devolucion_prevista": fecha_devolucion_prevista.strftime("%Y-%m-%d")
                }
            
            self.client.post("/api/prestamos", json=prestamo_data)
        
        print("Precarga de datos completada.")
    
    @task(8)
    def busqueda_autores_intensiva(self):
        """
        Búsquedas intensivas de autores durante carga máxima
        """
        patrones_busqueda = [
            "a", "e", "i", "o", "u",  # Vocales
            "an", "ar", "er", "ir", "or",  # Terminaciones
            "ga", "go", "gu", "ma", "me",  # Inicios
            "ez", "is", "ov", "sky", "man",  # Patrones comunes
            "dostoevsky", "borges", "neruda", "shakespeare"  # Nombres completos
        ]
        patron = random.choice(patrones_busqueda)
        
        with self.client.get(f"/api/autores/buscar?q={patron}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 400:
                response.success()
            else:
                response.failure(f"Error búsqueda intensiva: {response.status_code}")
    
    @task(7)
    def consulta_prestamos_usuario_masiva(self):
        """
        Consultas masivas de préstamos por usuario
        """
        usuario_id = random.randint(1, 1000)
        
        with self.client.get(f"/api/usuarios/{usuario_id}/prestamos", catch_response=True) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Error consulta masiva: {response.status_code}")
    
    @task(6)
    def creacion_prestamos_concurrente_maxima(self):
        """
        Creación de préstamos bajo carga máxima concurrente
        """
        usuario_id = random.randint(1, 1000)
        libro_id = random.randint(1, 2000)
        
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
                response.failure(f"Error creación concurrente: {response.status_code}")
    
    @task(5)
    def obtener_todos_autores_carga_maxima(self):
        """
        Obtener lista completa de autores bajo carga máxima
        """
        with self.client.get("/api/autores", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    response.success()
                else:
                    response.failure("Formato inválido en autores")
            else:
                response.failure(f"Error obteniendo autores: {response.status_code}")
    
    @task(5)
    def obtener_todos_prestamos_carga_maxima(self):
        """
        Obtener lista completa de préstamos bajo carga máxima
        """
        with self.client.get("/api/prestamos", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    response.success()
                else:
                    response.failure("Formato inválido en préstamos")
            else:
                response.failure(f"Error obteniendo préstamos: {response.status_code}")
    
    @task(4)
    def creacion_usuarios_durante_carga(self):
        """
        Crear usuarios durante carga máxima
        """
        usuario_data = {
            "nombre": f"Load{random.randint(10000, 99999)}",
            "apellido": f"Test{random.randint(10000, 99999)}",
            "correo": f"loadtest{random.randint(10000, 99999)}@biblioteca.edu",
            "tipo_usuario": random.choice(["lector", "bibliotecario"])
        }
        
        with self.client.post("/api/usuarios", json=usuario_data, catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Error creando usuario: {response.status_code}")
    
    @task(3)
    def creacion_libros_durante_carga(self):
        """
        Crear libros durante carga máxima
        """
        libro_data = {
            "titulo": f"Load Test Book {random.randint(10000, 99999)}",
            "isbn": f"978-{random.randint(1000000000, 9999999999)}",
            "anio_publicacion": random.randint(2020, 2024),
            "edicion": "Load Test Edition",
            "autor_id": random.randint(1, 20)
        }
        
        with self.client.post("/api/libros", json=libro_data, catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Error creando libro: {response.status_code}")
    
    @task(2)
    def operacion_mixta_aleatoria(self):
        """
        Operación mixta aleatoria para simular comportamiento real
        """
        operaciones = [
            lambda: self.client.get("/api/autores"),
            lambda: self.client.get("/api/libros"),
            lambda: self.client.get("/api/prestamos"),
            lambda: self.client.get(f"/api/autores/buscar?q={random.choice(['a', 'e', 'i'])}"),
            lambda: self.client.get(f"/api/usuarios/{random.randint(1, 1000)}/prestamos"),
            lambda: self.client.post("/api/usuarios", json={
                "nombre": f"Mixed{random.randint(1000, 9999)}",
                "apellido": "Test",
                "correo": f"mixed{random.randint(1000, 9999)}@test.com",
                "tipo_usuario": "lector"
            })
        ]
        
        operacion = random.choice(operaciones)
        
        with operacion() as response:
            if response.status_code in [200, 201, 404]:
                response.success()
            else:
                response.failure(f"Error operación mixta: {response.status_code}")
    
    @task(1)
    def stress_parametros_invalidos(self):
        """
        Enviar parámetros inválidos durante estrés máximo
        """
        endpoints_invalidos = [
            "/api/autores/buscar",
            "/api/autores/buscar?q=",
            "/api/autores/buscar?q=   ",
            "/api/usuarios/99999/prestamos"
        ]
        
        endpoint = random.choice(endpoints_invalidos)
        
        with self.client.get(endpoint, catch_response=True) as response:
            if response.status_code in [400, 404]:
                response.success()
            else:
                response.failure(f"Error en parámetros inválidos: {response.status_code}")
    
    @task(1)
    def verificar_integridad_final(self):
        """
        Verificación periódica de integridad de datos
        """
        # Verificar que las relaciones se mantengan consistentes
        with self.client.get("/api/prestamos", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Validar estructura básica
                    for prestamo in data[:10]:  # Solo verificar primeros 10 para no sobrecargar
                        if not all(key in prestamo for key in ['id', 'usuario_id', 'libro_id']):
                            response.failure("Estructura de préstamo inválida")
                            return
                    response.success()
                else:
                    response.failure("Formato inválido en verificación")
            else:
                response.failure(f"Error en verificación de integridad: {response.status_code}")
