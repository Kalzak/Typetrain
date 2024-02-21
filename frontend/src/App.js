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

function App() {

  const [text, setText] = useState('init');
  const [stats, setStats] = useState({});
  const [startTime, setStartTime] = useState(0);
  const [doneText, setDoneText] = useState('');
  const [wrongText, setWrongText] = useState('');
  const [leftText, setLeftText] = useState('');
  const [wpm, setWpm] = useState('N/A');
  const [textEndpoint, setTextEndpoint] = useState("get-text");

  const [wpmStatsOptions, setWpmStatsOptions] = useState({
    scales: {
      x: {
        display: false
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'WPM',
        },
      },
    },
  });
  const [wpmStatsData, setWpmStatsData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Potential',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        fill: false,
        pointRadius: 0
      },
    ],
  });
  const [wpmRecentStatsOptions, setWpmRecentStatsOptions] = useState({
    animation: {
      easing: 'easeInQuad', // Use the ease-in easing function
    },
    scales: {
      x: {
        display: false
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'WPM',
        },
      },
    },
  });
  const [wpmRecentStatsData, setWpmRecentStatsData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Potential',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        fill: false,
        pointRadius: 0
      },
    ],
  });
  const [wpmRollingStatsOptions, setWpmRollingStatsOptions] = useState({
    animation: {
      easing: 'easeInQuad', // Use the ease-in easing function
    },
    scales: {
      x: {
        display: false
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'WPM',
        },
      },
    },
  });
  const [wpmRollingStatsData, setWpmRollingStatsData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Potential',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        fill: false,
        pointRadius: 0
      },
    ],
  });

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );


  const calculateWpm = () => {
    if(startTime == 0) {
      setWpm(0);
    }
    let timePassed = Date.now() - startTime;

    let cpm = (doneText.length / timePassed) * 60000;

    setWpm(Math.floor(cpm / 5));
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

    if(key == "Backspace") {
      key = "Key.backspace"
    }
    if(key == " ") {
      key = "Key.space"
    }
    if(key == "Shift") {
      return;
    }

    stats_temp.keystrokes.push({"key": key, "action": "down", "time": keypress_time})

    setStats(stats_temp);

    calculateWpm();

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

    stats_temp.keystrokes.push({"key": key, "action": "up", "time": keypress_time})

    setStats(stats_temp);

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
      const serverUrl = 'http://localhost:8000'; // Replace with your server URL and port
      sendJsonData(stats, serverUrl);

      fetchTextFromServer(null)
      const inputElement = document.getElementById('typed');
      inputElement.value = ''
      setDoneText('');
      setWrongText('');

      updateWpmGraph();
      
    }
  }

  const sendJsonData = (jsonData, serverUrl) => {
    if(textEndpoint != "get-text") {
      console.log("not sending data");
      return;
    }
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
    
    fetch('http://localhost:5000/' + textEndpoint)
      .then(response => response.json())
      .then(data => {
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
    
    setStartTime(0);
    if(event != null)
    {
      const inputElement = document.getElementById('typed');
      inputElement.value = ''
    }
    setDoneText('');
    setWrongText('');

  }

  const updateWpmGraph = (event) => {
    if(event != null) {
      event.preventDefault();
    }

    fetch('http://127.0.0.1:44444/wpm')
    .then(response => response.json())
    .then(data => {
      const resultArray = [...Array(data.p_wpm.length).keys()].map(num => num + 1);
      setWpmStatsData({
        labels: resultArray,
        datasets: [
          {
            label: 'Potential',
            data: data.p_wpm,
            borderColor: "rgba(173, 26, 26, 1)",
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
          {
            label: 'Actual',
            data: data.a_wpm,
            borderColor: 'rgba(10, 41, 207, 1)',
            borderWidth: 1,
            fill: false,
            pointRadius: 0,
          },
        ],
      }
      );
    })
    .catch(error => {
      console.error('Error fetching wpm data:', error);
    });
  }

  const updateWpmRecentGraph = (event) => {
    if(event != null) {
      event.preventDefault();
    }

    fetch('http://127.0.0.1:44444/wpm-recent')
    .then(response => response.json())
    .then(data => {
      const resultArray = [...Array(data.p_wpm.length).keys()].map(num => num + 1);
      setWpmRecentStatsData({
        labels: resultArray,
        datasets: [
          {
            label: 'Potential',
            data: data.p_wpm,
            borderColor: "rgba(173, 26, 26, 1)",
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
          },
          {
            label: 'Actual',
            data: data.a_wpm,
            borderColor: 'rgba(10, 41, 207, 1)',
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
          },
        ],
      }
      );
    })
    .catch(error => {
      console.error('Error fetching wpm data:', error);
    });
  }

  const updateWpmRollingGraph = (event) => {
    if(event != null) {
      event.preventDefault();
    }

    fetch('http://127.0.0.1:44444/wpm-rolling-average')
    .then(response => response.json())
    .then(data => {
      const resultArray = [...Array(data.p_wpm.length).keys()].map(num => num + 1);
      setWpmRollingStatsData({
        labels: resultArray,
        datasets: [
          {
            label: 'Potential',
            data: data.p_wpm,
            borderColor: "rgba(173, 26, 26, 1)",
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
          },
          {
            label: 'Actual',
            data: data.a_wpm,
            borderColor: 'rgba(10, 41, 207, 1)',
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
          },
        ],
      }
      );
    })
    .catch(error => {
      console.error('Error fetching wpm data:', error);
    });
  }

  const updateAllGraphs = (event) => {
    updateWpmGraph(event);
    updateWpmRecentGraph(event);
    updateWpmRollingGraph(event);
  }

  if(text == "init") {
    fetchTextFromServer(null);
    updateAllGraphs(null);
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
      <span>
        <p className="inline text-2xl m-2">WPM: {wpm}</p>
        <button onClick={(event) => fetchTextFromServer(event)} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Get new text</button>
        <button onClick={(event) => updateAllGraphs(event)} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Update graphs</button>
        <button onClick={(event) => setTextEndpoint("get-llm-text")} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">LLM Mode</button>
        <button onClick={(event) => setTextEndpoint("get-text")} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Typeracer Mode</button>
        <button onClick={(event) => setTextEndpoint("get-weak-substrings")} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">WeakSubstring Mode</button>
        <button onClick={(event) => setTextEndpoint("get-weak-substring-words")} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">WeakSubstringWord Mode</button>
        <button onClick={(event) => setTextEndpoint("get-low-cpm-words")} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">LowCPM Mode</button>
        <button onClick={(event) => setTextEndpoint("get-high-cpm-words")} className="m-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-2xl w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">HighCPM Mode</button>
      </span>
    
      <div className="flex">
        <div className="w-1/3">
          <Line data={wpmStatsData} options={wpmStatsOptions} />
        </div>
        <div className="w-1/3">
          <Line data={wpmRecentStatsData} options={wpmRecentStatsOptions} />
        </div>
        <div className="w-1/3">
          <Line data={wpmRollingStatsData} options={wpmRollingStatsOptions} />
        </div>
      </div>
      <div className="flex">
        <div className="w-1/3">
          <WordPassFailRate text={text}/>
        </div>
        <div className="w-1/3">
          <LetterErrorRate text={text}/>
        </div>
        <div>
          <WeakSubstrings text={text}/>
        </div>
      </div>
    </div>
  );
}

export default App;
