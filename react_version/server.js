const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // Import the cors middleware

const app = express();
const port = 8080;

app.use(cors()); // Enable CORS for all routes

app.use(bodyParser.json());

app.post('/definir', (req, res) => {
  const term = req.body.term;
  // Your logic to fetch the definition based on the term goes here

  // For demonstration purposes, let's assume a simple definition
  const definition = `Defin: for ${term}`;

  res.json({ definicion: definition });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
