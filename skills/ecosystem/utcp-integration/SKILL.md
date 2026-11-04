---
name: utcp-integration
description: Use when integrating UTCP. Direct native endpoint calls.
category: ecosystem
---

# UTCP — Universal Tool Calling Protocol

## Overview
UTCP is an open standard (MPL-2.0) alternative to MCP. Instead of proxying calls through wrapper servers, UTCP describes *how* to call native endpoints directly (HTTP, gRPC, WebSocket, CLI).

## Key Concept
```
MCP:  Agent → MCP Server → Tool (wrapper tax, extra latency, infra)
UTCP: Agent → Tool (direct, native endpoint, zero wrapper)
```

## When to Use
- Tool already has HTTP API/OpenAPI spec → UTCP (zero wrapper)
- Latency critical → UTCP (direct call)
- Need server-side state/logic → MCP (wrapper can be stateful)
- Hybrid → UTCP-MCP Bridge

## Installation
```bash
pip install utcp          # Python client
pip install utcp-agent    # Ready-to-use agent
```

## Configuration (providers.json)
```json
{
  "manual_call_templates": [{
    "name": "my_api",
    "call_template_type": "http",
    "http_method": "GET",
    "url": "https://api.example.com/v1/data",
    "content_type": "application/json"
  }]
}
```

## Basic Usage
```python
import asyncio
from utcp.client import UtcpClient

async def main():
    client = await UtcpClient.create(
        config={"providers_file_path": "./providers.json"}
    )
    result = await client.call_tool(
        tool_name="my_api.get_data",
        arguments={"param": "value"}
    )
    print(result)

asyncio.run(main())
```

## UTCP + LLM (Agent Pattern)
```python
from utcp_agent import UtcpAgent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
agent = await UtcpAgent.create(llm=llm, utcp_config={...})
response = await agent.chat("Query that needs tools")
```

## Progressive Discovery
UTCP provides `search_tools()` — no need to load all schemas into prompt. LLM calls relevant tools only.

## UTCP-MCP Bridge
Connect existing MCP servers to UTCP:
```bash
pip install utcp-mcp  # Bridge: +230 tools via single MCP server
```

## Conflict Check with Existing Config
- Hermes MCP servers: filesystem, github, context7, composio — UTCP does NOT conflict (different layer)
- UTCP is complementary: use UTCP for native API calls, MCP for server-side logic
- No config changes needed in ~/.hermes/config.yaml
- UTCP runs as standalone Python library, not as MCP server

## Resources
- Spec: https://github.com/universal-tool-calling-protocol/utcp-specification
- GitHub: https://github.com/universal-tool-calling-protocol
- PyPI: https://pypi.org/project/utcp/
- Agent: https://github.com/universal-tool-calling-protocol/utcp-agent
- MCP Bridge: https://github.com/universal-tool-calling-protocol/utcp-mcp
