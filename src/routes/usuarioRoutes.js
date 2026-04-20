const express = require('express');
const router = express.Router();

const {
    getAllUsuarios,
    createUsuario,
    updateUsuario,
    getPrestamosByUsuario
} = require('../controllers/usuarioController');

router.get('/', getAllUsuarios);
router.post('/', createUsuario);
router.put('/:id', updateUsuario);
router.get('/:id/prestamos', getPrestamosByUsuario);

module.exports = router;