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
    consoel.log("SQL error");
    throw error; // Propagating any errors that occurred during the query
  }
}

// Synchronous function that calls asyncFunc
function sincDefinir(palabra) {
  return new Promise(async (resolve, reject) => {
    try {
      const result = await asincDefinir(palabra);
      // parse definicion
      let def_map = new Map();
      let def_words = result?.dataValues?.definicion
        .replaceAll("\n", " ")
        .replaceAll(",", "")
        .replaceAll(".", "")
        .replaceAll("-", "")
        .replaceAll("-", "")
        .replaceAll("'", "")
        .replaceAll("(", "")
        .split(" ");
      if (def_words) {
        let pal_defs = await Promise.all(
        def_words.map(async (item) => {
          if (!item) {
            return { definicion: undefined };
          }
          let x = await asincDefinir(item.toLowerCase());
          return { definicion: x?.dataValues?.definicion };
        }),
        );
        pal_defs.forEach((element, ix) => {
          if (element?.definicion) {
            def_map.set(def_words[ix], element.definicion);
          }
        });
      }
      // for (const [x, y] of def_map.entries()) {
      //   console.log(x, y);
      // }
      cool = {
        palabra: palabra,
        definicion: result?.dataValues?.definicion,
        palabras: Object.fromEntries(def_map)
      };  
      resolve(cool);
      // resolve(result);
    } catch (error) {
      console.log("Resolve DB error");
      reject(error);
    }
  });
}

// Define the route for '/definir'
router.post("/", (req, res) => {
  const palabra = req.body?.palabra;
  console.log("1o paso, recibido :");
  console.log(req.body);
  console.log("*".repeat(100));
  if (!palabra) {
    return res
      .status(400)
      .json({ error: "Palabra not provided in the request body" });
  }
  sincDefinir(palabra)
    .then((result) => {
      console.log("sincronizado activado");
      console.log(result); // Output: Async operation complete
      res.json(result);
    })
    .catch((error) => {
      console.error(error.message);
      const { definicion } = "fail";
      res.json(definicion);
    });
});

module.exports = router;
