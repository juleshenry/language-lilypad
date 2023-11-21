// routes/definirRoutes.js

const express = require("express");
const router = express.Router();
const { Sequelize, DataTypes } = require("sequelize");
const path = require("path");

const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: path.join(__dirname, "../../db/palabras.db"),
});

// Define a model for your entries
const Entry = sequelize.define(
  "palabras",
  {
    palabra: {
      type: Sequelize.STRING,
      primaryKey: true,
    },
    definicion: Sequelize.TEXT,
  },
  {
    timestamps: false,
  },
);

sequelize.sync();

// An asynchronous function that queries the database
async function asincDefinir(palabra) {
  try {
    // Simulating a Sequelize query to find a user
    const user = await Entry.findOne({ where: { palabra: palabra } });
    return user; // Returning the result of the query
  } catch (error) {
    throw error; // Propagating any errors that occurred during the query
  }
}

// Synchronous function that calls asyncFunc
function sincDefinir(palabra) {
  return new Promise(async (resolve, reject) => {
    try {
      const result = await asincDefinir(palabra);
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
}

// Define the route for '/definir'
router.get("/", (req, res) => {
  const palabra = req.body.palabra;
  if (!palabra) {
    return res
      .status(400)
      .json({ error: "Palabra not provided in the request body" });
  }
  sincDefinir(palabra)
    .then((result) => {
      console.log("?");
      console.log(result); // Output: Async operation complete
      const definicion = "exito";
      res.json(result);
    })
    .catch((error) => {
      console.error(error.message);
      const definicion = "fail";
      res.json(definicion);
    });
});

module.exports = router;
