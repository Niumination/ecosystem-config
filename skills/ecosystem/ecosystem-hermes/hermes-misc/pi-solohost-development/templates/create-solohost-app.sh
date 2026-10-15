#!/bin/bash
# SoloHost App Template Generator
# Usage: ./create-solohost-app.sh "My App Name"

APP_NAME=${1:-"my-solohost-app"}
APP_DIR="$HOME/SoloHostApps/$APP_NAME"

echo "=== Creating SoloHost App Template ==="
echo "App: $APP_NAME"
echo "Dir: $APP_DIR"
echo ""

# Create directory structure
mkdir -p "$APP_DIR"/{assets,src,docs,data}

# Create Dockerfile
cat > "$APP_DIR/Dockerfile" << 'DOCKERFILE'
# syntax=docker/dockerfile:1
FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8080
ENV PORT=8080
ENV NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://localhost:8080/health').then(r => r.ok ? process.exit(0) : process.exit(1)).catch(() => process.exit(1))"

CMD ["node", "dist/main.js"]
DOCKERFILE

# Create manifest.json
cat > "$APP_DIR/manifest.json" << MANIFEST
{
  "version": "1.0.0",
  "name": "$APP_NAME",
  "description": "Local app for Pi Desktop SoloHost",
  "author": "your-pi-account",
  "license": "MIT",
  "tags": ["ai", "local", "productivity"],
  "min_node_version": "0.6.2",
  "containers": [
    {
      "name": "main",
      "image": "${APP_NAME}:latest",
      "ports": [
        {"container": 8080, "host": 8080}
      ],
      "volumes": [
        {"name": "data", "path": "/app/data"}
      ],
      "environment": {
        "PORT": "8080",
        "NODE_ENV": "production"
      }
    }
  ],
  "permissions": {
    "filesystem": ["read", "write"],
    "network": ["outbound"],
    "process": ["execute"]
  }
}
MANIFEST

# Create README
cat > "$APP_DIR/README.md" << README
# $APP_NAME — SoloHost App

Local application for Pi Network SoloHost.

## Features
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

## Installation

### Build
\`\`\`bash
docker build -t ${APP_NAME}:latest .
\`\`\`

### Run Locally
\`\`\`bash
docker run -p 8080:8080 -v \$(pwd)/data:/app/data ${APP_NAME}:latest
\`\`\`

### Install to Pi Desktop
1. Open Pi Desktop
2. Go to SoloHost tab
3. Click "Install from Local"
4. Select this directory

## Project Structure
\`\`\`
$APP_NAME/
├── Dockerfile
├── manifest.json
├── README.md
├── src/
├── assets/
└── docs/
\`\`\`

## Resources
- [SoloHost Docs](https://minepi.com/blog/pi2day2026/)
- [Pi Developer Forum](https://forum.minepi.com/)
README

# Create source entry point
mkdir -p "$APP_DIR/src"
cat > "$APP_DIR/src/main.js" << 'SRC'
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8080;
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, '../data');

if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
  if (req.method === 'GET' && req.url === '/') {
    res.end(JSON.stringify({
      name: '$APP_NAME',
      version: '1.0.0',
      status: 'running',
      solohost: true
    }));
  } else if (req.method === 'GET' && req.url === '/health') {
    res.end(JSON.stringify({ healthy: true, uptime: process.uptime() }));
  } else {
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(\`$APP_NAME running on port \${PORT}\`);
  console.log(\`Data directory: \${DATA_DIR}\`);
});
SRC

# Create package.json
cat > "$APP_DIR/package.json" << 'PKGJSON'
{
  "name": "solohost-app",
  "version": "1.0.0",
  "description": "SoloHost app template",
  "main": "src/main.js",
  "scripts": {
    "start": "node src/main.js",
    "build": "echo 'No build step required'"
  },
  "dependencies": {},
  "engines": {
    "node": ">=20.0.0"
  }
}
PKGJSON

# Create placeholder assets
touch "$APP_DIR/assets/.gitkeep"

echo ""
echo "✅ Template created at: $APP_DIR"
echo ""
echo "Next steps:"
echo "  1. cd $APP_DIR"
echo "  2. Edit manifest.json (update name, description, author)"
echo "  3. Add your source code to src/"
echo "  4. Build: docker build -t $APP_NAME:latest ."
echo "  5. Test: docker run -p 8080:8080 $APP_NAME:latest"
echo "  6. Install to Pi Desktop via SoloHost tab"
echo ""
