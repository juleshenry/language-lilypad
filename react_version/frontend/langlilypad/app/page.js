"use client";
import React, { useState, useEffect } from "react";
import { languageOptions } from './languageOptions';


const Home = () => {
  const [dictionaryResponse, setDictionaryResponse] = useState(null);
  const [dictionaryString, setDictionaryString] = useState("");

  const [inputLanguage, setInputLanguage] = useState("en");
  const [outputLanguage, setOutputLanguage] = useState("es");

  const [translationString, setTranslationString] = useState("");

  const limpia = (e) => {
    return e
      .replaceAll("\n", " ")
      .replaceAll(",", "")
      .replaceAll(".", "")
      .replaceAll("-", "")
      .replaceAll("-", "")
      .replaceAll("'", "")
      .replaceAll("(", "").toLowerCase();
  };

  const handleDictionaryChange = (e) => {
    setDictionaryString(limpia(e.target.value));
  };

  const handleTranslationChange = (e) => {
    setTranslationString(limpia(e.target.value));
  };

  useEffect(() => {
    definirData();
  }, [dictionaryString]);

  useEffect(() => {
    traducirData();
  }, [translationString])

  const handleInputClick = async (word) => {
    setDictionaryString(limpia(word));
  };

  const handleInputLangChange = (e) => {
    setInputLanguage(e.target.value);
  };

  const handleOutputLangChange = (e) => {
    setOutputLanguage(e.target.value);
  };

  const definirData = async () => {
    try {
      console.log("querying dictionary for " + limpia(dictionaryString));
      let d = { palabra: limpia(dictionaryString) };
      const res = await fetch("http://localhost:3000/definir", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(d),
      });
      const res_json = await res.json();
      setDictionaryResponse(res_json);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const traducirData = async () => {
    try {
      // Translate
      console.log("querying translator for " + limpia(translationString));
      const trans_data = { 
        in_code: inputLanguage,
        out_code: outputLanguage,
        text: limpia(translationString)
      };
      const trad_resp = await fetch("http://127.0.0.1:5000/traducir", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(trans_data),
      });
      const trad_json = await trad_resp.json();
      console.log(trad_json);
      // set dictionary input to translated
      setDictionaryString(trad_json.traduccion);
      let def_data = { palabra: trad_json.traduccion };
      const def_res = await fetch("http://localhost:3000/definir", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(def_data),
      });
      const def_json = await def_res.json();
      setDictionaryResponse(def_json);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const makeWordsClickable = () => {
    const words = dictionaryResponse?.definicion?.split(" ");
    if (!words) {
      return <span>Could not find a definition.</span>;
    }
    // console.log( new Map(Object.entries(response?.palabras)).keys() );
    return words.map((word, index) => (
      <span
        key={index}
        className={
          (dictionaryResponse?.palabras && word in dictionaryResponse?.palabras) ? "clickable-word" : "unclickable-word"
        }
        onClick={async () => {
          await handleInputClick(word);
        }}
      >
        {word + (index === words.length - 1 ? "" : " ")}
      </span>
    ));
  };

  return (
    <div>
      <div style={{ textAlign: "center", margin: "20px", "fontSize": "69px" }}>
        <h1>Language Lilypad</h1>
        <h1>🪷🌺🐸🌺🪷</h1>
        <label id="inputLanguageDropdown">Input:</label>
        <select id="input-lang-choice" value={inputLanguage} onChange={handleInputLangChange}>
          {languageOptions.map((lang) => (
                <option 
                  key={lang.value} 
                  value={lang.value} 
                >
                  {lang.label}
                </option>
              ))}
        </select>
        <p>
          <label id="outputLanguageDropdown">Output:</label>
          <select id="output-lang-choice" value={outputLanguage} onChange={handleOutputLangChange}>
            {languageOptions.map((lang) => (
              <option 
                key={lang.value} 
                value={lang.value} 
              >
                {lang.label}
              </option>
            ))}
          </select>
        </p>
        <div>
        <input
          className="input-text"
          style={{
            textAlign: "center",
            height: "50px",
            color: "#5EDD5F",
            "fontSize": "40px",
          }}
          type="text"
          value={translationString}
          onChange={handleTranslationChange}
        />
        </div>
        <div>
        <input
          className="dictionary-text"
          style={{
            textAlign: "center",
            height: "50px",
            color: "#E5737A",
            "fontSize": "40px",
          }}
          type="text"
          value={dictionaryString}
          onChange={handleDictionaryChange}
        />
        </div>
      </div>
      <div className="definition-container">
        <p>
          {makeWordsClickable(JSON.stringify(dictionaryResponse?.definicion, null, 2))}
        </p>
      </div>
    </div>
  );
};

export default Home;
