  import React, { useState } from 'react';
  import axios from 'axios';

  const ApiCall = () => {
    const [inputValue, setInputValue] = useState('');
    const [result, setResult] = useState('');

    const handleInputChange = (e) => {
      setInputValue(e.target.value);
    };

    const handleApiCall = async () => {
      try {
        console.log(`called ${inputValue}`);
      //   const response = await axios.get(`http://localhost:3001/definir?palabra=${inputValue}`);
      const response = await axios.get(`http://localhost:3001/definir?palabra=${inputValue}`,
      {
          // method: 'GET',
          // mode: 'cors',
          // cache: 'no-cache',
          // credentials: 'same-origin' ,
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        });

      //   response = await axios.get(`https://api.kanye.rest/`);
        setResult(response.json()); // Adjust this based on your API response structure
      } catch (error) {
        console.error('Error fetching data:', error);
        setResult('Error fetching data');
      }
    };

    return (
      <div>
        <div style={{ textAlign: 'center', margin: '20px' }}>
          <input type="text" value={inputValue} onChange={handleInputChange} />
          <button onClick={handleApiCall}>Call API</button>
        </div>
        <div style={{ textAlign: 'center' }}>
          <p>API Result:</p>
          <p>{result?.quote || result?.definicion}</p>
        </div>
      </div>
    );
  };

  export default ApiCall;
