# Use Node.js 16 as the base image
FROM node:16

# Install Python, pip, Nginx, and BLAS/LAPACK libraries
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nginx \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to where server.js is located
WORKDIR /app/interface/Backend

# Copy package.json and package-lock.json (if present) for Node.js dependencies
COPY interface/Backend/package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the entire project to /app
COPY . /app

# Install Python dependencies (if requirements.txt exists)
RUN pip3 install --no-cache-dir -r /app/requirements.txt
WORKDIR /app/
# Configure Nginx to serve index.html from /app/interface on port 8080
RUN echo "server {\n    listen 8080;\n    root /app/interface;\n    index index.html;\n}" > /etc/nginx/sites-enabled/default

# Expose ports 3000 (Node.js server) and 8080 (Nginx for index.html)
EXPOSE 3000 8080

# Start Nginx in the background and Node.js server in the foreground
CMD ["sh", "-c", "nginx & node interface/Backend/server.js"]