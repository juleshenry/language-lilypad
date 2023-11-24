import React, { useState } from "react";
import axios from "axios";

const ApiCall = () => {
  const [inputValue, setInputValue] = useState("");
  const [response, setResponse] = useState("");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleApiCall = async () => {
    try {
      console.log(`Finna call ${inputValue}`);
      let d = {'palabra' : inputValue};
      const res = await fetch('http://localhost:3000/definir',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(d), 
      }
      );
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setResponse("Error fetching data");
    }
  };
// `https://api.kanye.rest/`,
  return (
    <div>
      <div style={{ textAlign: "center", margin: "20px" }}>
        <input type="text" value={inputValue} onChange={handleInputChange} />
        <button onClick={handleApiCall}>Call API</button>
      </div>
      <div style={{ textAlign: "center" }}>
        <p>API Result:</p>
        <p>{JSON.stringify(response, null, 2)}</p>
      </div>
    </div>
  );
};

export default ApiCall;

      // const response = await axios.get(`http://localhost:3031/definir?palabra=${inputValue}`);
      // curl -X GET -H "Content-Type: application/json" -d '{"palabra": "sin"}' http://localhost:3031/definir
      // const response = await axios.post(
      //   `http://localhost:3000/definir`,
      //   JSON.stringify({
      //     palabra: inputValue
      //   }),
      //   {
      //     headers: {
      //       "Content-Type": "application/json;charset=utf-8",
      //     }
      //   }
      // );