// server.js

const express = require("express");
const cors=require("cors");
const bodyParser = require("body-parser");
const definirRoutes = require("./src/routes/definir"); // Import the definir route

const app = express();

app.use(cors()) // Use this after the variable declaration

app.use(bodyParser.json());

// Use the definir route
app.use("/definir", definirRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  if (res.statusCode === 400) {
    console.error('Error 400: ', err.message);
  }
  next(err);
});


const PORT = process.env.PORT || 3031;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// SLOW AND STEADY

//curl -X GET -H "Content-Type: application/json" -d '{"palabra": "example"}' http://localhost:3001/definir
