#!/bin/bash
# generate-html.sh - Generate HTML scaffold for Free-Tier Reels
# Usage: ./generate-html.sh [output-dir]
#
# This script generates the HTML scaffold file for HyperFrames composition
# that creates Instagram Reels (9:16 aspect ratio, 60 seconds total).
#
# For Niumination content creator: Afrizal Munthe
# Part of free-tier-reels-workflow skill class

set -e

# Default output directory
OUTPUT_DIR="${1:-~/Downloads/ide-reels-html}"

# Expand tilde
OUTPUT_DIR=$(eval echo "$OUTPUT_DIR")

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate HTML scaffold
cat > "$OUTPUT_DIR/index.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free-Tier Reels Composition</title>
    <style>
        :root {
            --bg: #0a0a0f;
            --fg: #e8e8f0;
            --accent: #ffd700;
            --muted: #6b6b80;
            --card: #1a1a24;
            --danger: #ff5252;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        html, body {
            width: 1080px;
            height: 1920px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--fg);
            overflow: hidden;
        }
        
        #root {
            width: 1080px;
            height: 1920px;
            position: relative;
        }
        
        .clip {
            position: absolute;
            min-height: 120px;
            padding: 40px;
            line-height: 1.4;
        }
        
        [data-track-index="1"] { top: 0; left: 0; }
        [data-track-index="2"] { top: 180px; left: 0; }
        [data-track-index="3"] { top: 360px; left: 0; }
        [data-track-index="4"] { top: 540px; left: 0; }
        [data-track-index="5"] { top: 720px; left: 0; }
        [data-track-index="6"] { top: 900px; left: 0; }
        
        .title-style {
            font-size: 80px;
            color: var(--fg);
            text-align: center;
            line-height: 1.2;
            padding: 60px;
        }
        
        .tool-title {
            font-size: 48px;
            color: var(--accent);
            margin-bottom: 20px;
            display: block;
        }
        
        .tool-desc {
            font-size: 24px;
            color: var(--fg);
            margin-bottom: 10px;
        }
        
        .tool-bullets {
            color: var(--muted);
            margin: 15px 0;
            min-height: 40px;
        }
        
        .bullet {
            display: block;
            margin: 4px 0;
            font-size: 20px;
        }
        
        .cta-style {
            font-size: 56px;
            color: var(--danger);
            padding: 40px;
            text-align: center;
            background: #fff5f5;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .watermark {
            position: absolute;
            bottom: 20px;
            right: 20px;
            font-size: 24px;
            color: rgba(255, 255, 255, 0.5);
            font-style: italic;
        }
    </style>
</head>
<body>
    <div id="root">
        <div class="clip title-style" data-start="0" data-duration="5" data-track-index="1">
            4 TOOLS AI GRATIS<br>UNTUK KONTEN<br>REELS
        </div>

        <div class="clip" data-start="5" data-duration="15" data-track-index="2">
            <div class="tool-title">TOOL 1: GHOST</div>
            <div class="tool-desc">Naskah jadi alami 1 klik</div>
            <div class="tool-bullets">
                <div class="bullet">AI humanizer otomatis</div>
                <div class="bullet">Gratis di Niumination</div>
                <div class="bullet">Built with Niumination</div>
            </div>
        </div>

        <div class="clip" data-start="20" data-duration="15" data-track-index="3">
            <div class="tool-title">TOOL 2: HYPERFRAMES</div>
            <div class="tool-desc">Video 9:16 viral dalam menit</div>
            <div class="tool-bullets">
                <div class="bullet">0 cost, 100% result</div>
                <div class="bullet">Render HTML jadi MP4</div>
                <div class="bullet">Built with Niumination</div>
            </div>
        </div>

        <div class="clip" data-start="35" data-duration="15" data-track-index="4">
            <div class="tool-title">TOOL 3: BAOYU INFOGRAPHIC</div>
            <div class="tool-desc">Carousel keren tanpa desain</div>
            <div class="tool-bullets">
                <div class="bullet">Rp50.000 jadi gratis</div>
                <div class="bullet">68 skill tersedia</div>
                <div class="bullet">Built with Niumination</div>
            </div>
        </div>

        <div class="clip" data-start="50" data-duration="10" data-track-index="5">
            <div class="tool-title">TOOL 4: MANIM VIDEO</div>
            <div class="tool-desc">Animasi eksplainer jual ribuan</div>
            <div class="tool-bullets">
                <div class="bullet">Gratis di Niumination</div>
                <div class="bullet">Buat educator & creator</div>
                <div class="bullet">Built with Niumination</div>
            </div>
        </div>

        <div class="clip cta-style" data-start="60" data-duration="5" data-track-index="6">
            Link di Bio<br>Untuk Dapet Semua Tool Gratis!
        </div>

        <div class="watermark">Built with Niumination</div>
    </div>
</body>
</html>
HTMLEOF

echo "HTML scaffold generated at: $OUTPUT_DIR/index.html"
echo ""
echo "Next steps:"
echo "1. Run: cd ~/Downloads/ide-reels-html && npm install hyperframes@latest"
echo "2. Run: npx hyperframes render --composition index.html --output ide5-reels-final.mp4 --width 1080 --height 1920 --duration 60 --fps 24 --audio none"
echo "3. Upload ide5-reels-final.mp4 ke Instagram Reels"