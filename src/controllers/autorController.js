const Autor = require('../models/Autor');

const getAllAutores = async (req, res) => {
    try {
        const autores = await Autor.findAll();
        res.json(autores);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener autores' });
    }
}

const createAutor = async (req, res) => {
    try {
       const nuevoAutor = await Autor.createAutor(req.body);
       res.status(201).json(nuevoAutor);
    }
    catch (error) {
        res.status(500).json({ error: error.message });
    }
}

const deleteAutor = async (req, res) => {
    try {
        const result = await Autor.deleteAutor(req.params.id);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }           
}

const updateAutor = async (req, res) => {
    try {
        const result = await Autor.updateAutor(req.params.id, req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}

const getAutorById = async (req, res) => {
    try {
        const autor = await Autor.findById(req.params.id);
        res.json(autor);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}

const searchAutores = async (req, res) => {
    try {
        const { q } = req.query;
        
        if (!q) {
            return res.status(400).json({ 
                error: 'El parámetro de búsqueda "q" es obligatorio' 
            });
        }
        
        const autores = await Autor.searchByPartial(q);
        res.json(autores);
    } catch (error) {
        res.status(500).json({ error: 'Error al buscar autores' });
    }
}

module.exports = {
    getAllAutores,
    createAutor,
    deleteAutor,
    updateAutor,
    getAutorById,
    searchAutores
};