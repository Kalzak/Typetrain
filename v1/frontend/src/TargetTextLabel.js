import React, { useState, useEffect } from 'react';

function TargetTextLabel(props) {
  /*
  const [text, setText] = useState('Default Text');

  useEffect(() => {
    // Simulate a delay and then update the text
    setTimeout(() => {
      setText('newtext');
    }, 1000); // Change text after 1 second
  }, []); // Empty dependency array means this runs once after the initial render
  */

  return (
    <div className="bg-gray-200 h-[15rem]">
      <label id="target_text" className="2block mb-2 text-4xl font-medium text-gray-900 dark:text-white">
        <span className="bg-green-400">{props.doneText}</span>
        <span className="bg-red-400">{props.wrongText}</span>
        <span>{props.text}</span>
      </label>
    </div>

  );
}

export default TargetTextLabel;