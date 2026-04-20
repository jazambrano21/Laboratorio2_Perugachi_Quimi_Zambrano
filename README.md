# Sistema de Biblioteca - API REST

## Descripción del Proyecto

Sistema de gestión de biblioteca implementado con Node.js, Express y MySQL que permite la administración de autores, libros, usuarios y préstamos.

## Estrategia de Modelado de Datos

### Estrategia Elegida: Herencia en Base de Datos

Se ha implementado la estrategia de **herencia en base de datos** mediante una tabla única `usuario` con un campo discriminador `tipo_usuario`.

#### Justificación Técnica

**Ventajas:**

1. **Rendimiento Superior:**
   - Menos joins necesarios en consultas
   - Acceso directo a todos los datos del usuario en una sola tabla
   - Índices más eficientes al operar sobre una sola tabla

2. **Simplicidad de Mantenimiento:**
   - Menos complejidad en el esquema de base de datos
   - Migraciones más sencillas
   - Backup y restore más directos

3. **Escalabilidad Vertical:**
   - Fácil adición de nuevos tipos de usuario mediante valores en el campo discriminador
   - No requiere reestructuración de tablas para nuevos roles

**Desventajas:**

1. **Espacio de Almacenamiento:** Algunos campos pueden ser nulos para ciertos tipos de usuario
2. **Validación:** Requiere validación a nivel de aplicación para campos específicos de cada tipo

#### Atributos de Calidad Impactados

| Atributo | Impacto | Justificación |
|----------|---------|---------------|
| **Rendimiento** |  Positivo | Menos joins = consultas más rápidas |
| **Mantenibilidad** | Positivo | Esquema más simple y directo |
| **Escalabilidad** |  Positivo | Fácil adición de nuevos tipos |
| **Integridad** |  Neutro | Requiere validación adicional |

## Arquitectura del Sistema

```
src/
├── app.js              # Punto de entrada y configuración de Express
├── config/
│   └── db.js          # Configuración de conexión a MySQL
├── controllers/        # Lógica de negocio de los endpoints
│   ├── autorController.js
│   ├── libroController.js
│   ├── prestamoController.js
│   └── usuarioController.js
├── models/            # Acceso a datos y consultas SQL
│   ├── Autor.js
│   ├── Libro.js
│   ├── Prestamo.js
│   └── Usuario.js
└── routes/            # Definición de rutas HTTP
    ├── autorRoutes.js
    ├── libroRoutes.js
    ├── prestamoRoutes.js
    └── usuarioRoutes.js
```

## Configuración del Entorno de Desarrollo

### Prerrequisitos

- Node.js (v14 o superior)
- Docker y Docker Compose
- Locust (para pruebas de carga)

### Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone <repositorio>
   cd Laboratorio2_Perugachi_Quimi_Zambrano
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con las credenciales de la base de datos
   ```

4. **Levantar la base de datos con Docker:**
   ```bash
   docker-compose up -d
   ```

5. **Iniciar la aplicación:**
   ```bash
   # Desarrollo
   npm run dev
   
   # Producción
   npm start
   ```

La API estará disponible en `http://localhost:3000`

## Endpoints de la API

### Autores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/autores` | Obtener todos los autores |
| GET | `/api/autores/buscar?q=<texto>` | **[NUEVO]** Buscar autores por coincidencia parcial |
| POST | `/api/autores` | Crear nuevo autor |
| PUT | `/api/autores/:id` | Actualizar autor |
| DELETE | `/api/autores/:id` | Eliminar autor |

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/usuarios` | Obtener todos los usuarios |
| GET | `/api/usuarios/:id/prestamos` | **[NUEVO]** Obtener historial de préstamos de un usuario |
| POST | `/api/usuarios` | Crear nuevo usuario |
| PUT | `/api/usuarios/:id` | Actualizar usuario |

### Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/libros` | Obtener todos los libros |
| POST | `/api/libros` | Crear nuevo libro |
| PUT | `/api/libros/:id` | Actualizar libro |
| DELETE | `/api/libros/:id` | Eliminar libro |

### Préstamos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/prestamos` | Obtener todos los préstamos |
| POST | `/api/prestamos` | Crear nuevo préstamo |

## Ejemplos de Uso

### Búsqueda de Autores

```bash
# Buscar autores que contengan "gar" en nombre o apellido
curl -X GET "http://localhost:3000/api/autores/buscar?q=gar"

# Respuesta esperada (200):
[
  {
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García",
    "fecha_nacimiento": "1927-03-06",
    "nacionalidad": "Colombiana",
    "correo_electronico": "gabriel.garcia@ejemplo.com"
  }
]
```

```bash
# Error cuando falta parámetro (400):
curl -X GET "http://localhost:3000/api/autores/buscar"

# Respuesta esperada:
{
  "error": "El parámetro de búsqueda \"q\" es obligatorio"
}
```

### Consultar Préstamos de Usuario

```bash
# Obtener préstamos del usuario con ID 1
curl -X GET "http://localhost:3000/api/usuarios/1/prestamos"

# Respuesta esperada (200):
[
  {
    "id": 1,
    "fecha_prestamo": "2024-01-15",
    "fecha_devolucion_prevista": "2024-02-15",
    "fecha_devolucion_real": null,
    "titulo": "Cien Años de Soledad",
    "isbn": "978-0307474728",
    "anio_publicacion": 1967
  }
]
```

```bash
# Usuario no encontrado (404):
curl -X GET "http://localhost:3000/api/usuarios/99999/prestamos"

# Respuesta esperada:
{
  "error": "Usuario no encontrado"
}
```

### Crear Autor

```bash
curl -X POST "http://localhost:3000/api/autores" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Julio",
    "apellido": "Cortázar",
    "fecha_nacimiento": "1914-08-26",
    "nacionalidad": "Argentina",
    "correo_electronico": "julio.cortazar@ejemplo.com"
  }'
```

### Crear Préstamo

```bash
curl -X POST "http://localhost:3000/api/prestamos" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "libro_id": 1,
    "fecha_prestamo": "2024-01-15",
    "fecha_devolucion_prevista": "2024-02-15"
  }'
```

## Pruebas de Carga con Locust

### Ejecutar Pruebas

1. **Instalar Locust:**
   ```bash
   pip install locust
   ```

2. **Ejecutar escenario específico:**
   ```bash
   # Escenario 1: Operaciones básicas
   locust -f tests/locust_escenario_1.py --host=http://localhost:3000
   
   # Escenario 2: Búsqueda y préstamos
   locust -f tests/locust_escenario_2.py --host=http://localhost:3000
   
   # Escenario 3: Estrés concurrente
   locust -f tests/locust_escenario_3.py --host=http://localhost:3000
   
   # Escenario 4: Capacidad y escalabilidad
   locust -f tests/locust_escenario_4.py --host=http://localhost:3000
   ```

3. **Interfaz Web:**
   - Abrir `http://localhost:8089` en el navegador
   - Configurar número de usuarios y tasa de generación
   - Iniciar pruebas y monitorear resultados en tiempo real

### Descripción de Escenarios

- **Escenario 1:** Pruebas básicas de CRUD para todas las entidades
- **Escenario 2:** Enfoque en nuevos endpoints (búsqueda de autores, préstamos por usuario)
- **Escenario 3:** Pruebas de estrés con operaciones concurrentes
- **Escenario 4:** Pruebas de capacidad con pico de usuarios simultáneos

## Integridad Referencial

La base de datos implementa políticas `ON DELETE RESTRICT` para mantener la integridad:

- No se puede eliminar un autor si tiene libros asociados
- No se puede eliminar un libro si tiene préstamos activos
- No se puede eliminar un usuario si tiene préstamos registrados

## Tecnologías Utilizadas

- **Backend:** Node.js, Express.js
- **Base de Datos:** MySQL 8.0
- **Contenerización:** Docker, Docker Compose
- **Pruebas de Carga:** Locust
- **Gestión de Paquetes:** npm

## Estructura de Datos

### Tablas Principales

- **autor:** Información de autores
- **libro:** Catálogo de libros con relación a autores
- **usuario:** Usuarios del sistema (lectores/bibliotecarios)
- **prestamo:** Registro de préstamos con relaciones a usuarios y libros

## Contribución

1. Fork del proyecto
2. Crear rama de características (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo licencia ISC.
