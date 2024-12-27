function process_race(race) {
    // Load the text
    const text = mock_load_text(race.lang_id, race.text_id);
    
    const analysis = analyze_race(race.keystrokes, text);

    return analysis;
}

function analyze_race(keystrokes, text) {

    let final_text = text.split('');
    let typed_text = [];
    let failed_letter_indexes = [];
    let keystroke_times = [];
    let in_fail_path = false;
    let fail_index = null;

    // If the first keystroke is not an append then keystrokes are invalid
    if (keystrokes[0].type !== "append") {
        throw "invalid_keystrokes";
    }

    for (let i = 0; i < keystrokes.length; i++) {
        const type = keystrokes[i].type;
        const time = keystrokes[i].time;
        const char = keystrokes[i].char;
        let time_diff;

        switch (type) {
            case "append":
                // Push character to typed text
                typed_text.push(char);

                // Calculate time diff between last keystroke
                if (typed_text.length == 1) {
                    time_diff = time;
                } else {
                    time_diff = time - keystrokes[i - 1].time;
                }

                // Push time diff to keystroke times
                keystroke_times.push(time_diff);

                // If not already in fail path
                if (in_fail_path == false) {
                    // If typed letter is incorrect
                    if (char != final_text[typed_text.length - 1]) {
                        failed_letter_indexes.push(typed_text.length - 1);
                        in_fail_path = true;
                    }
                } else {
                    // Otherwise we are in fail path
                }

                break;

            case "delete":
                // Handle people deleting at start
                if (typed_text.length == 0) {
                    continue;
                }

                // Remove character from typed text
                typed_text.pop();

                // Remove time diff from keystroke times
                keystroke_times.pop();

                // If we are in fail path check if we are out of it
                if (in_fail_path == true) {
                    if (typed_text.length == failed_letter_indexes[failed_letter_indexes.length - 1]) {
                        in_fail_path = false;
                    }
                }

                break;

            // This is for languages like japanese where one input changes character instead of appending
            // Like you type three letters and suddenly you get some special japanese kanji character
            case "change":
                throw "unsupported";
                
                break;
        }
    }

    // Ensure that final result is the desired text
    if(typed_text.join("") != text) {
        throw "invalid_keystrokes";
    }

    // Calculate letter accuracy
    let letter_accuracy = {};
    for (let i = 0; i < typed_text.length; i++) {
        const char = typed_text[i];
        const was_incorrect = failed_letter_indexes.includes(i);
        if (!(char in letter_accuracy)) {
            letter_accuracy[char] = {
                "fail": 0,
                "pass": 0,
            }
        }
        if (was_incorrect == true) {
            letter_accuracy[char].fail += 1;
        } else {
            letter_accuracy[char].pass += 1;
        }
    }

    // Calculate word accuracy
    let word_accuracy = {};
    const words = text.split(" ");
    let word_counter = 0;
    let cumulative_word_length = 0;
    let word_fail = false;
    for (let i = 0; i < typed_text.length; i++) {
        // If we failed a letter in this word mark as failed
        if (failed_letter_indexes.includes(i) == true) {
            word_fail = true;
        }

        // When done with this word
        if (cumulative_word_length + words[word_counter].length == i + 1) {

            // Add to word accuracy dict if not already present
            if (!(words[word_counter] in word_accuracy)) {
                word_accuracy[words[word_counter]] = {
                    "fail": 0,
                    "pass": 0,
                }
            }
            
            // If word failed increment fail, otherwise increment pass
            if (word_fail == true) {
                word_accuracy[words[word_counter]].fail += 1;
            } else {
                word_accuracy[words[word_counter]].pass += 1;
            }
            
            cumulative_word_length += words[word_counter].length + 1;
            word_counter += 1;
            word_fail = false;
        }
    }

    // Calculate potential time
    let potential_time = 0;
    for (let i = 0; i < keystroke_times.length; i++) {
        potential_time += keystroke_times[i];
    }

    // Calculate other stats
    const word_count = text.split(" ").length;
    const actual_time = keystrokes[keystrokes.length - 1].time;
    const actual_cpm = Math.ceil((text.length / actual_time) * 60000);
    const potential_cpm = Math.ceil((text.length / potential_time) * 60000);
    const actual_wpm = Math.ceil((word_count / actual_time) * 60000);
    const potential_wpm = Math.ceil((word_count / potential_time) * 60000);

    return {
        "actual_time": actual_time,
        "actual_cpm": actual_cpm,
        "potential_time": potential_time,
        "potential_cpm": potential_cpm,
        "actual_wpm": actual_wpm,
        "potential_wpm": potential_wpm,
        "letter_accuracy": letter_accuracy,
        "word_accuracy": word_accuracy,
    }
}


function mock_load_text(lang_id, text_id) {
    return "this is a test to see how well you are at typing and i hope you do well";
}

sample_data_1 = {
    "lang_id": 1,
    "text_id": 1,
    "keystrokes": [
        {
            "type": "append",
            "time": 111,
            "char": "h"
        },
        {
            "type": "append",
            "time": 222,
            "char": "e"
        },
        {
            "type": "append",
            "time": 333,
            "char": "l"
        },
        {
            "type": "append",
            "time": 444,
            "char": "l"
        },
        {
            "type": "append",
            "time": 555,
            "char": "o"
        },
    ]
}

sample_data_2 = {
    "lang_id": 1,
    "text_id": 1,
    "keystrokes": [
        {
            "type": "append",
            "time": 111,
            "char": "h"
        },
        {
            "type": "append",
            "time": 222,
            "char": "e"
        },
        {
            "type": "append",
            "time": 333,
            "char": "l"
        },
        {
            "type": "append",
            "time": 444,
            "char": "l"
        },
        {
            "type": "append",
            "time": 555,
            "char": "a"
        },
        {
            "type": "delete",
            "time": 666,
        },
        {
            "type": "append",
            "time": 777,
            "char": "o"
        },
        {
            "type": "append",
            "time": 888,
            "char": " "
        },
        {
            "type": "append",
            "time": 999,
            "char": "w"
        },
        {
            "type": "append",
            "time": 1111,
            "char": "o"
        },
        {
            "type": "append",
            "time": 1222,
            "char": "c"
        },
        {
            "type": "append",
            "time": 1333,
            "char": "/"
        },
        {
            "type": "delete",
            "time": 1444,

        },
        {
            "type": "delete",
            "time": 1555,
        },
        {
            "type": "append",
            "time": 1666,
            "char": "r"
        },
        {
            "type": "append",
            "time": 1777,
            "char": "l"
        },
        {
            "type": "append",
            "time": 1888,
            "char": "d"
        }
    ]
}

//let result = process_race(sample_data_2);
//console.log(result);

module.exports = {
    process_race
}