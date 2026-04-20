const db = require('../config/db');

const Autor = {
    findAll: async () => {
        const [rows] = await db.query('SELECT * FROM autor');
        return rows;
    },

    //crear nuevo autor
    createAutor: async ({nombre,
                        apellido,
                        fecha_nacimiento,
                        nacionalidad,
                        correo_electronico}) => {
        const [result] = await db.query(
            'INSERT INTO autor (nombre, apellido, fecha_nacimiento, nacionalidad, correo_electronico) VALUES (?, ?, ?, ?, ?)',
            [nombre, apellido, fecha_nacimiento, nacionalidad, correo_electronico]
        );
        return { id: result.insertId, nombre, apellido, fecha_nacimiento, nacionalidad, correo_electronico };

    },

    //eliminar autor por id
    deleteAutor: async (id) => {
        await db.query('DELETE FROM autor WHERE id = ?', [id]);
        return { message: 'Autor eliminado exitosamente' };
    },

    // actualizar autor
    updateAutor: async (id, {nombre, apellido, fecha_nacimiento, nacionalidad, correo_electronico}) => {
        await db.query(
            'UPDATE autor SET nombre = ?, apellido = ?, fecha_nacimiento = ?, nacionalidad = ?, correo_electronico = ? WHERE id = ?',
            [nombre, apellido, fecha_nacimiento, nacionalidad, correo_electronico, id]
        );
        return { message: 'Autor actualizado correctamente' };
    },

    // buscar autor por id
    findById: async (id) => {
        const [rows] = await db.query('SELECT * FROM autor WHERE id = ?', [id]);
        return rows[0]; // Devuelve el primer autor encontrado o undefined si no existe
    },

    // buscar autores por coincidencia parcial en nombre o apellido
    searchByPartial: async (query) => {
        const [rows] = await db.query(
            'SELECT * FROM autor WHERE LOWER(nombre) LIKE LOWER(?) OR LOWER(apellido) LIKE LOWER(?)',
            [`%${query}%`, `%${query}%`]
        );
        return rows;
    }

};

module.exports = Autor;