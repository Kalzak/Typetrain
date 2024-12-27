import asyncio
from websockets.server import serve
from app import validate_jwt, random_text
import json
import time
import dbmodule

MAX_PLAYER_COUNT = 2
waiting_players = []
matches = []
ws_to_match = {}

async def handle_connection(websocket):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            message = json.loads(message)

            # If joining then add to waiting players
            if message["action"] == "join":
                # Check JWT token and extract username
                result = validate_jwt(message["token"])
                if result is None:
                    # If invalid then close the websocket
                    await websocket.send(json.dumps({"status": "invalid_token"}))
                    await websocket.close()
                    return
                username = result["sub"]
                # Add player to waiting players
                waiting_players.append({
                    "ws": websocket,
                    "uname": username,
                    "progress": 0
                })
                # Run matchmaking check to see if can start game
                await matchmake()
            
            # If submitting progress data then update match fields
            if message["action"] == "progress":
                # Get the match from the websocket
                match = ws_to_match[websocket]
                # Update the match with the progress data
                match["ws_to_player"][websocket]["progress"] = message["progress"]
                # Send the updated match data to the players
                await send_match_data(match)

            # If a user who has previously finished a game wants to play again
            if message["action"] == "newmatch":
                print("newmatching")
                # Get username before clearing
                username = match["ws_to_player"][websocket]["uname"]
                print("username", username)
                # Remove the websocket info from their previous match
                match = ws_to_match[websocket]
                del match["ws_to_player"][websocket]
                # Remove the websocket from match mapping
                del ws_to_match[websocket]
                # Put player back in waiting list
                waiting_players.append({
                    "ws": websocket,
                    "uname": username,
                    "progress": 0
                })
                # Send back a response
                await websocket.send(json.dumps({"status": "waiting"}))
                # Run matchmaking check to see if can start game
                await matchmake()
            
    except websockets.exceptions.ConnectionClosed:
        # Delete the map from websocket to match
        del ws_to_match[websocket]

async def send_game_found(match):
    # Send all the one-time things that need to be send at match start
    # Including the text to be typed, and players in match
    for current_player in match["ws_to_player"].values():
        await current_player["ws"].send(json.dumps({
            "status": "gamefound",
            "text": match["text"],
            "unames": [
                player["uname"]
                for player in match["ws_to_player"].values()
            ]
        }))

async def send_match_data(match):
    # We only can track usernames and progress data for now so send that
    players = match["ws_to_player"].values()
    match_data = {
        "status": "matchdata",
        "unames": [player["uname"] for player in players],
        "progress": [match["ws_to_player"][player["ws"]]["progress"] for player in players]
    }
    for player in players:
        await player["ws"].send(json.dumps(match_data))

async def matchmake_loop():
    while True:
        if len(waiting_players) != 0: 
            await matchmake()
        await asyncio.sleep(5)

async def cleaner_loop():
    while True:
        # 
        await asyncio.sleep(5)

async def matchmake():
    # Basic matchmaking for now, if enough players then put them in a game
    global waiting_players
    print("Matchmaking", waiting_players)
    if len(waiting_players) >= MAX_PLAYER_COUNT:
        # Get the players and remove them from waiting list
        players = waiting_players[:MAX_PLAYER_COUNT]
        waiting_players = waiting_players[MAX_PLAYER_COUNT:]
        # Create the match
        await new_match(players)
        print("Matchmade")

async def new_match(players):
        text = dbmodule.get_random_text()

        match = {
            "ws_to_player": {player["ws"]: player for player in players},
            "creation_time": time.time(),
            "text": text
        }
        # Use websocket to map connection to match
        for player in players:
            ws_to_match[player["ws"]] = match
        # Add match to list of all matches
        matches.append(match)
        # Send the match data to the players
        await send_game_found(match)

async def main():
    server = serve(handle_connection, "localhost", 5005)
    await asyncio.gather(
        server,
        matchmake_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())