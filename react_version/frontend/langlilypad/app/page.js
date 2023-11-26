"use client";
import React, { useState } from 'react';

const Home = () => {
  const [response, setResponse] = useState(null);
  
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleInputClick = (e) => {
    setInputValue(e);
  };

  // fetch hard-coded BE call
  const fetchData = async () => {
    try {
      console.log('fetch BE directly from button');
      let d = {'palabra' : 'sin'};
      const res = await fetch('http://localhost:3000/definir',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(d), 
      }
      );
      // const res = await fetch('http://localhost:3000/definir?palabra=sin');
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // fetch dynamic BE calls
  const definirData = async () => {
    try {
      console.log('fetching ' + inputValue + ' from backend');
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
      console.error('Error fetching data:', error);
    }
  };

  const makeWordsClickable = () => {
    const words = response?.definicion?.split(' ');
    if (! words) {
      return (<span>Nada.</span>);
    }
    return words.map((word, index) => (
      <span
        key={index}
        className='clickable-word'
        onClick={() => {handleInputClick(word);definirData()}}
      >
        {word + (index === words.length - 1 ? '' : ' ')}
      </span>
    ));
  };

  return (
    <div>

    <p>
      {makeWordsClickable(JSON.stringify(response?.definicion, null, 2))}
    </p>
    
      <h1>Language Lilypad Button  Test</h1>
      <button onClick={fetchData}>Fetch Data from /definir</button>
        {response && (
          <div>
            <h2>Response from /definir:</h2>
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
      <h1>Language Lilypad Serch</h1>
        <div style={{ textAlign: "center", margin: "20px" }}>
          <input style={{height: "40px", color: "red"}} type="text" value={inputValue} onChange={handleInputChange} />
          <button onClick={definirData}>Call API</button>
        </div>
        <div style={{ textAlign: "center" }}>
          <p>API Result:</p>
          <p>{JSON.stringify(response, null, 2)}</p>
        </div>  
    </div>
  );
};



export default Home;