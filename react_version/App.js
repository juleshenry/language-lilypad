// import React, { useState } from 'react';
// import './App.css';


// function App() {
//   const [inputValue, setInputValue] = useState('');
    

//   const handleInputChange = (e) => {
//     setInputValue(e.target.value);
//   }
  
//   return (
//     <div className="App">
//       <div className="container d-flex align-items-center justify-content-center h-100">
//         <div className="row">
//           <div className="col-md-6 mx-auto">
//             <div className="form-group">
//               <input 
//                 type="text" 
//                 className="form-control" 
//                 placeholder="Enter your text" 
//                 value={inputValue}
//                 onChange={handleInputChange}
//               />
//             </div>
//             <div className="mt-3">
//               <p>User Input: {inputValue}</p>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;
import React, { useState, useEffect } from 'react';

function MyComponent() {
  const [inputWord, setInputWord] = useState('');
  const [outputDefinition, setOutputDefinition] = useState('');

  const handleInputChange = (e) => {
    setInputWord(e.target.value);
  };

  useEffect(() => {
    const callApi = async () => {
      try {
        if (inputWord.trim() !== '') {
          const response = await fetch('http://localhost:3001/definir', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ palabra: inputWord }), // Include the term parameter in the request body
          });
    
          const data = await response.json();
          console.log(data);
          // if (Array.isArray(data) && data.length > 0) {
          //   console.log(data);
          //   const firstDefinition = data[0].definicion;
            
          // } else {
          //   setOutputDefinition('No definition found');
          // }
          setOutputDefinition(data?.definicion || 'no definición');
        }
      } catch (error) {
        console.error('Error:', error);
        setOutputDefinition('An error occurred while calling the API.');
      }
    };

    callApi();
  }, [inputWord]);

  return (
    <div>
      <input
        type="text"
        value={inputWord}
        onChange={handleInputChange}
      />
      {outputDefinition && <div>Definition: {outputDefinition}</div>}
    </div>
  );
}

export default MyComponent;
