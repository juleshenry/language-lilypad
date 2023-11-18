// routes/definirRoutes.js

const express = require('express');
const router = express.Router();

function definir(palabra) {
  // Your logic to define the word goes here
  const definicion = 'DEFINED';
  return { definicion };
}

// Define the route for '/definir'
router.get('/', (req, res) => {
  const palabra = req.body.palabra;

  if (!palabra) {
    return res.status(400).json({ error: 'Palabra not provided in the request body' });
  }

  const resultado = definir(palabra);
  res.json(resultado);
});

module.exports = router;