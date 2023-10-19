#!/bin/bash

# This function will be executed when you press CTRL+C or on script exit.
terminate_processes() {
    # Kill all background jobs (python scripts in this case)
    kill $(jobs -p)
}

# Set the trap
trap terminate_processes SIGINT SIGTERM EXIT

# Start your python scripts in the background
python3 graph/graph_wpm.py 2>/dev/null &
python3 graph/graph_success_cpm.py 2>/dev/null &
python3 graph/graph_fail_success_ratio.py 2>/dev/null &
python3 graph/graph_letter_errors.py 2>/dev/null &
python3 graph/graph_wpm_rolling_average_2.py 2>/dev/null &
# ... add as many as needed

# Wait forever, until the script receives SIGINT (CTRL+C) or EXIT
python3 server.py &
sleep 1
python3 client2.py

