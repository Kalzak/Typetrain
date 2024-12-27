import React, {useState} from 'react';
import TargetTextLabel from './TargetTextLabel';

import WordPassFailRate from './WordPassFailRate';
import LetterErrorRate from './LetterErrorRate';
import WeakSubstrings from './WeakSubstrings';

// Chart stuff
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

function AppNew() {

  const [text, setText] = useState('this is a test to see how well you are at typing and i hope you do well');
  const [stats, setStats] = useState({
    "lang_id": 1,
    "text_id": 1,
    "keystrokes": [],
  });
  const [startTime, setStartTime] = useState(0);
  const [doneText, setDoneText] = useState('');
  const [wrongText, setWrongText] = useState('');
  const [leftText, setLeftText] = useState('');
  const [wpm, setWpm] = useState('N/A');
  const [textEndpoint, setTextEndpoint] = useState("get-text");

  const onKeyPress = (key) => {
    if(startTime == 0) {
      setStartTime(Date.now());
    }

    let keypress_time = 0;

    let type = "append";

    if(startTime != 0) {
      keypress_time = Date.now() - startTime;
    }

    let stats_temp = stats

    let keystroke_data = {}

    if(key == "Backspace") {
      keystroke_data = {
        "type": "delete",
        "time": keypress_time,
      }
    } else {
      keystroke_data = {
        "type": "append",
        "time": keypress_time,
        "char": key,
      }
    }

    if(key == "Shift") {
      return;
    }

    //stats_temp.keystrokes.push({"key": key, "action": "down", "time": keypress_time})
    stats_temp.keystrokes.push(keystroke_data)

    setStats(stats_temp);

    console.log("D", key, keypress_time, keypress_time);
  }

  const onKeyRelease = (key) => {
    let keypress_time = 0;

    if(startTime != 0) {
      keypress_time = Date.now() - startTime;
    }

    let stats_temp = stats

    if(key == "Backspace") {
      key = "Key.backspace"
    }
    if(key == " ") {
      key = "Key.space"
    }
    // Added because my keyboard has custom binding for caps = backspace but x window server still 
    //   treats the "keyup" part as a capslock so pressing shift looks like down:shift up:capslock
    if(key == "CapsLock") {
      key = "Shift"
    }

    if(key == "Shift") {
      return;
    }

    //stats_temp.keystrokes.push({"key": key, "action": "up", "time": keypress_time})

    //setStats(stats_temp);

    console.log("U", key, keypress_time);
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
    setLeftText(text.substring(localDoneText.length + localWrongText.length, text.length));

    if(inputValue == text) {
      console.log("DONE");
      const serverUrl = 'http://localhost:4000/submitrace'; // Replace with your server URL and port
      console.log(stats)
      sendJsonData(stats, serverUrl);

      //fetchTextFromServer(null)
      const inputElement = document.getElementById('typed');
      inputElement.value = ''
      setDoneText('');
      setWrongText('');

      setStats({
        "lang_id": 1,
        "text_id": 1,
        "keystrokes": [],
      });

      setStartTime(0);

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

  return (
    <div>
      <form noValidate>
        <div className="grid gap-6 mb-6 p-2">
            <div>
                <TargetTextLabel text={leftText} doneText={doneText} wrongText={wrongText}/>
                <input onKeyDown={(char) => onKeyPress(char.key)} onKeyUp={(char) => onKeyRelease(char.key)} onChange={() => handleInputChange()} type="text" id="typed" className="bg-gray-50 border border-gray-300 text-gray-900 text-2xl rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Type here" required/>
            </div>
        </div>
      </form>
    </div>
  );
}


export default AppNew;
