// routes/definir_multilang.js
// Multi-language dictionary route supporting Portuguese, French, Korean, and Spanish
const express = require("express");
const router = express.Router();
const { Sequelize, DataTypes } = require("sequelize");
const path = require("path");

const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: path.join(__dirname, "../../db/palabras.db"),
});

// Language configuration mapping
const LANGUAGE_TABLES = {
  es: "palabras",      // Spanish (existing)
  pt: "pt_words",      // Portuguese
  fr: "fr_words",      // French
  ko: "ko_words",      // Korean
};

// Create model factory for different languages
function getEntryModel(languageCode) {
  const tableName = LANGUAGE_TABLES[languageCode] || "palabras";
  
  return sequelize.define(
    tableName,
    {
      palabra: {
        type: Sequelize.STRING,
        primaryKey: true,
      },
      definicion: Sequelize.TEXT,
      metadata: Sequelize.TEXT,
    },
    {
      timestamps: false,
      tableName: tableName,
    }
  );
}

sequelize.sync();

// Async function to query dictionary by language
async function asincDefinir(palabra, languageCode = "es") {
  try {
    const Entry = getEntryModel(languageCode);
    const result = await Entry.findOne({ where: { palabra: palabra } });
    return result;
  } catch (error) {
    console.log(`SQL error for language ${languageCode}:`, error.message);
    throw error;
  }
}

// Synchronous wrapper with word definition mapping
function sincDefinir(palabra, languageCode = "es") {
  return new Promise(async (resolve, reject) => {
    try {
      const result = await asincDefinir(palabra, languageCode);
      
      // Parse definition and find definitions for words in the definition
      let def_map = new Map();
      let def_words = result?.dataValues?.definicion
        ?.replaceAll("\n", " ")
        .replaceAll(",", "")
        .replaceAll(".", "")
        .replaceAll("-", "")
        .replaceAll("'", "")
        .replaceAll("(", "")
        .replaceAll(")", "")
        .split(" ");
      
      if (def_words) {
        let pal_defs = await Promise.all(
          def_words.map(async (item) => {
            if (!item) {
              return { definicion: undefined };
            }
            let x = await asincDefinir(item.toLowerCase(), languageCode);
            return { definicion: x?.dataValues?.definicion };
          })
        );
        
        pal_defs.forEach((element, ix) => {
          if (element?.definicion) {
            def_map.set(def_words[ix], element.definicion);
          }
        });
      }
      
      const response = {
        palabra: palabra,
        definicion: result?.dataValues?.definicion,
        palabras: Object.fromEntries(def_map),
        language: languageCode,
      };
      
      resolve(response);
    } catch (error) {
      console.log("Resolve DB error:", error.message);
      reject(error);
    }
  });
}

// Define the route for '/definir/multilang'
router.post("/", (req, res) => {
  const palabra = req.body?.palabra;
  const languageCode = req.body?.language || "es"; // Default to Spanish
  
  console.log("Multi-language query received:");
  console.log(`  Word: ${palabra}`);
  console.log(`  Language: ${languageCode}`);
  console.log("*".repeat(100));
  
  if (!palabra) {
    return res
      .status(400)
      .json({ error: "Palabra not provided in the request body" });
  }
  
  if (!LANGUAGE_TABLES[languageCode]) {
    return res
      .status(400)
      .json({ error: `Unsupported language: ${languageCode}` });
  }
  
  sincDefinir(palabra, languageCode)
    .then((result) => {
      console.log("Query successful");
      res.json(result);
    })
    .catch((error) => {
      console.error(error.message);
      res.status(500).json({ 
        error: "Failed to fetch definition",
        message: error.message 
      });
    });
});

// Get list of supported languages
router.get("/languages", (req, res) => {
  const languages = [
    { code: "es", name: "Spanish", nativeName: "Español" },
    { code: "pt", name: "Portuguese", nativeName: "Português" },
    { code: "fr", name: "French", nativeName: "Français" },
    { code: "ko", name: "Korean", nativeName: "한국어" },
  ];
  
  res.json(languages);
});

module.exports = router;
