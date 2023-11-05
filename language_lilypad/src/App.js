import React, { useState } from 'react';
// import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  }

  return (
    <div className="App">
      <div className="container d-flex align-items-center justify-content-center h-100">
        <div className="row">
          <div className="col-md-6 mx-auto">
            <div className="form-group">
              <input 
                type="text" 
                className="form-control" 
                placeholder="Enter your text" 
                value={inputValue}
                onChange={handleInputChange}
              />
            </div>
            <div className="mt-3">
              <p>User Input: {inputValue}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
