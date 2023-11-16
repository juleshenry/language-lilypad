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
const { Sequelize } = require('sequelize');


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
          const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/es/${inputWord}`);
          const data = await response.json();

          if (Array.isArray(data) && data.length > 0) {
            const firstDefinition = data[0].meanings[0].definitions[0].definition;
            setOutputDefinition(firstDefinition);
          } else {
            setOutputDefinition('No definition found');
          }
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
