# Ideas

I want the structure to be a "backend" that takes json input and then processes that
But the question is, how do I want to present that json data?
I have two ideas right now...

A json file which is "per-word" and says how long each word took to complete, and if there was a typo then point out where that happened
    But what about typos where it should have been a space and you typed something else? Well it'd belong to the previous word caues ofc

Another approach is to literally have each one letter by letter, with timing between
It's definitely the most "data-rich" but would be much larger filesizes and also annoying to deal with
Yeah I think the structure could be:

For "Hello there this is a test"

```json

[
    [
        "word": "Hello",
        "time": 945,
        "mistake": {}
    ],
    [
        "word": "there",
        "time": 812,
        "mistake": {
            "index": 1,
            "typo": "e"
        }
    ],
    [
        "word": "this",
        "time": 743,
        "mistake": {
            "index": 0,
            "typo": "s"
        }
    ],
    [
        "word": "is",
        "time": 594,
        "mistake": {}
    ],
    [
        "word": "a",
        "time": 357,
        "mistake": {}
    ],
    [
        "word": "test",
        "time": 829,
        "mistake": {}
    ]
]

```

Hello tehre shis is a test
hello there

hello there this is a test

---

After talking with GPT I have some more ideas that I can work with...

Mainly I think I should be taking as much data as possible, keypress up and keypress down for each letter, then I guess on the local system I can process that right?
But could also have it be processed on the remote machine too, that would be nice 
Let's just have it process on server for now and just accept that json data of keystrokes plus the original text...
