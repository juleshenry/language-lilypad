"use client";
import React, { useState } from 'react';

const Home = () => {
  const [response, setResponse] = useState(null);

  const fetchData = async () => {
    try {
      console.log('fetchin');
      let d = {'palabra' : 'sinsss'};
      const res = await fetch('http://localhost:3000/api/ghoul',
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

  return (
    <div>
      <h1>Next.js App</h1>
      <button onClick={fetchData}>Fetch Data from /api/boo</button>
      {response && (
        <div>
          <h2>Response from /api/boo:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default Home;