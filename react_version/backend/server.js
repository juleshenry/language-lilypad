const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // Import the cors middleware
const definir = require('./src/definir');
const app = express();
const port = 8080;

app.use(cors()); // Enable CORS for all routes

app.use(bodyParser.json());

app.post('/definir', (req, res) => {
  const term = req.body.term;
  // Your logic to fetch the definition based on the term goes here

  // For demonstration purposes, let's assume a simple definition
  async function ass(pa) {
    try {
        const result1 = await definir(pa);
        // const result2 = await definir('locomóvil');
        console.log(result1?.dataValues.?definicion);
        return result1;
    } catch (error) {
        // Handle any errors that might occur in the chain
        console.error(error);
    }
  }
  let x = ass(req.body.term).then(result => {
    // Use or log the result here
    console.log(result);
  })
  .catch(error => {
    // Handle errors if needed
    console.error('Error:', error);
  });
  const definition = `Defin: for ${term}`;
  console.log(`@@@ ${term}`);
  res.json({ definicion: definition });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
