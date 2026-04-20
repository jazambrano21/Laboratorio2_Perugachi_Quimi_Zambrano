const Autor = require('./src/models/Autor');
const Libro = require('./src/models/Libro');
const Usuario = require('./src/models/Usuario');
const Prestamo = require('./src/models/Prestamo');

async function setupEscenario2() {
    console.log('Preparando datos para Escenario 2...');
    
    try {
        // 1. Crear autores
        console.log('Creando autores...');
        const autores = [
            {nombre: "Gabriel", apellido: "García", fecha_nacimiento: "1927-03-06", nacionalidad: "Colombiana", correo_electronico: "garcia@literatura.com"},
            {nombre: "Julio", apellido: "Cortázar", fecha_nacimiento: "1914-08-26", nacionalidad: "Argentina", correo_electronico: "cortazar@literatura.com"},
            {nombre: "Mario", apellido: "Vargas", fecha_nacimiento: "1936-03-28", nacionalidad: "Peruana", correo_electronico: "vargas@literatura.com"},
            {nombre: "Jorge", apellido: "Borges", fecha_nacimiento: "1899-08-24", nacionalidad: "Argentina", correo_electronico: "borges@literatura.com"},
            {nombre: "Pablo", apellido: "Neruda", fecha_nacimiento: "1904-07-12", nacionalidad: "Chilena", correo_electronico: "neruda@literatura.com"}
        ];
        
        for (let autor of autores) {
            try {
                await Autor.createAutor(autor);
            } catch (error) {
                console.log('Autor ya existe o error:', error.message);
            }
        }
        
        // 2. Crear usuarios (200)
        console.log('Creando 200 usuarios...');
        for (let i = 1; i <= 200; i++) {
            try {
                await Usuario.createUsuario({
                    nombre: `Usuario${i}`,
                    apellido: `Apellido${i}`,
                    correo: `usuario${i}@biblioteca.edu`,
                    tipo_usuario: i <= 150 ? "lector" : "bibliotecario"
                });
            } catch (error) {
                console.log(`Usuario ${i} ya existe o error:`, error.message);
            }
        }
        
        // 3. Crear libros (500)
        console.log('Creando 500 libros...');
        const titulos = [
            "Cien Años de Soledad", "Rayuela", "Conversación en La Catedral", "El Aleph",
            "Veinte Poemas de Amor", "El Señor de los Anillos", "1984", "Ulises",
            "Don Quijote", "La Odisea", "Hamlet", "Romeo y Julieta"
        ];
        
        for (let i = 1; i <= 500; i++) {
            try {
                await Libro.createLibro({
                    titulo: `${titulos[i % titulos.length]} #${i}`,
                    isbn: `978-${1000000000 + i}`,
                    anio_publicacion: 1990 + (i % 33),
                    edicion: `${['Primera', 'Segunda', 'Tercera'][i % 3]} Edición`,
                    autor_id: (i % 5) + 1
                });
            } catch (error) {
                console.log(`Libro ${i} ya existe o error:`, error.message);
            }
        }
        
        // 4. Crear préstamos (1000) - 50% activos, 50% históricos
        console.log('Creando 1000 préstamos...');
        for (let i = 1; i <= 1000; i++) {
            try {
                const prestamoData = {
                    usuario_id: Math.floor(Math.random() * 200) + 1,
                    libro_id: Math.floor(Math.random() * 500) + 1,
                    fecha_prestamo: `2024-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
                    fecha_devolucion_prevista: `2024-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`
                };
                
                // 50% históricos (con fecha de devolución)
                if (Math.random() < 0.5) {
                    prestamoData.fecha_devolucion_real = `2024-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`;
                }
                
                await Prestamo.createPrestamo(prestamoData);
            } catch (error) {
                console.log(`Préstamo ${i} error:`, error.message);
            }
        }
        
        console.log('¡Escenario 2 configurado exitosamente!');
        console.log('- 200 usuarios creados');
        console.log('- 500 libros creados');  
        console.log('- 1000 préstamos creados');
        
    } catch (error) {
        console.error('Error configurando Escenario 2:', error);
    }
}

setupEscenario2();
