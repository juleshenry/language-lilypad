// server.js

const express = require("express");
const bodyParser = require("body-parser");
const definirRoutes = require("./src/routes/definir"); // Import the definir route

const app = express();
app.use(bodyParser.json());
const cors=require("cors");
const corsOptions ={
   origin:'*', 
  //  credentials:true,            //access-control-allow-credentials:true
   optionSuccessStatus:200,
}

app.use(cors()) // Use this after the variable declaration

// Use the definir route
app.use("/definir", definirRoutes);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// SLOW AND STEADY

//curl -X GET -H "Content-Type: application/json" -d '{"palabra": "example"}' http://localhost:3001/definir
