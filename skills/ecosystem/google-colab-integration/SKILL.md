---
name: google-colab-integration
description: Use when integrating Google Colab. Cloud GPU/TPU notebooks.
category: ecosystem
---

# Google Colab — Integrasi Ekosistem

## Overview
Colab adalah hosted Jupyter Notebook service dari Google. Free GPU/TPU, no setup, integrated with Google Drive.

## Kapan pakai
- Eksperimen ML/model yang butuh GPU/TPU
- Prototyping cepat tanpa setup infra lokal
- Sharing notebook dengan tim
- Pipeline ML yang berjalan di cloud

## Limitasi
- Session timeout: 12 jam max, idle 90 menit
- GPU quota terbatas (free tier)
- Filesystem ephemeral (perlu mount Google Drive)
- Tidak cocok untuk production serving

## Integrasi dengan UTCP
Colab bisa menjadi tool provider via UTCP:

### Skenario 1: Colab sebagai endpoint
Host model/API di Colab via ngrok/cloudflare tunnel, panggil via UTCP:
```json
// providers.json
{
  "manual_call_templates": [{
    "name": "colab_model",
    "call_template_type": "http",
    "http_method": "POST",
    "url": "https://xxx.ngrok.io/predict",
    "content_type": "application/json"
  }]
}
```

### Skenario 2: Colab sebagai agent runner
Jalankan UTCP agent di Colab notebook:
```python
# Colab cell
!pip install utcp utcp-agent
import asyncio, os
from langchain_openai import ChatOpenAI
from utcp_agent import UtcpAgent

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
agent = await UtcpAgent.create(llm=llm, utcp_config={...})
response = await agent.chat("Analyze this data")
print(response)
```

### Skenario 3: Colab + UTCP untuk ML pipeline
- Colab menyediakan compute (GPU/TPU)
- UTCP memanggil model endpoint langsung (tanpa wrapper)
- Agent orchestrates multiple Colab-hosted models

## Setup Colab
1. Buka https://colab.research.google.com/
2. File → New Notebook
3. Runtime → Change runtime type → GPU/TPU
4. Install dependencies: `!pip install ...`
5. Mount Drive: `from google.colab import drive; drive.mount('/content/drive')`

## Konflik Check
- Colab tidak konflik dengan ekosistem existing (cloud-based, terpisah)
- Tidak perlu config change di ~/.hermes/config.yaml
- UTCP bridge memungkinkan Colab endpoint dipanggil dari Hermes agent

## Resources
- Colab: https://colab.research.google.com/
- Colab FAQ: https://research.google.com/colaboratory/faq.html
- Colab Notebooks: https://developers.google.com/colab/notebooks
- UTCP: https://github.com/universal-tool-calling-protocol
