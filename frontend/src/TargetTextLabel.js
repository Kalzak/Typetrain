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
    <label id="target_text" class="block mb-2 text-4xl font-medium text-gray-900 dark:text-white">
      <span class="bg-green-400">{props.doneText}</span>
      <span class="bg-red-400">{props.wrongText}</span>
      <span>{props.text}</span>
    </label>
  );
}

export default TargetTextLabel;