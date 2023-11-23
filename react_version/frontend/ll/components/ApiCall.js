import React, { useState } from "react";
import axios from "axios";

const ApiCall = () => {
  const [inputValue, setInputValue] = useState("");
  const [result, setResult] = useState("");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleApiCall = async () => {
    try {
      console.log(`we called ${inputValue}`);
      //   const response = await axios.get(`http://localhost:3001/definir?palabra=${inputValue}`);
      // curl -X GET -H "Content-Type: application/json" -d '{"palabra": "sin"}' http://localhost:3031/definir

        // `http://localhost:3031/definir?palabra=${inputValue}`,
      const response = await axios.get(
        `https://api.kanye.rest/`,
        // {palabra : inputValue},
        // {
        //   headers: {
        //     "Content-Type": "application/json;charset=utf-8",
        //   },
        // },
      );
      console.log(response);
      setResult(response.data); // Adjust this based on your API response structure
    } catch (error) {
      console.error("Error fetching data:", error);
      setResult("Error fetching data");
    }
  };

  return (
    <div>
      <div style={{ textAlign: "center", margin: "20px" }}>
        <input type="text" value={inputValue} onChange={handleInputChange} />
        <button onClick={handleApiCall}>Call API</button>
      </div>
      <div style={{ textAlign: "center" }}>
        <p>API Result:</p>
        <p>{result.quote}</p>
      </div>
    </div>
  );
};

export default ApiCall;
