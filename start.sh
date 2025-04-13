#!/bin/bash

# Start the Node.js server in the background
node interface/Backend/server.js &

# Wait for the server to initialize
sleep 3

# Start the HTTP server for the frontend
http-server -p 8080 &

# Keep the container running
tail -f /dev/null