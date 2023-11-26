"use client";
import React, { useState, useEffect } from 'react';

const Home = () => {
  const [response, setResponse] = useState(null);
  
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  useEffect(() => {
    // This code runs after the component has rendered and inputValue has been updated
    console.log('Input has become... ', inputValue,' ...!');
    definirData();
  }, [inputValue]); // The effect will run whenever inputValue changes

  const handleInputClick = async (word) => {
    console.log('Setting...', word,'... to inputValue');
    setInputValue(word);
    // console.log('Input has become... ', inputValue,' ...!');
    
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
        onClick={async () => {await handleInputClick(word);}}
      >
        {word + (index === words.length - 1 ? '' : ' ')}
      </span>
    ));
  };

  return (
    <div>
        <div style={{ textAlign: "center", margin: "20px" }}>
          <h1>Language Lilypad</h1>
          <h1>🪷🌺🐸🌺🪷</h1>
          <input style={{height: "40px", color: "red"}} type="text" value={inputValue} onChange={handleInputChange} />
          <button onClick={definirData}>Call API</button>
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

