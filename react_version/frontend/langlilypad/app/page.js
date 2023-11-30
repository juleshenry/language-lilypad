"use client";
import React, { useState, useEffect } from "react";

const Home = () => {
  const [response, setResponse] = useState(null);
  const [inputValue, setInputValue] = useState("");

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

  const handleInputChange = (e) => {
    setInputValue(limpia(e.target.value));
  };

  useEffect(() => {
    definirData();
  }, [inputValue]);

  const handleInputClick = async (word) => {
    setInputValue(limpia(word));
  };

  // fetch dynamic BE calls
  const definirData = async () => {
    try {
      console.log("fetching " + limpia(inputValue) + " from backend");
      let d = { palabra: limpia(inputValue) };
      const res = await fetch("http://localhost:3000/definir", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(d),
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const makeWordsClickable = () => {
    const words = response?.definicion?.split(" ");
    if (!words) {
      return <span>Nada.</span>;
    }
    // console.log( new Map(Object.entries(response?.palabras)).keys() );
    return words.map((word, index) => (
      <span
        key={index}
        className={
          word in response?.palabras ? "clickable-word" : "unclickable-word"
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
    // You can add logic here to perform actions based on the selected language
  }
  return (
    <div>
      <div style={{ textAlign: "center", margin: "20px", "fontSize": "69px" }}>
        <h1>Language Lilypad</h1>
        <h1>🪷🌺🐸🌺🪷</h1>
        <label id="languageDropdown">Select Language:</label>
        <select id="lang-choice" onChange={displayLanguage}>
            <option value="albanian">Albanian 🇦🇱</option>
            <option value="arabic">Arabic 🇦🇪</option>
            <option value="azerbaijani">Azerbaijani 🇦🇿</option>
            <option value="bengali">Bengali 🇧🇩</option>
            <option value="bulgarian">Bulgarian 🇧🇬</option>
            <option value="catalan">Catalan 🇦🇩</option>
            <option value="chinese">Chinese 🇨🇳</option>
            <option value="czech">Czech 🇨🇿</option>
            <option value="danish">Danish 🇩🇰</option>
            <option value="dutch">Dutch 🇳🇱</option>
            <option value="english">English 🇬🇧</option>
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
        <p><span id="selectedLanguage">Selected Language: </span></p>
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
        />
        </div>
        <div>
        <input
          className="translated-text"
          style={{
            textAlign: "center",
            height: "50px",
            color: "#5EDD5F",
            "fontSize": "40px",
          }}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
        />
        </div>
      </div>
      <div style={{ textAlign: "center" }}>
        <p>
          {makeWordsClickable(JSON.stringify(response?.definicion, null, 2))}
        </p>
        {/* <p>API Result:</p> */}
        {/* <p>{JSON.stringify(response, null, 2)}</p> */}
      </div>
    </div>
  );
};

export default Home;
