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
          const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/es/${inputWord}`);
          const data = await response.json();

          if (Array.isArray(data) && data.length > 0) {
            const firstDefinition = data[0].meanings[0].definitions[0].definition;
            setOutputDefinition(firstDefinition);
          } else {
            setOutputDefinition('No definition found for the provided word.');
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
