const define_word = async (w) => {
  console.log(w);
  if (!w) {
    w = "undefined";
  }
  const response = await fetch('https://api.dictionaryapi.dev/api/v2/entries/en/'+w);
  const myJson = await response.json(); //extract JSON from the http response
  console.log(myJson[0]['meanings']);
  if (myJson[0]['meanings']) {
    myJson[0]['meanings'].forEach(function(data) {
      console.log(data['partOfSpeech']);
      data['definitions'].forEach(function(data2) {
        console.log(data2['definition'])
      });
    });
  }
  return myJson;
}

export function fetch_def(a) {
  // return define_word(a);
  return a + '!';
}