const Autor = require('./src/models/Autor');

async function testCreate() {
    try {
        const autorData = {
            nombre: "Juan",
            apellido: "Perez",
            fecha_nacimiento: "1990-01-01",
            nacionalidad: "Espanol",
            correo_electronico: "juan@test.com"
        };
        
        console.log('Intentando crear autor:', autorData);
        const result = await Autor.createAutor(autorData);
        console.log('Autor creado exitosamente:', result);
    } catch (error) {
        console.error('Error creando autor:', error.message);
        console.error('Error completo:', error);
    }
}

testCreate();
