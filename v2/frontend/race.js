const WS_URL = "ws://localhost:5005/game";

let socket;
let text = "";
let typed = "";
let error = "";
let untyped = "";
let stats = [];
let starttime = 0;
let finished = false;

document.getElementById("input").addEventListener("keydown" , (event) => {
    handleKeyInteraction("down", event.key);
});

document.getElementById("input").addEventListener("keyup" , (event) => {
    handleKeyInteraction("up", event.key);
});

function handleKeyInteraction(movement, key) {
    let action = "";
    let timedelta = 0;

    if(starttime === 0) {
        starttime = Date.now();
    } else {
        timedelta = Date.now() - starttime;
    }

    // Handle special keys (modifiers, backspace, etc.)
    // These are stored in a separate "action" variable
    // If detected will supersede the key variable
    if(key === "Backspace") {
        if(movement === "down") {
            if(error.length != 0) {
                error = error.slice(0, -1);
            } else if(typed.length != 0) {
                untyped = typed.slice(-1) + untyped;
                typed = typed.slice(0, -1);
            }
        }
        action = "backspace";
    }
    if(key === "Shift") {
        action = "shift";
    }
    if(key === "Alt") {
        action = "alt";
    }   
    // Because of my weird keyboards, convert capslock to shift
    if(key === "CapsLock") {
        action = "shift";
    }

    // Track stats
    // k = key, a = action, m = movement, d = timedelta
    stats.push({
        k: action === "" ? key : "",
        a: action,
        m: movement === "down" ? "d" : "u",
        d: timedelta,
    });

    if (movement === "down") {
        // Update typed/error/untyped
        if(action === "") {
            // If there is already an error then add to error string
            if(error.length !== 0) {
                // If incorrect then add to error string
                error += key;
            } else {
                // Otherwise check that char is correct
                if(key === untyped[0]) {
                    typed += key;
                } else {
                    // If incorrect then add to error string
                    error += key;
                }
            }
        }

        // Send progress to server
        socket.send(JSON.stringify({
            action:"progress", 
            progress: Math.floor((typed.length / text.length) * 100 )
        }));

        // If everything is typed correctly
        if(typed === text) {
            // Send stats to server
            if(socket) {
                payload = JSON.stringify({action:"stats", stats: stats});
                socket.send(payload);
            }

            // Disable input and update text cause letter missing otherwise
            document.getElementById("input").textContent = text;
            document.getElementById("input").disabled = true;

            document.getElementById("joinrace").textContent = "Join new race";
            finished = true;
        }

        // Update untyped and error
        error = text.slice(typed.length, typed.length + error.length);
        untyped = text.slice(typed.length + error.length);

        // Update display
        updateDisplay();
    }

    console.log(stats[stats.length - 1]);
}

document.getElementById("joinrace").addEventListener("click", () => {
    if(socket) {
        if(finished === true) {
            // Reset everything
            text = "";
            typed = "";
            error = "";
            untyped = "";
            stats = [];
            starttime = 0;
            finished = false;
            updateDisplay();
            document.getElementById("input").disabled = false;
            document.getElementById("input").value = "";
            socket.send(JSON.stringify({action: "newmatch"}));
        } else {
            alert("Already connected to a race!");
            return
        }
    } else {
        socket = new WebSocket(WS_URL); 
    }

    socket.onopen = () => {
        document.getElementById("status").textContent = "Waiting for match";
        socket.send(JSON.stringify({action:"join",token:localStorage.getItem("token")}));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Message from server:", data);
        
        if(data.status === "matchdata") {
            updateProgress(data.unames, data.progress);
        }

        if(data.status === "gamefound") {
            document.getElementById("status").textContent = "Game starting";
            text = data.text;
            untyped = data.text;
            updateDisplay();
            updateProgress(data.unames, new Array(data.unames.length).fill(0));
        }
    };

    socket.onerror = (error) => {
        console.error("Websocket error:", error);
        document.getElementById("status").textContent = "Connection error";
    };

    socket.onclose = () => {
        document.getElementById("status").textContent = "Disconnected";
        socket = null;
    };
});

function updateDisplay() {
    document.getElementById("typed").textContent = typed;
    document.getElementById("error").textContent = error;
    document.getElementById("untyped").textContent = untyped;
}

function updateProgress(unames, progress) {
    playerlist = document.getElementById("matchdata")

    for (let i = 0; i < unames.length; i++) {
        li = document.getElementById(`player${i}`)
        if(!li) {
            li = document.createElement("li");
            li.id = `player${i}`;
            li.style.fontFamily = "monospace";
            playerlist.appendChild(li);
        }
        li.textContent = `${unames[i]}`

        const MAX_LENGTH = 50;
        const dashrepeat = Math.floor((progress[i] / 100) * MAX_LENGTH);
        const dotrepeat = MAX_LENGTH - dashrepeat;
        li.innerHTML += `<br/>${'-'.repeat(dashrepeat)}${'.'.repeat(dotrepeat)}`;

        if(progress[i] === 100) {
            li.innerHTML += " finished"
        }
    }
}