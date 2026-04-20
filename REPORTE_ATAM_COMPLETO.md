# Reporte ATAM Completo - Sistema de Biblioteca

## Instrucciones para Ejecución

### 1. Preparar el Entorno

```bash
# 1. Iniciar la base de datos
docker-compose up -d

# 2. Instalar dependencias
npm install

# 3. Iniciar la aplicación
npm run dev

# 4. Verificar que la API está funcionando
curl http://localhost:3000/api/autores
```

### 2. Instalar Locust

```bash
pip install locust
```

### 3. Ejecutar los Escenarios

**Importante:** Ejecutar cada escenario durante al menos 3 minutos para obtener métricas estables.

```bash
# Escenario 1: Búsqueda de Autores bajo Carga Moderada
locust -f tests/locustfile_escenario1.py --host=http://localhost:3000

# Escenario 2: Consulta de Préstamos por Usuario con Relaciones  
locust -f tests/locustfile_escenario2.py --host=http://localhost:3000

# Escenario 3: Creación Concurrente de Préstamos
locust -f tests/locustfile_escenario3.py --host=http://localhost:3000

# Escenario 4: Integración de Operaciones Mixtas bajo Carga Máxima
locust -f tests/locustfile_escenario4.py --host=http://localhost:3000
```

### 4. Interfaz Web Locust

Abrir `http://localhost:8089` en el navegador y configurar:

- **Escenario 1:** 80 usuarios, Hatch Rate: 20/s
- **Escenario 2:** 50 usuarios, Hatch Rate: 15/s  
- **Escenario 3:** 60 usuarios, Hatch Rate: 30/s
- **Escenario 4:** 150 usuarios, Hatch Rate: 50/s

---

## Tablas ATAM (Para Completar con Resultados Reales)

### ESC-BUSQ-01: Búsqueda de Autores bajo Carga Moderada

| Métrica | Valor Obtenido |
|----------|---------------|
| **Tiempo de Respuesta Promedio** | [COMPLETAR] ms |
| **Percentil 95** | [COMPLETAR] ms |
| **RPS Máximo** | [COMPLETAR] req/s |
| **Tasa de Errores** | [COMPLETAR] % |
| **CPU Promedio** | [COMPLETAR] % |
| **Memoria Uso** | [COMPLETAR] MB |

**Configuración de Prueba:**
- Usuarios concurrentes: 80
- Tasa de generación: 20 usuarios/s
- Duración: 3+ minutos
- Base de datos: 500 autores precargados

---

### ESC-PREST-02: Consulta de Préstamos por Usuario con Relaciones

| Métrica | Valor Obtenido |
|----------|---------------|
| **Tiempo de Respuesta Promedio** | [COMPLETAR] ms |
| **Percentil 95** | [COMPLETAR] ms |
| **RPS Máximo** | [COMPLETAR] req/s |
| **Tasa de Errores** | [COMPLETAR] % |
| **CPU Promedio** | [COMPLETAR] % |
| **Memoria Uso** | [COMPLETAR] MB |

**Configuración de Prueba:**
- Usuarios concurrentes: 50
- Tasa de generación: 15 usuarios/s
- Duración: 3+ minutos
- Base de datos: 200 usuarios, 500 libros, 1000 préstamos

---

### ESC-PREST-03: Creación Concurrente de Préstamos

| Métrica | Valor Obtenido |
|----------|---------------|
| **Tasa de Éxito** | [COMPLETAR] % |
| **Tiempo de Respuesta Promedio** | [COMPLETAR] ms |
| **Percentil 95** | [COMPLETAR] ms |
| **RPS Máximo** | [COMPLETAR] req/s |
| **Errores 400 (No disponible)** | [COMPLETAR] % |
| **CPU Promedio** | [COMPLETAR] % |

**Configuración de Prueba:**
- Usuarios concurrentes: 60
- Tasa de generación: 30 usuarios/s
- Duración: 3+ minutos
- Base de datos: 200 usuarios, 500 libros con stock 1-3

---

### ESC-INTEGR-04: Integración de Operaciones Mixtas

| Métrica | Valor Obtenido |
|----------|---------------|
| **Tiempo de Respuesta Promedio** | [COMPLETAR] ms |
| **Percentil 95** | [COMPLETAR] ms |
| **RPS Máximo** | [COMPLETAR] req/s |
| **Tasa de Errores General** | [COMPLETAR] % |
| **Operaciones/Segundo Mixtas** | [COMPLETAR] ops/s |
| **CPU Promedio** | [COMPLETAR] % |

**Configuración de Prueba:**
- Usuarios concurrentes: 150
- Tasa de generación: 50 usuarios/s
- Duración: 3+ minutos
- Base de datos: 1000 usuarios, 2000 libros, 5000 préstamos

---

## Capturas de Pantalla Requeridas

### Para cada escenario, tomar capturas de:

1. **Pestaña Statistics** (al finalizar la prueba):
   - Mostrar todas las métricas principales
   - Destacar RPS, Failure %, Response Times

2. **Pestaña Charts** (durante la prueba):
   - Mostrar gráfico de RPS vs Time
   - Mostrar gráfico de Response Times vs Time

3. **Pestaña Failures** (si hay errores):
   - Mostrar tipos de errores y frecuencias

### Ejemplo de Captura (ESC-BUSQ-01):

```
┌─────────────────────────────────────────────────────────────┐
│                    Locust Statistics                    │
├─────────────────────────────────────────────────────────────┤
│ Type                 Name                    # reqs    # fails│
│ GET                  /api/autores/buscar      12,450    25   │
│                      Median      Avg       95%       Max│
│                      45ms        52ms      89ms      450ms│
│                      RPS: 65.2    Failures: 0.2%        │
└─────────────────────────────────────────────────────────────┘
```

---

## Análisis de Resultados Esperados

### ESC-BUSQ-01: Búsqueda de Autores
- **Objetivo:** <50ms tiempo respuesta promedio
- **Expected RPS:** 60-80 req/s
- **Expected Error Rate:** <1%

### ESC-PREST-02: Consulta de Préstamos  
- **Objetivo:** <100ms tiempo respuesta promedio (JOINs)
- **Expected RPS:** 40-60 req/s
- **Expected Error Rate:** <2%

### ESC-PREST-03: Creación Concurrente
- **Objetivo:** Alta tasa de éxito (>80%)
- **Expected RPS:** 25-35 req/s
- **Expected 400 Errors:** 10-20% (libros no disponibles)

### ESC-INTEGR-04: Operaciones Mixtas
- **Objetivo:** Sistema estable bajo carga máxima
- **Expected RPS:** 100-150 req/s total
- **Expected Error Rate:** <5%

---

## Recomendaciones para Presentación

1. **Ejecutar cada escenario exactamente como se especifica**
2. **Tomar capturas de pantalla claras y legibles**
3. **Completar las tablas con valores reales obtenidos**
4. **Incluir análisis breve de cada resultado**
5. **Documentar cualquier comportamiento inesperado**

---

## Checklist de Entrega

- [ ] Ejecutar ESC-BUSQ-01 (80 usuarios, 3+ min)
- [ ] Capturas Statistics y Charts ESC-BUSQ-01
- [ ] Completar tabla ESC-BUSQ-01

- [ ] Ejecutar ESC-PREST-02 (50 usuarios, 3+ min)  
- [ ] Capturas Statistics y Charts ESC-PREST-02
- [ ] Completar tabla ESC-PREST-02

- [ ] Ejecutar ESC-PREST-03 (60 usuarios, 3+ min)
- [ ] Capturas Statistics y Charts ESC-PREST-03
- [ ] Completar tabla ESC-PREST-03

- [ ] Ejecutar ESC-INTEGR-04 (150 usuarios, 3+ min)
- [ ] Capturas Statistics y Charts ESC-INTEGR-04  
- [ ] Completar tabla ESC-INTEGR-04

- [ ] Análisis final de resultados
- [ ] Conclusiones y recomendaciones

---

**Fecha de Ejecución:** [COMPLETAR]  
**Versión del Sistema:** 1.0.0  
**Entorno de Prueba:** Docker + Node.js + Locust
