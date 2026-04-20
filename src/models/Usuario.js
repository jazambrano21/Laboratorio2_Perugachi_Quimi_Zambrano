const db = require('../config/db');

const Usuario = {
    findAll: async () => {
        const [rows] = await db.query('SELECT * FROM usuario');
        return rows;
    },

    createUsuario: async ({nombre, apellido, correo, tipo_usuario}) => {
        const [result] = await db.query(
            'INSERT INTO usuario (nombre, apellido, correo, tipo_usuario) VALUES (?, ?, ?, ?)',
            [nombre, apellido, correo, tipo_usuario]
        );
        return { id: result.insertId, nombre, apellido, correo, tipo_usuario };
    },

    updateUsuario: async (id, {nombre, apellido, correo, tipo_usuario}) => {
        await db.query(
            'UPDATE usuario SET nombre = ?, apellido = ?, correo = ?, tipo_usuario = ? WHERE id = ?',
            [nombre, apellido, correo, tipo_usuario, id]
        );
        return { message: 'Usuario actualizado' };
    },

    findById: async (id) => {
        const [rows] = await db.query('SELECT * FROM usuario WHERE id = ?', [id]);
        return rows[0];
    },

    getPrestamosByUsuarioId: async (usuarioId) => {
        const [rows] = await db.query(`
            SELECT 
                p.id,
                p.fecha_prestamo,
                p.fecha_devolucion_prevista,
                p.fecha_devolucion_real,
                l.titulo,
                l.isbn,
                l.anio_publicacion
            FROM prestamo p
            JOIN libro l ON p.libro_id = l.id
            WHERE p.usuario_id = ?
            ORDER BY p.fecha_prestamo DESC
        `, [usuarioId]);
        return rows;
    }
};

module.exports = Usuario;