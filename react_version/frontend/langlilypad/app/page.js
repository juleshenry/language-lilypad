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

  return (
    <div>
      <div style={{ textAlign: "center", margin: "20px", "fontSize": "69px" }}>
        <h1>Language Lilypad</h1>
        <h1>🪷🌺🐸🌺🪷</h1>
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
