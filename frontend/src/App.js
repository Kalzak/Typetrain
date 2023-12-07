import React, {useState} from 'react';
import TargetTextLabel from './TargetTextLabel';

function App() {
  
  let target_type = "here is a text for you to type";
  const [text, setText] = useState('init');
  const [stats, setStats] = useState({});
  const [startTime, setStartTime] = useState(0);
  const [doneText, setDoneText] = useState('');
  const [wrongText, setWrongText] = useState('');
  const [leftText, setLeftText] = useState('');

  const printChar = (char) => {
    console.log(char);
  }

  const onKeyPress = (key) => {
    if(startTime == 0) {
      setStartTime(Date.now());
    }

    let keypress_time = 0;

    if(startTime != 0) {
      keypress_time = Date.now() - startTime;
    }

    let stats_temp = stats

    stats_temp.keystrokes.push({"key": key, "action": "down", "time": keypress_time})

    setStats(stats_temp);

    console.log("UP", key, keypress_time);
  }

  const onKeyRelease = (key) => {
    let keypress_time = 0;

    if(startTime != 0) {
      keypress_time = Date.now() - startTime;
    }

    let stats_temp = stats

    stats_temp.keystrokes.push({"key": key, "action": "up", "time": keypress_time})

    setStats(stats_temp);

    console.log("UP", key, keypress_time);
  }

  const handleInputChange = () => {
    let localDoneText = ''
    let localWrongText = ''

    const inputElement = document.getElementById('typed');
    const inputValue = inputElement.value;

    let len = inputValue.length;
    for(let i = 0; i < inputValue.length; i++) {
      if(localWrongText.length > 0) {
        localWrongText += text[i];
        continue;
      }

      if(inputValue[i] == text[i]) {
        localDoneText += text[i];
        continue;
      }
      if(inputValue[i] != text[i]) {
        localWrongText += text[i];
        continue;
      }
    }

    setDoneText(localDoneText);
    setWrongText(localWrongText);
    let bothLength = localDoneText.length + localWrongText.length;
    setLeftText(text.substring(localDoneText.length + localWrongText.length, text.length));

    if(inputValue == text) {
      console.log("DONE");
      const serverUrl = 'http://localhost:8000'; // Replace with your server URL and port
      sendJsonData(stats, serverUrl);

      fetchTextFromServer(null)
      const inputElement = document.getElementById('typed');
      inputElement.value = ''
      setDoneText('');
      setWrongText('');
    }

  }

  const sendJsonData = (jsonData, serverUrl) => {
    fetch(serverUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  }

  const fetchTextFromServer = (event) => {
    
    if(event != null) {
      event.preventDefault();
    }

    setText("loading");
    setLeftText("loading");
    
    fetch('http://localhost:5000/get-text')
      .then(response => response.json())
      .then(data => {
        console.log(data.text);
        // Do something with the text
        setText(data.text)
        setLeftText(data.text);
        let initialJson = {
          "sentence": data.text,
          "keystrokes": [],
        };
        setStats(initialJson);
      })
      .catch(error => {
        console.error('Error fetching text:', error);
      });
  }

  if(text == "init") {
    fetchTextFromServer(null);
  }
  
  return (
    <div>
      <form>
        <div class="grid gap-6 mb-6 p-2">
            <div>
                <TargetTextLabel text={leftText} doneText={doneText} wrongText={wrongText}/>
                <input onKeyDown={(char) => onKeyPress(char.key)} onKeyUp={(char) => onKeyRelease(char.key)} onChange={() => handleInputChange()} type="text" id="typed" class="bg-gray-50 border border-gray-300 text-gray-900 text-2xl rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Type here" required/>
            </div>
        </div>
        <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
        <button onClick={(event) => fetchTextFromServer(event)} class="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Get new text</button>
    </form>
    </div>
  );
}

export default App;
