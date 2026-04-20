const Usuario = require('../models/Usuario');

const getAllUsuarios = async (req, res) => {
    try {
        const usuarios = await Usuario.findAll();
        res.json(usuarios);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener usuarios' });
    }
}

const createUsuario = async (req, res) => {
    try {
        const nuevo = await Usuario.createUsuario(req.body);
        res.status(201).json(nuevo);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}

const updateUsuario = async (req, res) => {
    try {
        const result = await Usuario.updateUsuario(req.params.id, req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}

const getPrestamosByUsuario = async (req, res) => {
    try {
        const { id } = req.params;
        
        const usuario = await Usuario.findById(id);
        if (!usuario) {
            return res.status(404).json({ 
                error: 'Usuario no encontrado' 
            });
        }
        
        const prestamos = await Usuario.getPrestamosByUsuarioId(id);
        res.json(prestamos);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener préstamos del usuario' });
    }
}

module.exports = {
    getAllUsuarios,
    createUsuario,
    updateUsuario,
    getPrestamosByUsuario
}