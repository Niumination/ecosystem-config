# 🚀 Ultra Automation Dashboard - Full Functional Build

## Setup untuk Hackintosh macOS Tahoe 26.5 - ThinkPad X13 Yoga Gen 1

### Spesifikasi Target:

text

```
Machine   : Lenovo ThinkPad X13 Yoga Gen 1
CPU       : Intel Core i5-10310U (Comet Lake)
OS        : macOS Tahoe 26.5 (Hackintosh)
Tool      : opencode zen + model big pickle
Runtime   : Node.js + Puppeteer (Chromium)
```

---

## Struktur Project Final

text

```
ultra-automation/
├── package.json
├── .env
├── setup.sh                          # Auto installer
├── src/
│   ├── index.js                      # Main entry CLI
│   ├── core/
│   │   ├── browser-engine.js         # Puppeteer controller
│   │   ├── command-parser.js         # NLP command parser
│   │   ├── task-runner.js            # Task orchestrator
│   │   └── pipeline.js              # Pipeline executor
│   ├── modules/
│   │   ├── search.js                # Google search
│   │   ├── scraper.js               # Web scraper
│   │   ├── extractor.js             # Data extractor
│   │   ├── downloader.js            # File downloader
│   │   ├── screenshot.js            # Screenshot engine
│   │   └── monitor.js               # Page monitor
│   ├── server/
│   │   ├── app.js                   # Express + WS server
│   │   ├── routes.js                # API routes
│   │   └── websocket.js             # Real-time WS
│   ├── utils/
│   │   ├── config.js                # Configuration
│   │   ├── logger.js                # Live logger
│   │   └── files.js                 # File manager
│   └── dashboard/
│       └── index.html               # FULL dashboard UI
└── output/
    ├── downloads/
    ├── screenshots/
    ├── data/
    └── logs/
```

---

## 1. Auto Setup Script

Bash

```
#!/bin/bash
# setup.sh - Auto installer untuk macOS Tahoe Hackintosh

set -e

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║   🚀 Ultra Automation - Auto Setup            ║"
echo "║   macOS Tahoe 26.5 · ThinkPad X13 Yoga Gen1  ║"
echo "║   Intel i5-10310U · Hackintosh                ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Check Node.js
if ! command -v node &>/dev/null; then
    echo "⚠️  Node.js not found. Installing via Homebrew..."
    if ! command -v brew &>/dev/null; then
        echo "📦 Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install node
fi

NODE_VER=$(node -v)
echo "✅ Node.js: $NODE_VER"

# Create project
echo ""
echo "📁 Setting up project structure..."

mkdir -p output/{downloads,screenshots,data,logs}
mkdir -p src/{core,modules,server,utils,dashboard}

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Chromium fix for Hackintosh (Intel iGPU)
echo ""
echo "🔧 Applying Hackintosh Chromium patches..."
echo "   - Disabling GPU sandbox (Intel UHD 620)"
echo "   - Setting software rendering fallback"

# Create launch helper
cat > launch.sh << 'LAUNCH'
#!/bin/bash
# Hackintosh-optimized launch
export PUPPETEER_CHROMIUM_REVISION=latest
export DISABLE_GPU_SANDBOX=1

# Intel UHD 620 compatibility
export LIBVA_DRIVER_NAME=iHD
export MESA_LOADER_DRIVER_OVERRIDE=i965

node src/index.js "$@"
LAUNCH

chmod +x launch.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Quick start:"
echo "   ./launch.sh                    # Interactive mode"
echo "   ./launch.sh --dashboard        # With web dashboard"
echo "   ./launch.sh exec 'search test' # Single command"
echo ""
```

## 2. Package Configuration

JSON

```
{
  "name": "ultra-automation",
  "version": "2.0.0",
  "description": "Full Integrated Browser Automation - macOS Tahoe Hackintosh Build",
  "type": "module",
  "main": "src/index.js",
  "bin": { "auto": "./src/index.js" },
  "scripts": {
    "start": "node src/index.js",
    "dash": "node src/index.js --dashboard",
    "dev": "node src/index.js --dashboard --headless=false",
    "setup": "bash setup.sh",
    "exec": "node src/index.js exec"
  },
  "dependencies": {
    "puppeteer": "^23.11.0",
    "express": "^4.21.0",
    "ws": "^8.18.0",
    "chalk": "^5.3.0",
    "commander": "^12.1.0",
    "inquirer": "^12.0.0",
    "ora": "^8.1.0",
    "dotenv": "^16.4.5",
    "cli-table3": "^0.6.5",
    "boxen": "^8.0.1",
    "open": "^10.1.0"
  },
  "engines": {
    "node": ">=20.0.0"
  },
  "os": ["darwin"],
  "cpu": ["x64"]
}
```

env

```
# .env
# === macOS Tahoe Hackintosh Config ===
# ThinkPad X13 Yoga Gen 1 / i5-10310U

BROWSER_HEADLESS=false
BROWSER_SANDBOX=false
BROWSER_GPU=false
BROWSER_SHM=false

DOWNLOAD_DIR=./output/downloads
SCREENSHOT_DIR=./output/screenshots
DATA_DIR=./output/data
LOG_DIR=./output/logs

DASHBOARD_PORT=3456
DASHBOARD_HOST=0.0.0.0

MAX_CONCURRENT_TASKS=3
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=45000

USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

# Throttle for i5-10310U (4C/8T, 15W TDP)
CPU_THROTTLE=true
MAX_PAGES=5
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
```

## 3. Core Utils

JavaScript

```
// src/utils/config.js
import { config as dotenvConfig } from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';
import os from 'os';

dotenvConfig();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '../../');

const dirs = ['output/downloads', 'output/screenshots', 'output/data', 'output/logs'];
dirs.forEach(d => {
  const p = path.join(ROOT, d);
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
});

function env(key, fallback) {
  return process.env[key] ?? fallback;
}

const config = {
  ROOT,
  platform: os.platform(),
  arch: os.arch(),
  cpus: os.cpus().length,
  hostname: os.hostname(),
  totalMem: Math.round(os.totalmem() / 1024 / 1024 / 1024),

  browser: {
    headless: env('BROWSER_HEADLESS', 'false') === 'true',
    sandbox: env('BROWSER_SANDBOX', 'false') === 'true',
    gpu: env('BROWSER_GPU', 'false') === 'true',
    shm: env('BROWSER_SHM', 'false') === 'true',
    maxPages: parseInt(env('MAX_PAGES', '5')),
    viewportW: parseInt(env('VIEWPORT_WIDTH', '1920')),
    viewportH: parseInt(env('VIEWPORT_HEIGHT', '1080')),
    userAgent: env('USER_AGENT', ''),
    timeout: parseInt(env('DEFAULT_TIMEOUT', '30000')),
    navTimeout: parseInt(env('NAVIGATION_TIMEOUT', '45000')),
  },

  paths: {
    downloads:   path.join(ROOT, env('DOWNLOAD_DIR', './output/downloads')),
    screenshots: path.join(ROOT, env('SCREENSHOT_DIR', './output/screenshots')),
    data:        path.join(ROOT, env('DATA_DIR', './output/data')),
    logs:        path.join(ROOT, env('LOG_DIR', './output/logs')),
  },

  server: {
    port: parseInt(env('DASHBOARD_PORT', '3456')),
    host: env('DASHBOARD_HOST', '0.0.0.0'),
  },

  maxConcurrent: parseInt(env('MAX_CONCURRENT_TASKS', '3')),
  cpuThrottle: env('CPU_THROTTLE', 'true') === 'true',
};

// Hackintosh-specific Chromium args for Intel UHD 620
config.chromiumArgs = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-dev-shm-usage',
  '--disable-gpu-sandbox',
  `--window-size=${config.browser.viewportW},${config.browser.viewportH}`,
  '--disable-blink-features=AutomationControlled',
  '--disable-features=VizDisplayCompositor',
  '--disable-background-timer-throttling',
  '--disable-renderer-backgrounding',
  '--disable-backgrounding-occluded-windows',
  '--force-color-profile=srgb',
  '--hide-scrollbars',
];

if (!config.browser.gpu) {
  config.chromiumArgs.push(
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-gpu-compositing'
  );
}

if (!config.browser.shm) {
  config.chromiumArgs.push('--disable-dev-shm-usage');
}

export default config;
```

JavaScript

```
// src/utils/logger.js
import chalk from 'chalk';
import fs from 'fs';
import path from 'path';
import config from './config.js';

class Logger {
  constructor() {
    this.subscribers = new Set();
    this.history = [];
    this.maxHistory = 2000;
    this.sessionFile = path.join(
      config.paths.logs,
      `session-${new Date().toISOString().replace(/[:.]/g, '-')}.jsonl`
    );
    this.counts = { info: 0, success: 0, warn: 0, error: 0, task: 0, download: 0, step: 0 };
  }

  subscribe(fn) {
    this.subscribers.add(fn);
    return () => this.subscribers.delete(fn);
  }

  _broadcast(entry) {
    this.history.push(entry);
    if (this.history.length > this.maxHistory) this.history.shift();

    try {
      fs.appendFileSync(this.sessionFile, JSON.stringify(entry) + '\n');
    } catch {}

    for (const fn of this.subscribers) {
      try { fn(entry); } catch {}
    }
  }

  _log(type, icon, color, badge, message, data = null) {
    this.counts[type] = (this.counts[type] || 0) + 1;

    const entry = {
      id: this.history.length + 1,
      type,
      badge,
      message,
      data,
      timestamp: new Date().toISOString(),
      time: new Date().toLocaleTimeString('en-US', { hour12: false }),
    };

    console.log(`${color(icon)} ${color(message)}`);
    this._broadcast(entry);
    return entry;
  }

  info(msg, data)     { return this._log('info',    'ℹ', chalk.cyan,    'INFO',   msg, data); }
  success(msg, data)  { return this._log('success', '✔', chalk.green,   'OK',     msg, data); }
  warn(msg, data)     { return this._log('warn',    '⚠', chalk.yellow,  'WARN',   msg, data); }
  error(msg, data)    { return this._log('error',   '✖', chalk.red,     'ERROR',  msg, data); }
  task(msg, data)     { return this._log('task',    '➤', chalk.magenta, 'TASK',   msg, data); }
  download(msg, data) { return this._log('download','⬇', chalk.blue,    'DL',     msg, data); }

  step(num, total, msg, data) {
    return this._log('step', '›', chalk.gray, `${num}/${total}`, msg, data);
  }

  progress(label, percent, current, total) {
    const width = 30;
    const filled = Math.round(width * percent / 100);
    const bar = '█'.repeat(filled) + '░'.repeat(width - filled);
    const line = `  ${bar} ${percent}% · ${current} / ${total}`;
    process.stdout.write(`\r${chalk.cyan(line)}`);
    if (percent >= 100) console.log('');
  }

  divider(char = '─', len = 50) {
    console.log(chalk.gray(char.repeat(len)));
  }

  banner(text) {
    console.log('\n' + chalk.bgCyan.black(` ${text} `) + '\n');
  }

  table(headers, rows) {
    const Table = (await import('cli-table3')).default;
    const t = new Table({
      head: headers.map(h => chalk.cyan(h)),
      style: { 'padding-left': 1 }
    });
    rows.forEach(r => t.push(r));
    console.log(t.toString());
  }
}

export default new Logger();
```

JavaScript

```
// src/utils/files.js
import fs from 'fs';
import path from 'path';
import config from './config.js';
import logger from './logger.js';

class FileManager {
  write(filename, content, type = 'data') {
    const dir = config.paths[type] || config.paths.data;
    const filePath = path.join(dir, filename);

    if (Buffer.isBuffer(content)) {
      fs.writeFileSync(filePath, content);
    } else if (typeof content === 'object') {
      fs.writeFileSync(filePath, JSON.stringify(content, null, 2), 'utf-8');
    } else {
      fs.writeFileSync(filePath, String(content), 'utf-8');
    }

    const stat = fs.statSync(filePath);
    const sizeStr = this.formatSize(stat.size);
    logger.success(`Saved: ${filePath} (${sizeStr})`);
    return { path: filePath, size: stat.size, sizeStr };
  }

  json(name, data) {
    const fn = name.endsWith('.json') ? name : `${name}.json`;
    return this.write(fn, data, 'data');
  }

  csv(name, headers, rows) {
    const fn = name.endsWith('.csv') ? name : `${name}.csv`;
    const lines = [headers.join(','), ...rows.map(r => r.map(c => `"${String(c).replace(/"/g,'""')}"`).join(','))];
    return this.write(fn, lines.join('\n'), 'data');
  }

  html(name, content) {
    const fn = name.endsWith('.html') ? name : `${name}.html`;
    return this.write(fn, content, 'data');
  }

  list(type = 'data') {
    const dir = config.paths[type];
    if (!dir || !fs.existsSync(dir)) return [];
    return fs.readdirSync(dir).map(name => {
      const fp = path.join(dir, name);
      const stat = fs.statSync(fp);
      return {
        name,
        path: fp,
        size: stat.size,
        sizeStr: this.formatSize(stat.size),
        modified: stat.mtime.toISOString(),
        isDir: stat.isDirectory()
      };
    }).filter(f => !f.isDir).sort((a, b) => b.modified.localeCompare(a.modified));
  }

  summary() {
    const types = ['downloads', 'screenshots', 'data', 'logs'];
    const result = {};
    let totalSize = 0;

    types.forEach(type => {
      const files = this.list(type);
      const size = files.reduce((s, f) => s + f.size, 0);
      totalSize += size;
      result[type] = { count: files.length, size, sizeStr: this.formatSize(size), files };
    });

    result.totalSize = totalSize;
    result.totalSizeStr = this.formatSize(totalSize);
    return result;
  }

  formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(i > 0 ? 1 : 0)} ${units[i]}`;
  }

  timestamp() {
    return new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  }
}

export default new FileManager();
```

## 4. Browser Engine (Hackintosh Optimized)

JavaScript

```
// src/core/browser-engine.js
import puppeteer from 'puppeteer';
import config from '../utils/config.js';
import logger from '../utils/logger.js';
import path from 'path';
import fs from 'fs';

class BrowserEngine {
  constructor() {
    this.browser = null;
    this.pages = new Map();
    this.isReady = false;
    this.stats = {
      launched: null,
      pagesOpened: 0,
      pagesActive: 0,
      downloads: 0,
      screenshots: 0,
      navigations: 0,
      errors: 0,
    };
  }

  async launch(opts = {}) {
    if (this.browser && this.isReady) return this.browser;

    logger.task('Launching Chromium browser...');
    logger.info(`Platform: ${config.platform} ${config.arch} · CPUs: ${config.cpus} · RAM: ${config.totalMem}GB`);
    logger.info(`Hackintosh: ThinkPad X13 Yoga Gen1 · i5-10310U · Intel UHD 620`);

    const launchOpts = {
      headless: opts.headless ?? config.browser.headless,
      defaultViewport: {
        width: config.browser.viewportW,
        height: config.browser.viewportH,
      },
      args: config.chromiumArgs,
      ignoreDefaultArgs: ['--enable-automation'],
      timeout: 60000,
    };

    try {
      this.browser = await puppeteer.launch(launchOpts);
      this.isReady = true;
      this.stats.launched = Date.now();

      this.browser.on('disconnected', () => {
        this.isReady = false;
        this.pages.clear();
        logger.warn('Browser disconnected');
      });

      const version = await this.browser.version();
      logger.success(`Browser ready: ${version}`);
      return this.browser;

    } catch (err) {
      logger.error(`Browser launch failed: ${err.message}`);
      logger.info('Retrying with headless mode...');

      launchOpts.headless = 'shell';
      this.browser = await puppeteer.launch(launchOpts);
      this.isReady = true;
      this.stats.launched = Date.now();
      logger.success('Browser ready (headless fallback)');
      return this.browser;
    }
  }

  async newPage(id = null) {
    if (!this.browser) await this.launch();

    const pageId = id || `page-${++this.stats.pagesOpened}`;
    const page = await this.browser.newPage();

    // Anti-detection
    await page.setUserAgent(config.browser.userAgent);
    await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });

    await page.evaluateOnNewDocument(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => false });
      Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
      });
      window.chrome = { runtime: {} };
    });

    // Download path via CDP
    try {
      const cdp = await page.createCDPSession();
      await cdp.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: config.paths.downloads,
      });
    } catch {}

    // Timeout
    page.setDefaultNavigationTimeout(config.browser.navTimeout);
    page.setDefaultTimeout(config.browser.timeout);

    this.pages.set(pageId, page);
    this.stats.pagesActive = this.pages.size;

    page.on('close', () => {
      this.pages.delete(pageId);
      this.stats.pagesActive = this.pages.size;
    });

    return { page, id: pageId };
  }

  async page(id = 'main') {
    if (this.pages.has(id)) return this.pages.get(id);
    const { page } = await this.newPage(id);
    return page;
  }

  async goto(url, id = 'main') {
    const page = await this.page(id);
    logger.info(`Navigating: ${url}`);

    const response = await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: config.browser.navTimeout,
    });

    this.stats.navigations++;
    const title = await page.title().catch(() => '');
    const status = response?.status() || 0;

    logger.success(`Loaded: ${title} [${status}]`);
    return { page, title, status, url };
  }

  async screenshot(id = 'main', name = null) {
    const page = await this.page(id);
    const title = await page.title().catch(() => 'page');
    const safeName = (name || title)
      .replace(/[^a-z0-9_-]/gi, '-')
      .substring(0, 60)
      .toLowerCase();
    const filename = `${safeName}-${Date.now()}.png`;
    const filePath = path.join(config.paths.screenshots, filename);

    await page.screenshot({ path: filePath, fullPage: true, type: 'png' });
    this.stats.screenshots++;

    const stat = fs.statSync(filePath);
    logger.success(`Screenshot: ${filename} (${Math.round(stat.size / 1024)} KB)`);
    return { path: filePath, filename, size: stat.size };
  }

  async pdf(id = 'main', name = null) {
    const page = await this.page(id);
    const title = await page.title().catch(() => 'page');
    const safeName = (name || title)
      .replace(/[^a-z0-9_-]/gi, '-')
      .substring(0, 60)
      .toLowerCase();
    const filename = `${safeName}-${Date.now()}.pdf`;
    const filePath = path.join(config.paths.downloads, filename);

    await page.pdf({
      path: filePath,
      format: 'A4',
      printBackground: true,
      margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
    });

    const stat = fs.statSync(filePath);
    logger.success(`PDF: ${filename} (${Math.round(stat.size / 1024)} KB)`);
    return { path: filePath, filename, size: stat.size };
  }

  async evaluate(fn, id = 'main') {
    const page = await this.page(id);
    return page.evaluate(fn);
  }

  async click(selector, id = 'main') {
    const page = await this.page(id);
    await page.waitForSelector(selector, { timeout: config.browser.timeout });
    await page.click(selector);
    logger.info(`Clicked: ${selector}`);
  }

  async type(selector, text, id = 'main') {
    const page = await this.page(id);
    await page.waitForSelector(selector, { timeout: config.browser.timeout });
    await page.type(selector, text, { delay: 40 });
    logger.info(`Typed ${text.length} chars into: ${selector}`);
  }

  async scroll(direction = 'down', amount = 500, id = 'main') {
    const page = await this.page(id);
    const map = {
      down:   () => page.evaluate(px => window.scrollBy(0, px), amount),
      up:     () => page.evaluate(px => window.scrollBy(0, -px), amount),
      top:    () => page.evaluate(() => window.scrollTo(0, 0)),
      bottom: () => page.evaluate(() => window.scrollTo(0, document.body.scrollHeight)),
    };
    await (map[direction] || map.down)();
    logger.info(`Scrolled: ${direction} ${amount}px`);
  }

  async close() {
    if (this.browser) {
      await this.browser.close().catch(() => {});
      this.browser = null;
      this.isReady = false;
      this.pages.clear();
      logger.info('Browser closed');
    }
  }

  getStats() {
    return {
      ...this.stats,
      isReady: this.isReady,
      uptime: this.stats.launched ? Date.now() - this.stats.launched : 0,
      uptimeStr: this.stats.launched
        ? this._formatUptime(Date.now() - this.stats.launched)
        : '0s',
    };
  }

  _formatUptime(ms) {
    const s = Math.floor(ms / 1000);
    if (s < 60) return `${s}s`;
    const m = Math.floor(s / 60);
    if (m < 60) return `${m}m ${s % 60}s`;
    const h = Math.floor(m / 60);
    return `${h}h ${m % 60}m`;
  }
}

export default new BrowserEngine();
```

## 5. Modules

JavaScript

```
// src/modules/search.js
import browser from '../core/browser-engine.js';
import logger from '../utils/logger.js';
import files from '../utils/files.js';

export default {
  async search(query) {
    logger.task(`Searching: "${query}"`);
    const url = `https://www.google.com/search?q=${encodeURIComponent(query)}&hl=en`;
    const { page, title } = await browser.goto(url);

    await page.waitForSelector('body', { timeout: 10000 });
    await new Promise(r => setTimeout(r, 1500));

    const results = await page.evaluate(() => {
      const items = [];
      document.querySelectorAll('.g, .MjjYud').forEach((el, i) => {
        const titleEl = el.querySelector('h3');
        const linkEl = el.querySelector('a[href^="http"]');
        const snippetEl = el.querySelector('.VwiC3b, [data-sncf], .lEBKkf');
        if (titleEl && linkEl) {
          items.push({
            rank: items.length + 1,
            title: titleEl.textContent?.trim() || '',
            link: linkEl.href || '',
            snippet: snippetEl?.textContent?.trim()?.substring(0, 200) || '',
          });
        }
      });
      return items.slice(0, 15);
    });

    logger.divider();
    logger.banner(`SEARCH: "${query}" — ${results.length} results`);
    results.forEach((r, i) => {
      console.log(`  ${i + 1}. ${r.title}`);
      console.log(`     ${r.link}`);
      if (r.snippet) console.log(`     ${r.snippet.substring(0, 100)}...`);
      console.log('');
    });

    const saved = files.json(`search-${files.timestamp()}`, {
      query,
      timestamp: new Date().toISOString(),
      count: results.length,
      results,
    });

    return { query, count: results.length, results, saved };
  },

  async multiSearch(queries) {
    logger.banner(`MULTI-SEARCH: ${queries.length} queries`);
    const all = {};

    for (let i = 0; i < queries.length; i++) {
      logger.step(i + 1, queries.length, queries[i]);
      const result = await this.search(queries[i]);
      all[queries[i]] = result;
      if (i < queries.length - 1) await new Promise(r => setTimeout(r, 2500));
    }

    files.json(`multi-search-${files.timestamp()}`, all);
    logger.success(`Multi-search done: ${queries.length} queries`);
    return all;
  },
};
```

JavaScript

```
// src/modules/scraper.js
import browser from '../core/browser-engine.js';
import logger from '../utils/logger.js';
import files from '../utils/files.js';

export default {
  async scrape(url, selector = null) {
    logger.task(`Scraping: ${url}`);
    const { page, title } = await browser.goto(url);

    let data;

    if (selector) {
      data = await page.evaluate((sel) => {
        return Array.from(document.querySelectorAll(sel)).map(el => ({
          tag: el.tagName.toLowerCase(),
          text: el.textContent?.trim()?.substring(0, 500),
          html: el.innerHTML?.substring(0, 1000),
          attrs: Object.fromEntries(Array.from(el.attributes).map(a => [a.name, a.value])),
        }));
      }, selector);
      logger.success(`Scraped ${data.length} elements: "${selector}"`);
    } else {
      data = await page.evaluate(() => ({
        title: document.title,
        url: location.href,
        meta: {
          description: document.querySelector('meta[name="description"]')?.content || '',
          keywords: document.querySelector('meta[name="keywords"]')?.content || '',
          ogTitle: document.querySelector('meta[property="og:title"]')?.content || '',
          ogImage: document.querySelector('meta[property="og:image"]')?.content || '',
          ogDescription: document.querySelector('meta[property="og:description"]')?.content || '',
        },
        headings: {
          h1: [...document.querySelectorAll('h1')].map(e => e.textContent?.trim()),
          h2: [...document.querySelectorAll('h2')].map(e => e.textContent?.trim()),
          h3: [...document.querySelectorAll('h3')].map(e => e.textContent?.trim()).slice(0, 20),
        },
        stats: {
          links: document.querySelectorAll('a[href]').length,
          images: document.querySelectorAll('img').length,
          forms: document.querySelectorAll('form').length,
          inputs: document.querySelectorAll('input').length,
          buttons: document.querySelectorAll('button').length,
          scripts: document.querySelectorAll('script').length,
          stylesheets: document.querySelectorAll('link[rel="stylesheet"]').length,
        },
        textLength: document.body?.innerText?.length || 0,
        wordCount: (document.body?.innerText || '').split(/\s+/).filter(Boolean).length,
      }));

      logger.success(`Full scrape: ${title}`);
      logger.info(`  Links: ${data.stats.links} · Images: ${data.stats.images} · Words: ${data.wordCount}`);
    }

    const safeName = (title || 'scrape').replace(/[^a-z0-9]/gi, '-').substring(0, 50);
    const ts = files.timestamp();

    files.json(`scrape-${safeName}-${ts}`, { url, title, scrapedAt: new Date().toISOString(), data });

    const html = await page.content();
    files.html(`scrape-${safeName}-${ts}`, html);

    return { url, title, data };
  },
};
```

JavaScript

```
// src/modules/extractor.js
import browser from '../core/browser-engine.js';
import logger from '../utils/logger.js';
import files from '../utils/files.js';

export default {
  async extract(type, url = null) {
    if (url) await browser.goto(url);
    const page = await browser.page();

    logger.task(`Extracting: ${type}`);

    const extractors = {
      links: () => page.evaluate(() =>
        [...document.querySelectorAll('a[href]')].map(a => ({
          text: a.textContent?.trim()?.substring(0, 150) || '',
          href: a.href,
          external: !a.href.startsWith(location.origin),
        }))
      ),

      images: () => page.evaluate(() =>
        [...document.querySelectorAll('img')].filter(i => i.src).map(i => ({
          src: i.src,
          alt: i.alt || '',
          width: i.naturalWidth || i.width,
          height: i.naturalHeight || i.height,
          loading: i.loading || 'eager',
        }))
      ),

      text: () => page.evaluate(() => ({
        title: document.title,
        body: document.body?.innerText || '',
        wordCount: (document.body?.innerText || '').split(/\s+/).filter(Boolean).length,
        lang: document.documentElement.lang || 'unknown',
      })),

      emails: async () => {
        const html = await page.evaluate(() => document.body.innerHTML);
        const re = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
        return [...new Set(html.match(re) || [])];
      },

      tables: () => page.evaluate(() =>
        [...document.querySelectorAll('table')].map((t, ti) => ({
          index: ti,
          caption: t.querySelector('caption')?.textContent?.trim() || '',
          headers: [...(t.querySelector('thead tr')?.querySelectorAll('th') || [])].map(h => h.textContent?.trim()),
          rows: [...t.querySelectorAll('tbody tr, tr')].slice(0, 100).map(tr =>
            [...tr.querySelectorAll('td, th')].map(c => c.textContent?.trim())
          ),
          rowCount: t.querySelectorAll('tr').length,
        }))
      ),

      scripts: () => page.evaluate(() =>
        [...document.querySelectorAll('script[src]')].map(s => ({
          src: s.src,
          async: s.async,
          defer: s.defer,
          type: s.type || 'text/javascript',
        }))
      ),

      meta: () => page.evaluate(() => {
        const metas = {};
        document.querySelectorAll('meta').forEach(m => {
          const key = m.getAttribute('name') || m.getAttribute('property') || m.getAttribute('http-equiv');
          if (key) metas[key] = m.getAttribute('content') || '';
        });
        return metas;
      }),

      styles: () => page.evaluate(() =>
        [...document.querySelectorAll('link[rel="stylesheet"]')].map(l => ({
          href: l.href,
          media: l.media || 'all',
        }))
      ),
    };

    if (!extractors[type]) {
      logger.error(`Unknown type: ${type}. Available: ${Object.keys(extractors).join(', ')}`);
      return null;
    }

    const data = await extractors[type]();
    const count = Array.isArray(data) ? data.length : Object.keys(data).length;
    logger.success(`Extracted ${type}: ${count} items`);

    const saved = files.json(`extract-${type}-${files.timestamp()}`, {
      type,
      count,
      extractedAt: new Date().toISOString(),
      data,
    });

    return { type, count, data, saved };
  },
};
```

JavaScript

```
// src/modules/downloader.js
import browser from '../core/browser-engine.js';
import logger from '../utils/logger.js';
import files from '../utils/files.js';
import config from '../utils/config.js';
import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';

export default {
  async download(url, filename = null) {
    const name = filename || url.split('/').pop()?.split('?')[0] || `file-${Date.now()}`;
    const filePath = path.join(config.paths.downloads, name);

    logger.download(`Downloading: ${url}`);
    logger.info(`Target: ${filePath}`);

    return new Promise((resolve, reject) => {
      const proto = url.startsWith('https') ? https : http;

      const fetch = (targetUrl, redirects = 0) => {
        if (redirects > 5) return reject(new Error('Too many redirects'));

        proto.get(targetUrl, {
          headers: {
            'User-Agent': config.browser.userAgent,
            'Accept': '*/*',
          },
          timeout: config.browser.timeout,
        }, (res) => {
          if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
            return fetch(res.headers.location, redirects + 1);
          }

          if (res.statusCode !== 200) {
            return reject(new Error(`HTTP ${res.statusCode}`));
          }

          const total = parseInt(res.headers['content-length'], 10) || 0;
          let downloaded = 0;
          const file = fs.createWriteStream(filePath);

          res.on('data', chunk => {
            downloaded += chunk.length;
            if (total > 0) {
              const pct = Math.round((downloaded / total) * 100);
              logger.progress(name, pct,
                files.formatSize(downloaded),
                files.formatSize(total)
              );
            }
          });

          res.pipe(file);

          file.on('finish', () => {
            file.close();
            const sizeStr = files.formatSize(downloaded);
            logger.success(`Downloaded: ${name} (${sizeStr})`);
            resolve({ path: filePath, filename: name, size: downloaded, sizeStr });
          });

          file.on('error', err => {
            fs.unlink(filePath, () => {});
            reject(err);
          });
        }).on('error', reject);
      };

      fetch(url);
    });
  },

  async batchDownload(url) {
    logger.task(`Batch download from: ${url}`);
    const { page } = await browser.goto(url);

    const links = await page.evaluate(() => {
      const exts = ['.pdf','.zip','.rar','.7z','.tar','.gz','.doc','.docx','.xls','.xlsx',
        '.ppt','.pptx','.csv','.mp3','.mp4','.avi','.mkv','.jpg','.jpeg','.png',
        '.gif','.svg','.webp','.woff','.woff2','.ttf','.eot'];

      return [...document.querySelectorAll('a[href]')]
        .filter(a => exts.some(ext => a.href.toLowerCase().includes(ext)))
        .map(a => ({
          url: a.href,
          text: a.textContent?.trim()?.substring(0, 100),
          filename: decodeURIComponent(a.href.split('/').pop()?.split('?')[0] || ''),
        }));
    });

    logger.info(`Found ${links.length} downloadable files`);

    const results = [];
    for (let i = 0; i < links.length; i++) {
      logger.step(i + 1, links.length, links[i].filename);
      try {
        const r = await this.download(links[i].url, links[i].filename);
        results.push({ ...r, status: 'ok' });
      } catch (err) {
        logger.error(`Failed: ${links[i].filename} — ${err.message}`);
        results.push({ filename: links[i].filename, status: 'error', error: err.message });
      }
      if (i < links.length - 1) await new Promise(r => setTimeout(r, 500));
    }

    const ok = results.filter(r => r.status === 'ok').length;
    logger.success(`Batch complete: ${ok}/${links.length} files`);

    files.json(`batch-download-${files.timestamp()}`, {
      source: url,
      total: links.length,
      downloaded: ok,
      failed: links.length - ok,
      files: results,
    });

    return { source: url, total: links.length, downloaded: ok, results };
  },
};
```

JavaScript

```
// src/modules/screenshot.js
import browser from '../core/browser-engine.js';

export default {
  async capture(name = null, opts = {}) {
    return browser.screenshot('main', name);
  },

  async captureElement(selector, name = null) {
    const page = await browser.page();
    const el = await page.$(selector);
    if (!el) throw new Error(`Element not found: ${selector}`);

    const filename = (name || `element-${Date.now()}`) + '.png';
    const path = (await import('../utils/config.js')).default.paths.screenshots + '/' + filename;
    await el.screenshot({ path });
    return { path, filename };
  },

  async captureMultiple(urls, namePrefix = 'multi') {
    const results = [];
    for (let i = 0; i < urls.length; i++) {
      await browser.goto(urls[i]);
      await new Promise(r => setTimeout(r, 1500));
      const r = await browser.screenshot('main', `${namePrefix}-${i + 1}`);
      results.push(r);
    }
    return results;
  },
};
```

JavaScript

```
// src/modules/monitor.js
import browser from '../core/browser-engine.js';
import logger from '../utils/logger.js';
import files from '../utils/files.js';

export default {
  async monitor(url, intervalSec = 30, maxChecks = 120) {
    logger.task(`Monitoring: ${url} every ${intervalSec}s (max ${maxChecks} checks)`);
    let prevHash = '';
    let prevLength = 0;
    let checks = 0;
    const changes = [];

    const check = async () => {
      checks++;
      const { page } = await browser.goto(url);
      const content = await page.evaluate(() => document.body?.innerText || '');

      // Simple content hash
      let hash = 0;
      for (let i = 0; i < content.length; i++) {
        hash = ((hash << 5) - hash + content.charCodeAt(i)) | 0;
      }
      const hashStr = hash.toString(36);

      if (prevHash && hashStr !== prevHash) {
        logger.warn(`⚡ Change detected! Check #${checks} · Old: ${prevLength} chars → New: ${content.length} chars`);
        const shot = await browser.screenshot('main', `monitor-change-${checks}`);
        const diff = {
          check: checks,
          timestamp: new Date().toISOString(),
          prevLength,
          newLength: content.length,
          delta: content.length - prevLength,
          screenshot: shot.filename,
        };
        changes.push(diff);
        files.json(`monitor-change-${files.timestamp()}`, {
          url,
          ...diff,
          preview: content.substring(0, 2000),
        });
      } else {
        logger.info(`Check #${checks}: No changes (${content.length} chars)`);
      }

      prevHash = hashStr;
      prevLength = content.length;
    };

    await check();

    const timer = setInterval(async () => {
      if (checks >= maxChecks) {
        clearInterval(timer);
        logger.success(`Monitor stopped after ${maxChecks} checks`);
        return;
      }
      await check().catch(e => logger.error(`Monitor error: ${e.message}`));
    }, intervalSec * 1000);

    return { url, interval: intervalSec, maxChecks, changes, stop: () => clearInterval(timer) };
  },
};
```

## 6. Command Parser & Task Runner

JavaScript

```
// src/core/command-parser.js
const patterns = [
  { re: /^search\s+(.+)$/i,                                  action: 'search',        parse: m => ({ query: m[1] }) },
  { re: /^google\s+(.+)$/i,                                  action: 'search',        parse: m => ({ query: m[1] }) },
  { re: /^(?:open|go|visit|navigate)\s+(?:to\s+)?(.+)$/i,    action: 'navigate',      parse: m => ({ url: m[1].startsWith('http') ? m[1] : `https://${m[1]}` }) },
  { re: /^(?:screenshot|capture|snap)\s*(.*)$/i,              action: 'screenshot',    parse: m => ({ name: m[1] || null }) },
  { re: /^download\s+(.+?)(?:\s+as\s+(.+))?$/i,              action: 'download',      parse: m => ({ url: m[1], filename: m[2] || null }) },
  { re: /^scrape\s+(.+?)(?:\s+selector\s+(.+))?$/i,          action: 'scrape',        parse: m => ({ url: m[1], selector: m[2] || null }) },
  { re: /^extract\s+(links|images|text|emails|tables|scripts|meta|styles)\s*(?:from\s+(.+))?$/i,
                                                               action: 'extract',       parse: m => ({ type: m[1].toLowerCase(), url: m[2] || null }) },
  { re: /^click\s+(.+)$/i,                                   action: 'click',         parse: m => ({ selector: m[1] }) },
  { re: /^type\s+"([^"]+)"\s+(?:in|into)\s+(.+)$/i,          action: 'type',          parse: m => ({ text: m[1], selector: m[2] }) },
  { re: /^scroll\s+(up|down|top|bottom)(?:\s+(\d+))?$/i,     action: 'scroll',        parse: m => ({ direction: m[1], amount: parseInt(m[2]) || 500 }) },
  { re: /^(?:pdf|save-pdf)\s*(.*)$/i,                         action: 'pdf',           parse: m => ({ name: m[1] || null }) },
  { re: /^batch-download\s+(.+)$/i,                           action: 'batch-download',parse: m => ({ url: m[1] }) },
  { re: /^multi-search\s+(.+)$/i,                             action: 'multi-search',  parse: m => ({ queries: m[1].split(',').map(q => q.trim()) }) },
  { re: /^monitor\s+(.+?)(?:\s+every\s+(\d+)s?)?$/i,         action: 'monitor',       parse: m => ({ url: m[1], interval: parseInt(m[2]) || 30 }) },
  { re: /^pipe(?:line)?\s+(.+)$/i,                            action: 'pipeline',      parse: m => ({ steps: m[1].split('|').map(s => s.trim()) }) },
  { re: /^wait\s+(\d+)$/i,                                   action: 'wait',          parse: m => ({ ms: parseInt(m[1]) }) },
];

const helpList = [
  { cmd: 'search <query>',                        desc: 'Google search & save results' },
  { cmd: 'open <url>',                            desc: 'Navigate to URL' },
  { cmd: 'screenshot [name]',                     desc: 'Full-page screenshot' },
  { cmd: 'download <url> [as name]',              desc: 'Download file with progress' },
  { cmd: 'scrape <url> [selector ...]',           desc: 'Scrape page data' },
  { cmd: 'extract links|images|text|emails|tables', desc: 'Extract specific data' },
  { cmd: 'click <selector>',                      desc: 'Click element' },
  { cmd: 'type "text" in <selector>',             desc: 'Type into field' },
  { cmd: 'scroll up|down|top|bottom [px]',        desc: 'Scroll page' },
  { cmd: 'pdf [name]',                            desc: 'Save as PDF' },
  { cmd: 'batch-download <url>',                  desc: 'Download all files from page' },
  { cmd: 'multi-search q1, q2, q3',               desc: 'Search multiple queries' },
  { cmd: 'monitor <url> [every Ns]',              desc: 'Watch for page changes' },
  { cmd: 'pipe cmd1 | cmd2 | cmd3',               desc: 'Chain commands' },
  { cmd: 'wait <ms>',                             desc: 'Wait N milliseconds' },
  { cmd: 'status',                                desc: 'System status' },
  { cmd: 'help',                                  desc: 'Show commands' },
  { cmd: 'exit',                                  desc: 'Quit' },
];

export function parse(input) {
  const text = input.trim();

  for (const p of patterns) {
    const m = text.match(p.re);
    if (m) return { action: p.action, ...p.parse(m), raw: text };
  }

  if (/^https?:\/\//.test(text)) return { action: 'navigate', url: text, raw: text };
  return { action: 'search', query: text, raw: text };
}

export function getHelp() {
  return helpList;
}
```

JavaScript

```
// src/core/task-runner.js
import { parse } from './command-parser.js';
import browser from './browser-engine.js';
import logger from '../utils/logger.js';
import files from '../utils/files.js';
import search from '../modules/search.js';
import scraper from '../modules/scraper.js';
import extractor from '../modules/extractor.js';
import downloader from '../modules/downloader.js';
import screenshot from '../modules/screenshot.js';
import monitor from '../modules/monitor.js';

class TaskRunner {
  constructor() {
    this.tasks = [];
    this.subscribers = new Set();
    this.idCounter = 0;
  }

  subscribe(fn) {
    this.subscribers.add(fn);
    return () => this.subscribers.delete(fn);
  }

  _emit(event, task) {
    for (const fn of this.subscribers) {
      try { fn(event, task); } catch {}
    }
  }

  async run(input) {
    const cmd = typeof input === 'string' ? parse(input) : input;
    const task = {
      id: ++this.idCounter,
      action: cmd.action,
      detail: cmd.query || cmd.url || cmd.name || cmd.type || '',
      raw: cmd.raw || '',
      status: 'running',
      startTime: Date.now(),
      endTime: null,
      duration: null,
      result: null,
      error: null,
    };

    this.tasks.push(task);
    this._emit('start', task);

    try {
      task.result = await this._dispatch(cmd);
      task.status = 'done';
    } catch (err) {
      task.status = 'fail';
      task.error = err.message;
      logger.error(`Task ${task.id} failed: ${err.message}`);
    }

    task.endTime = Date.now();
    task.duration = task.endTime - task.startTime;
    this._emit(task.status === 'done' ? 'complete' : 'error', task);
    return task;
  }

  async _dispatch(cmd) {
    switch (cmd.action) {
      case 'search':
        return search.search(cmd.query);

      case 'multi-search':
        return search.multiSearch(cmd.queries);

      case 'navigate': {
        const r = await browser.goto(cmd.url);
        return { url: cmd.url, title: r.title, status: r.status };
      }

      case 'screenshot':
        return screenshot.capture(cmd.name);

      case 'download':
        return downloader.download(cmd.url, cmd.filename);

      case 'batch-download':
        return downloader.batchDownload(cmd.url);

      case 'scrape':
        return scraper.scrape(cmd.url, cmd.selector);

      case 'extract':
        return extractor.extract(cmd.type, cmd.url);

      case 'click':
        await browser.click(cmd.selector);
        return { clicked: cmd.selector };

      case 'type':
        await browser.type(cmd.selector, cmd.text);
        return { typed: cmd.text.length, selector: cmd.selector };

      case 'scroll':
        await browser.scroll(cmd.direction, cmd.amount);
        return { scrolled: cmd.direction, amount: cmd.amount };

      case 'pdf':
        return browser.pdf('main', cmd.name);

      case 'wait':
        logger.info(`Waiting ${cmd.ms}ms...`);
        await new Promise(r => setTimeout(r, cmd.ms));
        return { waited: cmd.ms };

      case 'monitor':
        return monitor.monitor(cmd.url, cmd.interval);

      case 'pipeline':
        return this._pipeline(cmd.steps);

      default:
        return search.search(cmd.action);
    }
  }

  async _pipeline(steps) {
    logger.banner(`PIPELINE: ${steps.length} steps`);
    const results = [];

    for (let i = 0; i < steps.length; i++) {
      logger.step(i + 1, steps.length, steps[i]);
      const task = await this.run(steps[i]);
      results.push({ step: i + 1, command: steps[i], status: task.status, duration: task.duration });
      if (task.status === 'fail') {
        logger.error(`Pipeline halted at step ${i + 1}`);
        break;
      }
      if (i < steps.length - 1) await new Promise(r => setTimeout(r, 300));
    }

    const ok = results.filter(r => r.status === 'done').length;
    logger.success(`Pipeline done: ${ok}/${steps.length}`);
    return { pipeline: true, total: steps.length, completed: ok, results };
  }

  getStatus() {
    return {
      total: this.tasks.length,
      done: this.tasks.filter(t => t.status === 'done').length,
      failed: this.tasks.filter(t => t.status === 'fail').length,
      running: this.tasks.filter(t => t.status === 'running').length,
      browser: browser.getStats(),
      output: files.summary(),
      recentTasks: this.tasks.slice(-20).reverse(),
    };
  }
}

export default new TaskRunner();
```

## 7. Server (Express + WebSocket)

JavaScript

```
// src/server/websocket.js
import { WebSocketServer } from 'ws';
import logger from '../utils/logger.js';
import taskRunner from '../core/task-runner.js';

export function attachWebSocket(server) {
  const wss = new WebSocketServer({ server });
  const clients = new Set();

  function broadcast(type, data) {
    const msg = JSON.stringify({ type, data, ts: Date.now() });
    for (const ws of clients) {
      if (ws.readyState === 1) ws.send(msg);
    }
  }

  // Forward logs
  logger.subscribe(entry => broadcast('log', entry));

  // Forward task events
  taskRunner.subscribe((event, task) => {
    broadcast('task', { event, ...task });
  });

  // Status pulse
  const pulse = setInterval(() => {
    broadcast('status', taskRunner.getStatus());
  }, 2000);

  wss.on('connection', ws => {
    clients.add(ws);
    logger.info(`Dashboard client connected (${clients.size} total)`);

    // Send initial state
    ws.send(JSON.stringify({
      type: 'init',
      data: taskRunner.getStatus(),
      ts: Date.now(),
    }));

    ws.on('message', async raw => {
      try {
        const msg = JSON.parse(raw);
        if (msg.type === 'command' && msg.data) {
          const result = await taskRunner.run(msg.data);
          ws.send(JSON.stringify({ type: 'result', data: result, ts: Date.now() }));
        }
      } catch (err) {
        ws.send(JSON.stringify({ type: 'error', data: err.message, ts: Date.now() }));
      }
    });

    ws.on('close', () => {
      clients.delete(ws);
      logger.info(`Dashboard client disconnected (${clients.size} remaining)`);
    });
  });

  wss.on('close', () => clearInterval(pulse));
  return wss;
}
```

JavaScript

```
// src/server/routes.js
import { Router } from 'express';
import taskRunner from '../core/task-runner.js';
import files from '../utils/files.js';
import config from '../utils/config.js';
import logger from '../utils/logger.js';

const router = Router();

router.get('/api/status', (req, res) => {
  res.json(taskRunner.getStatus());
});

router.post('/api/execute', async (req, res) => {
  const { command } = req.body;
  if (!command) return res.status(400).json({ error: 'No command' });

  try {
    const task = await taskRunner.run(command);
    res.json({ ok: true, task });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

router.get('/api/files/:type', (req, res) => {
  const type = req.params.type;
  const map = { downloads: 'downloads', screenshots: 'screenshots', data: 'data', logs: 'logs' };
  if (!map[type]) return res.status(400).json({ error: 'Invalid type' });
  res.json(files.list(type));
});

router.get('/api/logs', (req, res) => {
  const limit = parseInt(req.query.limit) || 200;
  res.json(logger.history.slice(-limit));
});

router.get('/api/config', (req, res) => {
  res.json({
    platform: config.platform,
    arch: config.arch,
    cpus: config.cpus,
    hostname: config.hostname,
    totalMem: config.totalMem,
    browser: config.browser,
    server: config.server,
  });
});

export default router;
```

JavaScript

```
// src/server/app.js
import express from 'express';
import { createServer } from 'http';
import { fileURLToPath } from 'url';
import path from 'path';
import config from '../utils/config.js';
import logger from '../utils/logger.js';
import routes from './routes.js';
import { attachWebSocket } from './websocket.js';

export function startServer(taskRunner) {
  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const app = express();
  const server = createServer(app);

  app.use(express.json());
  app.use(routes);

  // Serve dashboard
  app.use(express.static(path.join(__dirname, '../dashboard')));

  // Fallback
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../dashboard/index.html'));
  });

  // WebSocket
  attachWebSocket(server);

  server.listen(config.server.port, config.server.host, () => {
    logger.success(`Dashboard: http://localhost:${config.server.port}`);
  });

  return server;
}
```

## 8. Main Entry (CLI)

JavaScript

```
#!/usr/bin/env node
// src/index.js

import { Command } from 'commander';
import inquirer from 'inquirer';
import chalk from 'chalk';
import ora from 'ora';
import boxen from 'boxen';
import Table from 'cli-table3';
import open from 'open';

import config from './utils/config.js';
import logger from './utils/logger.js';
import browser from './core/browser-engine.js';
import taskRunner from './core/task-runner.js';
import { getHelp } from './core/command-parser.js';
import { startServer } from './server/app.js';
import files from './utils/files.js';

const VERSION = '2.0.0';

function banner() {
  console.log(chalk.cyan(`
  ╔══════════════════════════════════════════════════════════╗
  ║            🚀  ULTRA AUTOMATION  v${VERSION}               ║
  ║        Full Browser Automation + Live Dashboard          ║
  ╠══════════════════════════════════════════════════════════╣
  ║  Machine : ThinkPad X13 Yoga Gen1 · i5-10310U           ║
  ║  OS      : macOS Tahoe 26.5 (Hackintosh)                ║
  ║  Engine  : Puppeteer + Chromium (GPU sandbox disabled)   ║
  ╚══════════════════════════════════════════════════════════╝
  `));
}

function showHelp() {
  const cmds = getHelp();
  const table = new Table({
    head: [chalk.cyan('Command'), chalk.cyan('Description')],
    colWidths: [48, 32],
    style: { 'padding-left': 1 }
  });
  cmds.forEach(c => table.push([chalk.white(c.cmd), chalk.gray(c.desc)]));
  console.log('\n' + table.toString());
  console.log(chalk.gray('\n  Tip: commands are case-insensitive. Unknown text is auto-searched.\n'));
}

function showStatus() {
  const s = taskRunner.getStatus();
  const b = s.browser;
  const o = s.output;

  console.log(boxen([
    `${chalk.cyan('Browser')}      ${b.isReady ? chalk.green('● Running') : chalk.red('● Stopped')}`,
    `${chalk.cyan('Uptime')}       ${b.uptimeStr}`,
    `${chalk.cyan('Pages')}        ${b.navigations} visited · ${b.pagesActive} active`,
    `${chalk.cyan('Screenshots')}  ${b.screenshots}`,
    `${chalk.cyan('Downloads')}    ${b.downloads}`,
    '',
    `${chalk.cyan('Tasks')}        ${s.done} done · ${s.failed} failed · ${s.running} running`,
    '',
    `${chalk.cyan('Output')}`,
    `  Downloads    ${o.downloads.count} files  ${o.downloads.sizeStr}`,
    `  Screenshots  ${o.screenshots.count} files  ${o.screenshots.sizeStr}`,
    `  Data         ${o.data.count} files  ${o.data.sizeStr}`,
    `  Total        ${o.totalSizeStr}`,
  ].join('\n'), {
    padding: 1, margin: { top: 1, bottom: 1 },
    borderStyle: 'round', borderColor: 'cyan',
    title: '📊 System Status', titleAlignment: 'center',
  }));
}

// CLI program
const program = new Command();
program.name('auto').version(VERSION);

// Default: interactive
program
  .command('interactive', { isDefault: true })
  .alias('i')
  .option('-d, --dashboard', 'Launch web dashboard')
  .option('--headless', 'Headless browser')
  .action(async (opts) => {
    banner();

    if (opts.headless) config.browser.headless = true;

    // Launch browser
    const spin = ora({ text: 'Initializing browser engine...', color: 'cyan' }).start();
    try {
      await browser.launch({ headless: config.browser.headless });
      spin.succeed('Browser engine ready');
    } catch (err) {
      spin.fail(`Browser error: ${err.message}`);
      process.exit(1);
    }

    // Dashboard
    if (opts.dashboard) {
      startServer(taskRunner);
      console.log(chalk.gray(`  📊 Dashboard → http://localhost:${config.server.port}\n`));
    }

    console.log(chalk.gray('  Type "help" for commands · "exit" to quit\n'));

    // REPL
    const loop = async () => {
      while (true) {
        try {
          const { cmd } = await inquirer.prompt([{
            type: 'input',
            name: 'cmd',
            message: chalk.cyan('auto ❯'),
            prefix: '',
          }]);

          const text = cmd.trim();
          if (!text) continue;

          if (text === 'exit' || text === 'quit') {
            const s = ora('Shutting down...').start();
            await browser.close();
            s.succeed('Goodbye! 👋');
            process.exit(0);
          }

          if (text === 'help')      { showHelp(); continue; }
          if (text === 'status')    { showStatus(); continue; }
          if (text === 'clear')     { console.clear(); banner(); continue; }
          if (text === 'dashboard') {
            startServer(taskRunner);
            await open(`http://localhost:${config.server.port}`);
            continue;
          }

          // Execute
          const s = ora({ text: `Executing: ${text}`, color: 'cyan' }).start();
          const task = await taskRunner.run(text);

          if (task.status === 'done') {
            s.succeed(`Done (${task.duration}ms)`);
            if (task.result?.path) {
              console.log(chalk.green(`  📁 ${task.result.path}`));
            }
          } else {
            s.fail(`Failed: ${task.error}`);
          }

          console.log('');
        } catch (err) {
          if (err.name === 'ExitPromptError' || err.message?.includes('force closed')) {
            await browser.close();
            process.exit(0);
          }
          logger.error(err.message);
        }
      }
    };

    await loop();
  });

// Single exec
program
  .command('exec <command...>')
  .description('Execute single command')
  .action(async (parts) => {
    banner();
    await browser.launch({ headless: true });
    const task = await taskRunner.run(parts.join(' '));
    console.log(JSON.stringify(task.result, null, 2));
    await browser.close();
  });

// Dashboard
program
  .command('dashboard')
  .alias('dash')
  .description('Launch dashboard only')
  .action(async () => {
    banner();
    await browser.launch();
    startServer(taskRunner);
    logger.success(`Dashboard → http://localhost:${config.server.port}`);
    await open(`http://localhost:${config.server.port}`);
  });

// Shutdown handler
process.on('SIGINT', async () => {
  console.log(chalk.yellow('\nShutting down...'));
  await browser.close();
  process.exit(0);
});

process.on('unhandledRejection', err => logger.error(`Unhandled: ${err}`));

program.parse();
```

## 9. Dashboard HTML (Full Functional)

Ini file terbesar — dashboard lengkap yang bisa terkoneksi WebSocket ke server backend, menampilkan semua secara live:

HTML

```
<!-- src/dashboard/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🚀 Ultra Automation Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg0:#050a15;--bg1:#0a1628;--bg2:#0f1f38;--bg3:#142a4a;
  --bd:#1a3a60;--bd2:#245080;
  --t1:#e8edf5;--t2:#94a8c8;--t3:#506888;
  --accent:#3b82f6;--accentDim:rgba(59,130,246,.12);--accentGlow:rgba(59,130,246,.35);
  --ok:#22c55e;--okDim:rgba(34,197,94,.12);
  --warn:#f59e0b;--warnDim:rgba(245,158,11,.12);
  --err:#ef4444;--errDim:rgba(239,68,68,.12);
  --info:#06b6d4;--infoDim:rgba(6,182,212,.12);
  --purple:#a855f7;--purpleDim:rgba(168,85,247,.12);
  --pink:#ec4899;
  --g1:linear-gradient(135deg,#3b82f6,#8b5cf6);
  --g2:linear-gradient(135deg,#06b6d4,#3b82f6);
  --mono:'SF Mono','Menlo','Courier New',monospace;
  --sans:'SF Pro Text','Helvetica Neue','Segoe UI',system-ui,sans-serif;
}
html,body{height:100%;overflow:hidden}
body{font-family:var(--sans);background:var(--bg0);color:var(--t1);display:flex;flex-direction:column}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:var(--bg0)}
::-webkit-scrollbar-thumb{background:var(--bd);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--bd2)}

/* ===== HEADER ===== */
.hd{display:flex;align-items:center;justify-content:space-between;height:52px;padding:0 16px;background:var(--bg1);border-bottom:1px solid var(--bd);flex-shrink:0;position:relative}
.hd::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--g1)}
.hd-l{display:flex;align-items:center;gap:10px}
.logo{display:flex;align-items:center;gap:8px}
.logo-i{width:30px;height:30px;background:var(--g1);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 0 12px var(--accentGlow)}
.logo-t{font-size:14px;font-weight:700;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.badge{display:flex;align-items:center;gap:5px;padding:3px 9px;border-radius:14px;font-size:10px;font-weight:600}
.badge-ok{background:var(--okDim);color:var(--ok);border:1px solid rgba(34,197,94,.25)}
.badge-hw{background:var(--purpleDim);color:var(--purple);border:1px solid rgba(168,85,247,.25)}
.dot{width:6px;height:6px;border-radius:50%}
.dot-ok{background:var(--ok);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(34,197,94,.5)}50%{box-shadow:0 0 0 4px transparent}}
.hd-r{display:flex;gap:5px}
.hs{display:flex;flex-direction:column;align-items:center;padding:3px 12px;background:var(--bg2);border:1px solid var(--bd);border-radius:7px;min-width:58px}
.hs-l{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:var(--t3)}
.hs-v{font-family:var(--mono);font-size:15px;font-weight:700}
.c-blue{color:var(--accent)}.c-ok{color:var(--ok)}.c-warn{color:var(--warn)}.c-info{color:var(--info)}.c-purple{color:var(--purple)}

/* ===== CMD BAR ===== */
.cb{display:flex;align-items:center;gap:8px;padding:8px 16px;background:var(--bg1);border-bottom:1px solid var(--bd);flex-shrink:0}
.cb-p{font-family:var(--mono);font-size:13px;color:var(--accent);font-weight:700;white-space:nowrap}
.cb-iw{flex:1}
.cb-i{width:100%;padding:9px 14px;background:var(--bg0);border:1.5px solid var(--bd);border-radius:7px;color:var(--t1);font-family:var(--mono);font-size:12.5px;outline:none;transition:all .25s}
.cb-i:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accentDim)}
.cb-i::placeholder{color:var(--t3)}
.btn{padding:8px 16px;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap}
.btn-p{background:var(--g1);color:#fff}.btn-p:hover{transform:translateY(-1px);box-shadow:0 4px 12px var(--accentGlow)}
.btn-p:disabled{opacity:.5;transform:none;cursor:default}
.btn-g{background:var(--bg2);border:1px solid var(--bd);color:var(--t2)}.btn-g:hover{border-color:var(--accent);color:var(--accent)}

/* ===== QUICK ===== */
.qb{display:flex;align-items:center;gap:5px;padding:6px 16px;background:var(--bg1);border-bottom:1px solid var(--bd);flex-shrink:0;overflow-x:auto}
.qb::-webkit-scrollbar{height:3px}
.ql{font-size:9px;color:var(--t3);text-transform:uppercase;letter-spacing:1px;white-space:nowrap;margin-right:4px}
.qb-b{display:flex;align-items:center;gap:4px;padding:4px 10px;background:var(--bg2);border:1px solid var(--bd);border-radius:16px;color:var(--t2);font-size:10.5px;cursor:pointer;transition:all .2s;white-space:nowrap}
.qb-b:hover{border-color:var(--accent);color:var(--accent);background:var(--accentDim)}

/* ===== MAIN GRID ===== */
.mg{display:grid;grid-template-columns:1fr 320px;grid-template-rows:1fr 1fr;flex:1;gap:1px;background:var(--bd);overflow:hidden;min-height:0}
.pn{background:var(--bg0);display:flex;flex-direction:column;overflow:hidden;min-height:0}
.pn-h{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--bg2);border-bottom:1px solid var(--bd);flex-shrink:0}
.pn-t{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;color:var(--t2);text-transform:uppercase;letter-spacing:.4px}
.pn-ti{width:18px;height:18px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:10px}
.pn-a{display:flex;align-items:center;gap:5px}
.pb{padding:2px 7px;background:var(--bg0);border:1px solid var(--bd);border-radius:3px;color:var(--t3);font-size:9.5px;cursor:pointer;transition:all .15s}
.pb:hover{color:var(--accent);border-color:var(--accent)}
.pb.active{color:var(--accent);border-color:var(--accent)}

/* ===== LOG ===== */
.log-pn{grid-row:1/3}
.log-b{flex:1;overflow-y:auto;padding:6px;display:flex;flex-direction:column;gap:1px}
.le{display:grid;grid-template-columns:56px 48px 1fr;gap:5px;align-items:flex-start;padding:4px 7px;border-radius:4px;font-family:var(--mono);font-size:11px;border-left:2px solid transparent;animation:fadeIn .25s ease}
@keyframes fadeIn{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:translateX(0)}}
.le:hover{background:var(--bg2)}
.le-t{color:var(--t3);font-size:10px;padding-top:1px}
.le-b{padding:1px 4px;border-radius:2px;font-size:8.5px;font-weight:700;text-align:center;letter-spacing:.3px}
.le-m{color:var(--t2);line-height:1.5;word-break:break-all}
.le-info{border-left-color:var(--info)}.le-info .le-b{background:var(--infoDim);color:var(--info)}
.le-success{border-left-color:var(--ok)}.le-success .le-b{background:var(--okDim);color:var(--ok)}
.le-error{border-left-color:var(--err)}.le-error .le-b{background:var(--errDim);color:var(--err)}
.le-warn{border-left-color:var(--warn)}.le-warn .le-b{background:var(--warnDim);color:var(--warn)}
.le-task{border-left-color:var(--purple)}.le-task .le-b{background:var(--purpleDim);color:var(--purple)}
.le-download{border-left-color:var(--accent)}.le-download .le-b{background:var(--accentDim);color:var(--accent)}
.le-step{border-left-color:var(--pink)}.le-step .le-b{background:rgba(236,72,153,.12);color:var(--pink)}

/* DL Progress */
.dl-e{padding:7px 9px;background:var(--bg2);border:1px solid var(--bd);border-left:2px solid var(--accent);border-radius:5px;margin:2px 0;animation:fadeIn .25s}
.dl-h{display:flex;justify-content:space-between;font-size:10.5px;font-family:var(--mono);margin-bottom:4px}
.dl-n{color:var(--t1);font-weight:600}.dl-p{color:var(--accent);font-weight:700}
.dl-bar{height:4px;background:var(--bg0);border-radius:2px;overflow:hidden}
.dl-fill{height:100%;border-radius:2px;background:var(--g1);transition:width .4s ease}
.dl-f{display:flex;justify-content:space-between;font-size:9.5px;color:var(--t3);font-family:var(--mono);margin-top:3px}

/* Pipeline */
.pipe-e{padding:7px 9px;background:var(--bg2);border:1px solid var(--bd);border-left:2px solid var(--purple);border-radius:5px;margin:2px 0;animation:fadeIn .25s}
.pipe-t{font-size:10.5px;font-weight:600;color:var(--purple);margin-bottom:5px;display:flex;align-items:center;gap:4px}
.pipe-s{display:flex;align-items:center;gap:5px;padding:2px 0;font-size:10px;font-family:var(--mono)}
.pipe-n{width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:700;flex-shrink:0}
.pipe-s.done .pipe-n{background:var(--okDim);color:var(--ok)}
.pipe-s.act  .pipe-n{background:var(--warnDim);color:var(--warn);animation:pulse .8s infinite}
.pipe-s.wait .pipe-n{background:var(--bg0);color:var(--t3)}
.pipe-s.done .pipe-c{color:var(--t2)}.pipe-s.act .pipe-c{color:var(--warn);font-weight:600}
.pipe-s.wait .pipe-c{color:var(--t3)}
.pipe-d{margin-left:auto;color:var(--t3);font-size:9px}

/* ===== TASKS ===== */
.tk-b{flex:1;overflow-y:auto;padding:6px;display:flex;flex-direction:column;gap:3px}
.tk{display:flex;align-items:center;gap:7px;padding:7px 9px;background:var(--bg2);border-radius:6px;border:1px solid var(--bd);animation:fadeIn .25s;transition:border-color .2s}
.tk:hover{border-color:var(--bd2)}
.tk.running{border-color:var(--warn);animation:taskPulse 1.5s infinite}
@keyframes taskPulse{0%,100%{box-shadow:0 0 0 1px var(--warnDim)}50%{box-shadow:0 0 6px var(--warnDim)}}
.tk.done{border-left:3px solid var(--ok)}.tk.fail{border-left:3px solid var(--err)}
.tk-i{width:22px;height:22px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.tk-i.done{background:var(--okDim)}.tk-i.running{background:var(--warnDim)}.tk-i.fail{background:var(--errDim)}
.tk-info{flex:1;min-width:0}
.tk-act{font-size:11px;font-weight:600;color:var(--t1)}
.tk-det{font-size:9.5px;color:var(--t3);font-family:var(--mono);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px}
.tk-meta{display:flex;flex-direction:column;align-items:flex-end;gap:1px;flex-shrink:0}
.tk-sb{padding:1px 5px;border-radius:2px;font-size:8.5px;font-weight:700}
.tk-sb.done{background:var(--okDim);color:var(--ok)}.tk-sb.running{background:var(--warnDim);color:var(--warn)}.tk-sb.fail{background:var(--errDim);color:var(--err)}
.tk-dur{font-family:var(--mono);font-size:9.5px;color:var(--t3)}

/* ===== RESULT ===== */
.rs-b{flex:1;overflow-y:auto;padding:8px;font-family:var(--mono);font-size:11px}
.rs-b pre{white-space:pre-wrap;word-break:break-all;line-height:1.65}
.jk{color:var(--info)}.js{color:var(--ok)}.jn{color:var(--warn)}.jb{color:var(--purple)}.jnull{color:var(--err)}.jbr{color:var(--t2)}

/* Search results */
.sr{display:flex;flex-direction:column;gap:6px}
.sri{padding:8px 10px;background:var(--bg2);border:1px solid var(--bd);border-radius:6px;cursor:pointer;transition:all .2s}
.sri:hover{border-color:var(--accent)}
.sr-rk{font-size:9px;color:var(--t3)}.sr-tt{font-size:11.5px;font-weight:600;color:var(--accent);margin:2px 0}
.sr-url{font-size:9.5px;color:var(--ok);font-family:var(--mono);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:3px}
.sr-sn{font-size:10.5px;color:var(--t3);line-height:1.4}

/* Extracted data */
.ex-list{display:flex;flex-direction:column;gap:3px}
.ex-item{display:flex;align-items:center;gap:6px;padding:4px 7px;background:var(--bg2);border-radius:4px;font-size:10.5px;font-family:var(--mono)}
.ex-n{width:18px;height:18px;background:var(--bg0);border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:8.5px;color:var(--t3);flex-shrink:0}
.ex-t{flex:1;color:var(--t2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ex-link{color:var(--accent);cursor:pointer}.ex-link:hover{text-decoration:underline}

/* File tabs */
.ft{display:flex;border-bottom:1px solid var(--bd);flex-shrink:0;background:var(--bg2)}
.ft-b{flex:1;padding:6px 4px;background:transparent;border:none;color:var(--t3);font-size:10px;font-weight:500;cursor:pointer;border-bottom:2px solid transparent;transition:all .2s}
.ft-b:hover{color:var(--t2)}.ft-b.active{color:var(--accent);border-bottom-color:var(--accent)}
.fl-b{flex:1;overflow-y:auto;padding:5px}
.fi{display:flex;align-items:center;gap:7px;padding:6px 8px;border-radius:5px;cursor:pointer;transition:all .15s;border:1px solid transparent}
.fi:hover{background:var(--bg2);border-color:var(--bd)}
.fi-i{width:24px;height:24px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.fi-info{flex:1;min-width:0}
.fi-n{font-size:10.5px;font-family:var(--mono);color:var(--t1);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fi-s{font-size:9px;color:var(--t3);margin-top:1px}
.fi-new{padding:1px 4px;background:var(--okDim);color:var(--ok);border-radius:2px;font-size:8px;font-weight:700;flex-shrink:0}

/* ===== FOOTER ===== */
.ft-bar{display:flex;align-items:center;justify-content:space-between;padding:0 16px;height:32px;background:var(--bg1);border-top:1px solid var(--bd);flex-shrink:0;font-size:10.5px;color:var(--t3)}
.ft-stats{display:flex;gap:16px}
.fs-v{font-family:var(--mono);font-weight:600}
.fs-v.blue{color:var(--accent)}.fs-v.green{color:var(--ok)}.fs-v.amber{color:var(--warn)}.fs-v.purple{color:var(--purple)}
.ft-right{display:flex;align-items:center;gap:10px}
.br-st{display:flex;align-items:center;gap:4px;font-size:10.5px;color:var(--ok)}

/* ===== TOASTS ===== */
.toasts{position:fixed;top:60px;right:12px;z-index:9999;display:flex;flex-direction:column;gap:6px;pointer-events:none}
.toast{display:flex;align-items:flex-start;gap:8px;padding:10px 14px;background:var(--bg2);border:1px solid var(--bd);border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.5);min-width:250px;max-width:340px;pointer-events:all;animation:tIn .25s ease}
@keyframes tIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:translateX(0)}}
@keyframes tOut{from{opacity:1;transform:translateX(0)}to{opacity:0;transform:translateX(16px)}}
.toast.success{border-left:3px solid var(--ok)}.toast.error{border-left:3px solid var(--err)}
.toast.info{border-left:3px solid var(--info)}.toast.warning{border-left:3px solid var(--warn)}
.toast-ti{font-size:11px;font-weight:600;color:var(--t1)}.toast-mg{font-size:10px;color:var(--t3);margin-top:2px}

/* ===== EMPTY ===== */
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;height:70px;color:var(--t3);font-size:11px;gap:4px}
.empty-i{font-size:20px;opacity:.4}
</style>
</head>
<body>

<!-- HEADER -->
<header class="hd">
  <div class="hd-l">
    <div class="logo"><div class="logo-i">🚀</div><span class="logo-t">Ultra Automation</span></div>
    <div class="badge badge-ok" id="connBadge"><div class="dot dot-ok"></div>Connecting...</div>
    <div class="badge badge-hw">i5-10310U · macOS Tahoe</div>
  </div>
  <div class="hd-r">
    <div class="hs"><span class="hs-l">Tasks</span><span class="hs-v c-blue" id="hTasks">0</span></div>
    <div class="hs"><span class="hs-l">Pages</span><span class="hs-v c-warn" id="hPages">0</span></div>
    <div class="hs"><span class="hs-l">DL</span><span class="hs-v c-ok" id="hDl">0</span></div>
    <div class="hs"><span class="hs-l">Uptime</span><span class="hs-v c-info" id="hUp">0s</span></div>
  </div>
</header>

<!-- COMMAND BAR -->
<div class="cb">
  <span class="cb-p">auto ❯</span>
  <div class="cb-iw"><input type="text" class="cb-i" id="cmdIn" placeholder="Type a command... search, open, screenshot, extract, download, pipe ..." autocomplete="off"></div>
  <button class="btn btn-g" onclick="showHelpPanel()">? Help</button>
  <button class="btn btn-p" id="execBtn" onclick="exec()">▶ Execute</button>
</div>

<!-- QUICK ACTIONS -->
<div class="qb">
  <span class="ql">Quick:</span>
  <button class="qb-b" onclick="qc('search node.js best practices 2024')">🔍 Search</button>
  <button class="qb-b" onclick="qc('open https://github.com/trending')">🐙 GitHub</button>
  <button class="qb-b" onclick="qc('screenshot')">📸 Screenshot</button>
  <button class="qb-b" onclick="qc('extract links')">🔗 Links</button>
  <button class="qb-b" onclick="qc('extract images')">🖼️ Images</button>
  <button class="qb-b" onclick="qc('extract emails')">📧 Emails</button>
  <button class="qb-b" onclick="qc('extract tables')">📊 Tables</button>
  <button class="qb-b" onclick="qc('pdf report')">📄 PDF</button>
  <button class="qb-b" onclick="qc('pipe open https://npmjs.com | screenshot npm | extract links')">⚡ Pipeline</button>
  <button class="qb-b" onclick="qc('batch-download https://example.com/files')">⬇️ Batch DL</button>
  <button class="qb-b" onclick="qc('monitor https://news.ycombinator.com every 30s')">👁️ Monitor</button>
</div>

<!-- MAIN GRID -->
<div class="mg">

  <!-- LOG -->
  <div class="pn log-pn">
    <div class="pn-h">
      <div class="pn-t"><div class="pn-ti" style="background:var(--infoDim)">📋</div>Live Log<span id="logCnt" style="font-size:9px;color:var(--t3);font-weight:400">0</span></div>
      <div class="pn-a"><button class="pb" onclick="clearLog()">Clear</button></div>
    </div>
    <div class="log-b" id="logB"></div>
  </div>

  <!-- TASKS -->
  <div class="pn">
    <div class="pn-h">
      <div class="pn-t"><div class="pn-ti" style="background:var(--purpleDim)">⚙️</div>Tasks<span id="tkCnt" style="font-size:9px;color:var(--t3);font-weight:400">0</span></div>
      <div class="pn-a"><button class="pb" onclick="clearTasks()">Clear</button></div>
    </div>
    <div class="tk-b" id="tkB"><div class="empty"><span class="empty-i">⚙️</span>No tasks yet</div></div>
  </div>

  <!-- RESULT + FILES -->
  <div class="pn">
    <div class="pn-h">
      <div class="pn-t"><div class="pn-ti" style="background:var(--okDim)">📊</div>Output</div>
      <div class="pn-a">
        <button class="pb active" id="tbRes" onclick="setTab('res')">Result</button>
        <button class="pb" id="tbFiles" onclick="setTab('files')">Files</button>
      </div>
    </div>
    <!-- Result -->
    <div id="tabRes" class="rs-b"><div class="empty"><span class="empty-i">📊</span>Execute a command to see results</div></div>
    <!-- Files -->
    <div id="tabFiles" style="display:none;flex:1;overflow:hidden;display:none;flex-direction:column">
      <div class="ft">
        <button class="ft-b active" onclick="showFt(this,'dl')">⬇ Downloads</button>
        <button class="ft-b" onclick="showFt(this,'ss')">📸 Screenshots</button>
        <button class="ft-b" onclick="showFt(this,'dt')">📊 Data</button>
      </div>
      <div class="fl-b" id="flDl"></div>
      <div class="fl-b" id="flSs" style="display:none"></div>
      <div class="fl-b" id="flDt" style="display:none"></div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<footer class="ft-bar">
  <div class="ft-stats">
    <span>🌐 Pages: <span class="fs-v amber" id="fPg">0</span></span>
    <span>📸 Shots: <span class="fs-v purple" id="fSh">0</span></span>
    <span>⬇️ DL: <span class="fs-v blue" id="fDl">0</span></span>
    <span>📊 Data: <span class="fs-v green" id="fDt">0</span></span>
    <span>💾 <span class="fs-v amber" id="fSz">0 B</span></span>
  </div>
  <div class="ft-right">
    <div class="br-st"><div class="dot dot-ok"></div>Chromium · macOS Tahoe · i5-10310U</div>
  </div>
</footer>

<!-- TOASTS -->
<div class="toasts" id="toasts"></div>

<script>
// ==============================
// STATE
// ==============================
const S={
  ws:null,connected:false,
  logs:[],tasks:[],files:{dl:[],ss:[],dt:[]},
  stats:{tasks:0,pages:0,dl:0,shots:0,data:0},
  hist:[],hIdx:-1,running:false,autoScroll:true,
  start:Date.now(),tid:0,curTab:'res',curFt:'dl'
};

// ==============================
// WEBSOCKET
// ==============================
function connectWS(){
  try{
    const p=location.protocol==='https:'?'wss:':'ws:';
    S.ws=new WebSocket(`${p}//${location.host}`);
    S.ws.onopen=()=>{
      S.connected=true;
      document.getElementById('connBadge').innerHTML='<div class="dot dot-ok"></div>Live Connected';
      log('success','CONN','WebSocket connected to backend');
    };
    S.ws.onmessage=e=>{
      try{const m=JSON.parse(e.data);handleMsg(m)}catch{}
    };
    S.ws.onclose=()=>{
      S.connected=false;
      document.getElementById('connBadge').innerHTML='<div class="dot" style="background:var(--err)"></div>Disconnected';
      setTimeout(connectWS,3000);
    };
    S.ws.onerror=()=>{};
  }catch{
    // Demo mode (no backend)
    log('warn','DEMO','No backend detected — running in demo/preview mode');
  }
}

function handleMsg(m){
  if(m.type==='log')log(m.data.type,m.data.badge,m.data.message);
  if(m.type==='status')updateFromServer(m.data);
  if(m.type==='task'){
    const t=m.data;
    addTaskUI(t.action,t.detail||'',t.event==='complete'?'done':t.status,t.duration);
  }
  if(m.type==='result')showJSON(m.data.result||m.data);
  if(m.type==='init')updateFromServer(m.data);
}

function updateFromServer(d){
  if(!d)return;
  if(d.browser){
    S.stats.pages=d.browser.navigations||0;
    S.stats.dl=d.browser.downloads||0;
    S.stats.shots=d.browser.screenshots||0;
    el('hUp').textContent=d.browser.uptimeStr||'0s';
  }
  S.stats.tasks=d.done||0;
  updateStats();
}

function sendCmd(cmd){
  if(S.ws&&S.ws.readyState===1){
    S.ws.send(JSON.stringify({type:'command',data:cmd}));
    return true;
  }
  return false;
}

// ==============================
// UTILS
// ==============================
const el=id=>document.getElementById(id);
const delay=ms=>new Promise(r=>setTimeout(r,ms));
function time(){const d=new Date();return[d.getHours(),d.getMinutes(),d.getSeconds()].map(n=>String(n).padStart(2,'0')).join(':')}
function uptime(){const s=Math.floor((Date.now()-S.start)/1000);if(s<60)return s+'s';const m=Math.floor(s/60);return m<60?`${m}m ${s%60}s`:`${Math.floor(m/60)}h ${m%60}m`}
setInterval(()=>el('hUp').textContent=uptime(),1000);

// ==============================
// LOG
// ==============================
function log(type,badge,msg,extra=null){
  S.logs.push({type,badge,msg,time:time()});
  const b=el('logB');
  if(extra==='dl-start'){
    // handled in download sim
    return;
  }
  const d=document.createElement('div');
  d.className=`le le-${type}`;
  d.innerHTML=`<span class="le-t">${time()}</span><span class="le-b">${badge}</span><span class="le-m">${esc(msg)}</span>`;
  b.appendChild(d);
  el('logCnt').textContent=S.logs.length;
  if(S.autoScroll)b.scrollTop=b.scrollHeight;
}

function addDlProgress(id,name,total){
  const b=el('logB');
  const d=document.createElement('div');
  d.className='dl-e';d.id=`dl${id}`;
  d.innerHTML=`<div class="dl-h"><span class="dl-n">⬇ ${esc(name)}</span><span class="dl-p" id="dlP${id}">0%</span></div>
<div class="dl-bar"><div class="dl-fill" id="dlF${id}" style="width:0%"></div></div>
<div class="dl-f"><span id="dlI${id}">0 / ${total}</span><span id="dlS${id}">Starting...</span></div>`;
  b.appendChild(d);
  if(S.autoScroll)b.scrollTop=b.scrollHeight;
}

function updateDl(id,pct,current,speed){
  const f=el(`dlF${id}`),p=el(`dlP${id}`),i=el(`dlI${id}`),s=el(`dlS${id}`);
  if(f)f.style.width=pct+'%';if(p)p.textContent=pct+'%';
  if(i)i.textContent=current;if(s)s.textContent=speed;
  if(S.autoScroll)el('logB').scrollTop=999999;
}

function addPipeline(id,steps){
  const b=el('logB');
  const d=document.createElement('div');d.className='pipe-e';d.id=`pipe${id}`;
  d.innerHTML=`<div class="pipe-t">⚡ Pipeline · ${steps.length} steps</div>
<div id="pipeSteps${id}">${steps.map((s,i)=>`<div class="pipe-s wait" id="ps${id}-${i}"><div class="pipe-n">${i+1}</div><span class="pipe-c">${esc(s)}</span><span class="pipe-d" id="pd${id}-${i}"></span></div>`).join('')}</div>`;
  b.appendChild(d);
  if(S.autoScroll)b.scrollTop=b.scrollHeight;
}

function updatePipeStep(pipeId,stepIdx,status,dur){
  const s=el(`ps${pipeId}-${stepIdx}`);
  if(s){s.className=`pipe-s ${status}`;
    if(dur){const d=el(`pd${pipeId}-${stepIdx}`);if(d)d.textContent=dur}
  }
  if(S.autoScroll)el('logB').scrollTop=999999;
}

function clearLog(){el('logB').innerHTML='';S.logs=[];el('logCnt').textContent='0'}

// ==============================
// TASKS
// ==============================
function addTaskUI(action,detail,status,duration){
  const id=++S.tid;
  const t={id,action,detail,status,duration};
  S.tasks.unshift(t);renderTasks();
  S.stats.tasks=S.tasks.filter(x=>x.status==='done').length;
  updateStats();return id;
}

function renderTasks(){
  const b=el('tkB');
  if(!S.tasks.length){b.innerHTML='<div class="empty"><span class="empty-i">⚙️</span>No tasks yet</div>';return}
  const ic={done:'✅',running:'⏳',fail:'❌'};
  const lb={done:'DONE',running:'RUN',fail:'FAIL'};
  b.innerHTML=S.tasks.slice(0,25).map(t=>`<div class="tk ${t.status}">
<div class="tk-i ${t.status}">${ic[t.status]||'📋'}</div>
<div class="tk-info"><div class="tk-act">${esc(t.action)}</div><div class="tk-det">${esc(t.detail)}</div></div>
<div class="tk-meta"><span class="tk-sb ${t.status}">${lb[t.status]||'?'}</span>
<span class="tk-dur">${t.duration!=null?(t.duration>999?(t.duration/1000).toFixed(1)+'s':t.duration+'ms'):'...'}</span></div></div>`).join('');
  el('tkCnt').textContent=S.tasks.length;
}

function clearTasks(){S.tasks=[];renderTasks()}

// ==============================
// RESULTS
// ==============================
function setTab(t){
  S.curTab=t;
  el('tabRes').style.display=t==='res'?'block':'none';
  el('tabFiles').style.display=t==='files'?'flex':'none';
  el('tbRes').classList.toggle('active',t==='res');
  el('tbFiles').classList.toggle('active',t==='files');
}

function showJSON(data){
  setTab('res');
  const body=el('tabRes');
  if(!data){body.innerHTML='<div class="empty"><span class="empty-i">📊</span>No data</div>';return}
  const s=JSON.stringify(data,null,2);
  const h=s.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g,m=>{
    let c='jn';if(/^"/.test(m))c=/:$/.test(m)?'jk':'js';else if(/true|false/.test(m))c='jb';else if(/null/.test(m))c='jnull';
    return`<span class="${c}">${m}</span>`;
  });
  body.innerHTML=`<pre>${h}</pre>`;
}

function showSearch(results){
  setTab('res');
  el('tabRes').innerHTML=`<div class="sr">${results.map((r,i)=>`<div class="sri">
<div class="sr-rk">#${i+1}</div><div class="sr-tt">${esc(r.title)}</div>
<div class="sr-url">${esc(r.link)}</div><div class="sr-sn">${esc(r.snippet)}</div></div>`).join('')}</div>`;
}

function showExtracted(type,data){
  setTab('res');
  const isArr=Array.isArray(data);
  el('tabRes').innerHTML=`<div style="font-size:10.5px;color:var(--t3);margin-bottom:6px">Found <span style="color:var(--ok);font-weight:700">${isArr?data.length:Object.keys(data).length}</span> ${type}</div>
<div class="ex-list">${(isArr?data:[]).slice(0,30).map((item,i)=>{
    const txt=typeof item==='string'?item:(item.text||item.href||item.src||item.email||JSON.stringify(item));
    const isLink=typeof item==='object'&&(item.href||item.src);
    return`<div class="ex-item"><div class="ex-n">${i+1}</div><span class="ex-t ${isLink?'ex-link':''}">${esc(String(txt).substring(0,120))}</span></div>`;
  }).join('')}</div>`;
}

// ==============================
// FILES
// ==============================
function addFile(type,name,size){S.files[type].unshift({name,size});renderFiles();updateStats()}
function renderFiles(){
  const render=(type,elId,icon)=>{
    const b=el(elId);const f=S.files[type];
    if(!f.length){b.innerHTML='<div class="empty"><span class="empty-i">📁</span>No files</div>';return}
    b.innerHTML=f.map((x,i)=>`<div class="fi"><div class="fi-i" style="background:var(--accentDim)">${icon}</div>
<div class="fi-info"><div class="fi-n">${esc(x.name)}</div><div class="fi-s">${x.size}</div></div>
${i===0?'<span class="fi-new">NEW</span>':''}</div>`).join('');
  };
  render('dl','flDl','📥');render('ss','flSs','📸');render('dt','flDt','📊');
}

function showFt(btn,type){
  S.curFt=type;
  document.querySelectorAll('.ft-b').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  ['dl','ss','dt'].forEach(t=>{
    const e=el(`fl${t.charAt(0).toUpperCase()+t.slice(1)}`);
    if(e)e.style.display=t===type?'block':'none';
  });
}

function updateStats(){
  el('hTasks').textContent=S.stats.tasks;
  el('hPages').textContent=S.stats.pages;
  el('hDl').textContent=S.files.dl.length;
  el('fPg').textContent=S.stats.pages;
  el('fSh').textContent=S.files.ss.length;
  el('fDl').textContent=S.files.dl.length;
  el('fDt').textContent=S.files.dt.length;
  const total=S.files.dl.length+S.files.ss.length+S.files.dt.length;
  const sizes=['0 B','12 KB','89 KB','234 KB','512 KB','1.2 MB','2.4 MB','3.6 MB','5.1 MB'];
  el('fSz').textContent=sizes[Math.min(total,sizes.length-1)];
}

// ==============================
// TOAST
// ==============================
function toast(type,title,msg,dur=3500){
  const ic={success:'✅',error:'❌',info:'ℹ️',warning:'⚠️'};
  const c=el('toasts');const d=document.createElement('div');
  d.className=`toast ${type}`;
  d.innerHTML=`<span style="font-size:16px;flex-shrink:0">${ic[type]}</span><div><div class="toast-ti">${title}</div><div class="toast-mg">${msg}</div></div>`;
  c.appendChild(d);
  setTimeout(()=>{d.style.animation='tOut .25s ease forwards';setTimeout(()=>d.remove(),250)},dur);
}

// ==============================
// COMMAND INPUT
// ==============================
el('cmdIn').addEventListener('keydown',e=>{
  if(e.key==='Enter'){exec();return}
  if(e.key==='Escape'){e.target.value='';S.hIdx=-1;return}
  if(e.key==='ArrowUp'){e.preventDefault();if(S.hIdx<S.hist.length-1){S.hIdx++;e.target.value=S.hist[S.hist.length-1-S.hIdx]}}
  if(e.key==='ArrowDown'){e.preventDefault();if(S.hIdx>0){S.hIdx--;e.target.value=S.hist[S.hist.length-1-S.hIdx]}else{S.hIdx=-1;e.target.value=''}}
});

function qc(cmd){el('cmdIn').value=cmd;exec()}

async function exec(){
  const inp=el('cmdIn');const cmd=inp.value.trim();
  if(!cmd||S.running)return;
  S.hist.push(cmd);S.hIdx=-1;inp.value='';

  // Try backend first
  if(sendCmd(cmd)){
    log('task','CMD',`Sent: ${cmd}`);
    return;
  }

  // Demo mode simulation
  await simulate(cmd);
}

// ==============================
// SIMULATION ENGINE (Demo Mode)
// ==============================
async function simulate(cmd){
  S.running=true;
  el('execBtn').textContent='⏳';el('execBtn').disabled=true;
  const lo=cmd.toLowerCase().trim();

  log('task','CMD',`Executing: ${cmd}`);

  try{
    if(lo.startsWith('search ')||lo.startsWith('google '))await simSearch(cmd);
    else if(/^(open|go|visit|navigate)\s/.test(lo))await simNav(cmd);
    else if(/^(screenshot|capture|snap)/.test(lo))await simShot(cmd);
    else if(lo.startsWith('download '))await simDl(cmd);
    else if(lo.startsWith('extract '))await simExtract(cmd);
    else if(lo.startsWith('scrape '))await simScrape(cmd);
    else if(lo.startsWith('pdf'))await simPdf(cmd);
    else if(lo.startsWith('batch-download'))await simBatch(cmd);
    else if(lo.startsWith('pipe '))await simPipe(cmd);
    else if(lo.startsWith('monitor '))await simMonitor(cmd);
    else if(lo==='status')simStatus();
    else if(lo==='help')showHelpPanel();
    else if(lo==='clear'){clearLog();clearTasks();el('tabRes').innerHTML='<div class="empty"><span class="empty-i">📊</span>Cleared</div>'}
    else await simSearch(`search ${cmd}`);
  }catch(e){log('error','ERR',e.message);toast('error','Error',e.message)}

  S.running=false;
  el('execBtn').textContent='▶ Execute';el('execBtn').disabled=false;
}

async function simSearch(cmd){
  const q=cmd.replace(/^(search|google)\s+/i,'');
  const tid=addTaskUI('search',`"${q}"`,'running');
  log('info','INFO',`Searching: "${q}"`);await delay(300);
  log('info','NAV',`google.com/search?q=${encodeURIComponent(q)}`);await delay(800);
  log('info','INFO','Extracting results...');await delay(600);

  const R=[];for(let i=0;i<8;i++)R.push({
    title:[`Complete Guide to ${q}`,`${q} - Official Docs`,`Learn ${q} in 2024`,`${q} Best Practices`,`Getting Started with ${q}`,`${q} Tutorial - MDN`,`${q} Examples & Demos`,`Top ${q} Resources`][i],
    link:`https://example.com/${q.replace(/\s/g,'-').toLowerCase()}/${['guide','docs','learn','best-practices','getting-started','tutorial','examples','resources'][i]}`,
    snippet:`Comprehensive ${['guide','documentation','tutorial','article','reference','walkthrough','collection','overview'][i]} covering all aspects of ${q} with practical examples and code samples...`
  });

  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=1700+Math.random()*500|0;renderTasks();
  log('success','FOUND',`${R.length} results for "${q}"`);
  const fn=`search-${Date.now()}.json`;
  log('success','SAVED',`output/data/${fn}`);addFile('dt',fn,'12 KB');
  S.stats.pages++;updateStats();
  showSearch(R);toast('success','Search Complete',`${R.length} results`);
}

async function simNav(cmd){
  const url=cmd.replace(/^(open|go|visit|navigate)\s+(to\s+)?/i,'');
  const full=url.startsWith('http')?url:`https://${url}`;
  const tid=addTaskUI('navigate',full,'running');
  log('info','NAV',`→ ${full}`);await delay(400);
  log('info','WAIT','networkidle2...');await delay(1000);
  const title=`Page at ${full.split('/').slice(2,3).join('')}`;
  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=1400;renderTasks();
  log('success','LOAD',`${title} [200]`);
  S.stats.pages++;updateStats();
  showJSON({url:full,title,status:200,loadTime:'1.4s'});
  toast('success','Page Loaded',title);
}

async function simShot(cmd){
  const name=(cmd.replace(/^(screenshot|capture|snap)\s*/i,'').trim()||`screenshot-${Date.now()}`)+'.png';
  const tid=addTaskUI('screenshot',name,'running');
  log('info','SNAP','Capturing full-page...');await delay(700);
  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=700;renderTasks();
  log('success','SAVED',`output/screenshots/${name}`);
  S.stats.shots++;addFile('ss',name,`${(700+Math.random()*400|0)} KB`);updateStats();
  showJSON({file:`output/screenshots/${name}`,fullPage:true,width:1920,height:5200});
  toast('success','Screenshot',name);
}

async function simDl(cmd){
  const m=cmd.match(/download\s+(.+?)(?:\s+as\s+(.+))?$/i);if(!m)return;
  const url=m[1],name=m[2]||url.split('/').pop()||`file-${Date.now()}`;
  const total=`${(100+Math.random()*900|0)} KB`;
  const tid=addTaskUI('download',name,'running');
  const dlId=Date.now();
  addDlProgress(dlId,name,total);

  for(let p=0;p<=100;p+=Math.random()*18+6|0){
    const pct=Math.min(p,100);
    await delay(180);
    updateDl(dlId,pct,`${(parseInt(total)*pct/100|0)} KB / ${total}`,`${(120+Math.random()*200|0)} KB/s`);
  }
  updateDl(dlId,100,total,'Done');

  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=2000;renderTasks();
  log('success','DONE',`Downloaded: ${name} (${total})`);
  addFile('dl',name,total);updateStats();
  showJSON({file:`output/downloads/${name}`,size:total,url});
  toast('success','Downloaded',`${name} (${total})`);
}

async function simExtract(cmd){
  const m=cmd.match(/extract\s+(links|images|text|emails|tables|scripts|meta|styles)/i);
  const type=m?m[1].toLowerCase():'links';
  const tid=addTaskUI(`extract:${type}`,type,'running');
  log('info','INFO',`Extracting ${type}...`);await delay(300);
  log('info','SCAN','Scanning DOM...');await delay(600);

  const counts={links:89,images:23,text:1,emails:5,tables:3,scripts:18,meta:12,styles:6};
  const cnt=counts[type]||10;
  let data;

  if(type==='links')data=Array.from({length:Math.min(cnt,20)},(_,i)=>({text:['Docs','API','Guide','GitHub','Blog','About','Contact','Download','Pricing','Features','Support','Login','Register','Dashboard','Settings','Help','FAQ','Terms','Privacy','Changelog'][i],href:`https://example.com/${['docs','api','guide','github','blog','about','contact','download','pricing','features','support','login','register','dashboard','settings','help','faq','terms','privacy','changelog'][i]}`}));
  else if(type==='emails')data=['info@example.com','support@company.io','hello@startup.dev','admin@site.org','press@brand.com'];
  else if(type==='images')data=Array.from({length:8},(_,i)=>({src:`https://cdn.example.com/img/${i+1}.webp`,alt:`Image ${i+1}`,width:[800,1200,400,960,640,1920,480,320][i]}));
  else data={type,count:cnt,extractedAt:new Date().toISOString()};

  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=900;renderTasks();
  log('success','DONE',`Extracted ${cnt} ${type}`);
  const fn=`extract-${type}-${Date.now()}.json`;
  addFile('dt',fn,`${cnt} KB`);updateStats();
  showExtracted(type,data);
  toast('success',`Extracted ${type}`,`${cnt} items`);
}

async function simScrape(cmd){
  const url=cmd.replace(/^scrape\s+/i,'').trim();
  const tid=addTaskUI('scrape',url,'running');
  log('info','NAV',`→ ${url}`);await delay(500);
  log('info','PARSE','Analyzing DOM structure...');await delay(700);
  log('info','INFO','Extracting metadata, headings, stats...');await delay(500);
  const data={url,title:'Scraped Page',meta:{description:'Page meta description'},headings:{h1:['Main'],h2:['Sec 1','Sec 2'],h3:['Sub 1','Sub 2']},stats:{links:127,images:34,forms:2,words:8924}};
  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=1700;renderTasks();
  log('success','DONE',`Scraped: ${data.stats.links} links, ${data.stats.images} images, ${data.stats.words} words`);
  const fn=`scrape-${Date.now()}`;
  addFile('dt',fn+'.json','45 KB');addFile('dt',fn+'.html','189 KB');updateStats();
  showJSON(data);toast('success','Page Scraped',`${data.stats.links} links`);
}

async function simPdf(cmd){
  const name=(cmd.replace(/^pdf\s*/i,'').trim()||`page-${Date.now()}`)+'.pdf';
  const tid=addTaskUI('pdf',name,'running');
  log('info','INFO','Generating PDF...');await delay(500);
  log('info','RENDER','CSS, fonts, images...');await delay(900);
  log('info','WRITE','Writing to disk...');await delay(500);
  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=1900;renderTasks();
  log('success','DONE',`output/downloads/${name}`);
  addFile('dl',name,'1.4 MB');updateStats();
  showJSON({file:`output/downloads/${name}`,format:'A4',pages:8,size:'1.4 MB'});
  toast('success','PDF Saved',name);
}

async function simBatch(cmd){
  const url=cmd.replace(/^batch-download\s+/i,'').trim();
  const tid=addTaskUI('batch-dl',url,'running');
  log('info','SCAN',`Scanning: ${url}`);await delay(600);

  const files2=[
    {n:'express-guide.pdf',s:'245 KB'},{n:'nodejs-cheat.pdf',s:'89 KB'},
    {n:'react-tutorial.zip',s:'1.2 MB'},{n:'vue-starter.zip',s:'876 KB'},{n:'data.csv',s:'45 KB'}
  ];
  log('info','FOUND',`${files2.length} downloadable files`);

  for(let i=0;i<files2.length;i++){
    const f=files2[i];const did=Date.now()+i;
    addDlProgress(did,f.n,f.s);
    for(let p=0;p<=100;p+=25){await delay(120);updateDl(did,Math.min(p,100),`${f.s}`,'')}
    addFile('dl',f.n,f.s);updateStats();
  }

  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=3000;renderTasks();
  log('success','DONE',`Batch: ${files2.length}/${files2.length} files`);
  showJSON({source:url,total:files2.length,downloaded:files2.length,files:files2});
  toast('success','Batch Complete',`${files2.length} files`);
}

async function simPipe(cmd){
  const steps=cmd.replace(/^pipe\s+/i,'').split('|').map(s=>s.trim());
  const tid=addTaskUI('pipeline',`${steps.length} steps`,'running');
  const pid=Date.now();
  addPipeline(pid,steps);await delay(200);

  for(let i=0;i<steps.length;i++){
    updatePipeStep(pid,i,'act');
    log('step',`${i+1}/${steps.length}`,steps[i]);
    await delay(500+Math.random()*700|0);
    const dur=`${(.3+Math.random()*1.2).toFixed(1)}s`;
    updatePipeStep(pid,i,'done',dur);
  }

  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=steps.length*800;renderTasks();
  log('success','DONE',`Pipeline: ${steps.length}/${steps.length} steps ✔`);
  toast('success','Pipeline Complete',`${steps.length} steps`);
}

async function simMonitor(cmd){
  const m=cmd.match(/monitor\s+(.+?)(?:\s+every\s+(\d+)s?)?$/i);
  const url=m?m[1]:cmd;const iv=m?parseInt(m[2])||30:30;
  const tid=addTaskUI('monitor',`${url} / ${iv}s`,'running');
  log('info','MON',`Watching: ${url} every ${iv}s`);await delay(500);
  log('success','CHECK','#1: Baseline captured');await delay(800);
  log('success','CHECK','#2: No changes');await delay(500);
  log('warn','CHANGE','⚡ #3: Content changed! (length: 8924 → 9102)');
  log('success','SNAP',`Screenshot: monitor-change-${Date.now()}.png`);
  addFile('ss',`monitor-change-${Date.now()}.png`,'892 KB');updateStats();
  S.tasks.find(t=>t.id===tid).status='done';S.tasks.find(t=>t.id===tid).duration=1800;renderTasks();
  toast('warning','Change Detected!',url);
}

function simStatus(){
  showJSON({
    machine:'ThinkPad X13 Yoga Gen1',cpu:'i5-10310U',os:'macOS Tahoe 26.5',
    browser:{running:true,pages:S.stats.pages,downloads:S.files.dl.length,screenshots:S.files.ss.length},
    tasks:{done:S.tasks.filter(t=>t.status==='done').length,failed:S.tasks.filter(t=>t.status==='fail').length},
    output:{downloads:S.files.dl.length,screenshots:S.files.ss.length,data:S.files.dt.length},
    uptime:uptime()
  });
  log('info','STATUS',`Tasks: ${S.stats.tasks} · Pages: ${S.stats.pages} · DL: ${S.files.dl.length} · Uptime: ${uptime()}`);
}

// ==============================
// HELP
// ==============================
function showHelpPanel(){
  setTab('res');
  const cmds=[
    {c:'search <query>',d:'Google search & save results'},
    {c:'open <url>',d:'Navigate to URL'},
    {c:'screenshot [name]',d:'Full-page screenshot'},
    {c:'download <url> [as name]',d:'Download with progress'},
    {c:'scrape <url>',d:'Full page data extraction'},
    {c:'extract links|images|emails|tables',d:'Extract specific data'},
    {c:'pdf [name]',d:'Save page as PDF'},
    {c:'batch-download <url>',d:'Download all files from page'},
    {c:'pipe cmd1 | cmd2 | cmd3',d:'Chain commands'},
    {c:'monitor <url> [every Ns]',d:'Watch for page changes'},
    {c:'status',d:'System statistics'},
    {c:'clear',d:'Clear all panels'},
    {c:'help',d:'This help'},
  ];

  el('tabRes').innerHTML=`<div style="margin-bottom:10px">
<div style="font-size:12px;font-weight:700;color:var(--accent);margin-bottom:3px">🚀 Ultra Automation Commands</div>
<div style="font-size:10px;color:var(--t3)">↑↓ History · Enter Execute · Esc Clear · macOS Tahoe · i5-10310U</div></div>
${cmds.map(c=>`<div style="display:flex;gap:10px;padding:6px 8px;border-radius:4px;border:1px solid var(--bd);margin-bottom:3px;background:var(--bg2)">
<span style="font-family:var(--mono);font-size:10.5px;color:var(--ok);min-width:200px;flex-shrink:0">${c.c}</span>
<span style="font-size:10.5px;color:var(--t3)">${c.d}</span></div>`).join('')}
<div style="margin-top:8px;padding:7px 9px;background:var(--accentDim);border-radius:4px;border:1px solid var(--bd)">
<div style="font-size:10.5px;color:var(--accent);font-weight:600;margin-bottom:3px">💡 Examples</div>
<div style="font-family:var(--mono);font-size:10px;color:var(--t3);line-height:1.8">search node.js best practices 2024
open https://github.com/trending
pipe open https://npmjs.com | screenshot | extract links
download https://example.com/docs.pdf as my-docs.pdf
monitor https://news.ycombinator.com every 60s</div></div>`;
}

function esc(s){if(typeof s!=='string')return s;return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

// ==============================
// INIT
// ==============================
renderFiles();updateStats();
connectWS();

(async()=>{
  await delay(500);
  log('info','SYS','🚀 Ultra Automation Dashboard v2.0');
  log('info','HW','ThinkPad X13 Yoga Gen1 · i5-10310U · Intel UHD 620');
  log('info','OS','macOS Tahoe 26.5 (Hackintosh) · GPU sandbox disabled');
  await delay(400);
  log('success','READY','All systems operational');
  log('info','TIP','Try: search javascript automation — or click Quick Actions above');
  await delay(1500);

  // Auto-demo
  await simulate('search node.js automation frameworks 2024');
})();
</script>
</body>
</html>
```

---

## 🚀 Cara Install & Jalankan

Bash

```
# 1. Clone / buat folder project
mkdir ultra-automation && cd ultra-automation

# 2. Buat semua file sesuai struktur di atas
# Atau copy-paste semua code blocks

# 3. Install
npm install

# 4. Jalankan Mode Interactive + Dashboard
node src/index.js --dashboard

# 5. Atau dashboard saja
node src/index.js dashboard

# 6. Atau single command
node src/index.js exec "search puppeteer tutorial"

# 7. Buka dashboard di browser
open http://localhost:3456

# 8. Untuk preview HTML tanpa backend:
open src/dashboard/index.html
```

### Khusus Hackintosh ThinkPad X13 Yoga

Bash

```
# Jika Chromium crash karena Intel UHD 620:
PUPPETEER_CHROMIUM_REVISION=latest \
DISABLE_GPU_SANDBOX=1 \
node src/index.js --dashboard

# Atau gunakan launch script:
chmod +x launch.sh
./launch.sh --dashboard
```

Dashboard HTML bisa langsung dibuka tanpa backend (demo mode) — atau terkoneksi real ke backend Node.js via WebSocket untuk operasi nyata. Semua output masuk ke `./output/` di directory project.