ultra-automation/
├── package.json
├── .env
├── src/
│   ├── index.js                 # Entry point + CLI
│   ├── core/
│   │   ├── browser-engine.js    # Puppeteer browser controller
│   │   ├── command-parser.js    # Natural language command parser
│   │   ├── task-runner.js       # Task orchestrator
│   │   └── download-manager.js  # Download handler
│   ├── modules/
│   │   ├── search.js            # Google/web search
│   │   ├── scraper.js           # Web scraping
│   │   ├── screenshot.js        # Screenshot capture
│   │   ├── form-filler.js       # Auto form fill
│   │   ├── file-downloader.js   # File download
│   │   └── data-extractor.js    # Data extraction
│   ├── dashboard/
│   │   ├── server.js            # Live dashboard server
│   │   ├── websocket.js         # Real-time updates
│   │   └── public/
│   │       ├── index.html       # Dashboard UI
│   │       ├── style.css        # Dashboard styles
│   │       └── app.js           # Dashboard frontend
│   └── utils/
│       ├── logger.js            # Colored console logger
│       ├── file-manager.js      # File I/O operations
│       └── config.js            # Configuration
└── output/                      # Auto-created output directory
    ├── downloads/
    ├── screenshots/
    ├── data/
    └── logs/
