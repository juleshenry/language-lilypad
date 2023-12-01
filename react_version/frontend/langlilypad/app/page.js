"use client";
import React, { useState, useEffect } from "react";

const Home = () => {
  const [dictionaryResponse, setDictionaryResponse] = useState(null);
  const [dictionaryString, setDictionaryString] = useState("");

  const [translationResponse, setTranslationResponse] = useState(null);
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
        in_code: "en",
        out_code: "es",
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
      return <span>Could find a definition.</span>;
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

  function displayLanguage() {
    var selectedLanguage = document.getElementById("lang-choice").value;
    document.getElementById("selectedLanguage").innerText = selectedLanguage;
  }

  return (
    <div>
      <div style={{ textAlign: "center", margin: "20px", "fontSize": "69px" }}>
        <h1>Language Lilypad</h1>
        <h1>🪷🌺🐸🌺🪷</h1>
        <label id="languageDropdown">Input Language:</label>
        <select id="lang-choice" onChange={displayLanguage}>
            <option value="Albanian">Albanian 🇦🇱</option>
            <option value="Arabic">Arabic 🇦🇪</option>
            <option value="Azerbaijani">Azerbaijani 🇦🇿</option>
            <option value="Bengali">Bengali 🇧🇩</option>
            <option value="bulgarian">Bulgarian 🇧🇬</option>
            <option value="catalan">Catalan 🇦🇩</option>
            <option value="chinese">Chinese 🇨🇳</option>
            <option value="czech">Czech 🇨🇿</option>
            <option value="danish">Danish 🇩🇰</option>
            <option value="dutch">Dutch 🇳🇱</option>
            <option value="english" selected>English 🇬🇧</option>
            <option value="esperanto">Esperanto 🌐</option>
            <option value="estonian">Estonian 🇪🇪</option>
            <option value="finnish">Finnish 🇫🇮</option>
            <option value="french">French 🇫🇷</option>
            <option value="german">German 🇩🇪</option>
            <option value="greek">Greek 🇬🇷</option>
            <option value="hebrew">Hebrew 🇮🇱</option>
            <option value="hindi">Hindi 🇮🇳</option>
            <option value="hungarian">Hungarian 🇭🇺</option>
            <option value="indonesian">Indonesian 🇮🇩</option>
            <option value="irish">Irish ☘️</option>
            <option value="italian">Italian 🇮🇹</option>
            <option value="japanese">Japanese 🇯🇵</option>
            <option value="korean">Korean 🇰🇷</option>
            <option value="latvian">Latvian 🇱🇻</option>
            <option value="lithuanian">Lithuanian 🇱🇹</option>
            <option value="malay">Malay 🇲🇾</option>
            <option value="norwegian">Norwegian 🇳🇴</option>
            <option value="persian">Persian 🇮🇷</option>
            <option value="polish">Polish 🇵🇱</option>
            <option value="portuguese">Portuguese 🇵🇹</option>
            <option value="romanian">Romanian 🇷🇴</option>
            <option value="russian">Russian 🇷🇺</option>
            <option value="serbian">Serbian 🇷🇸</option>
            <option value="slovak">Slovak 🇸🇰</option>
            <option value="slovenian">Slovenian 🇸🇮</option>
            <option value="spanish">Spanish 🇪🇸</option>
            <option value="swedish">Swedish 🇸🇪</option>
            <option value="tagalog">Tagalog 🇵🇭</option>
            <option value="thai">Thai 🇹🇭</option>
            <option value="turkish">Turkish 🇹🇷</option>
            <option value="ukranian">Ukrainian 🇺🇦</option>
        </select>
        <p><span id="selectedLanguage">English</span></p>
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
      <div style={{ textAlign: "center" }}>
        <p>
          {makeWordsClickable(JSON.stringify(dictionaryResponse?.definicion, null, 2))}
        </p>
        {/* <p>API Result:</p> */}
        {/* <p>{JSON.stringify(response, null, 2)}</p> */}
      </div>
    </div>
  );
};

export default Home;
