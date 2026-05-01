"""
FullStackArkham MCP Server

Model Context Protocol server for exposing agents to AI assistants.
Allows Claude, Cursor, and other AI assistants to:
- List available agents
- Execute agent actions
- Query workflow status
- Access knowledge graph
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ModuleNotFoundError:  # pragma: no cover - local unit tests may not install MCP runtime
    class Tool:  # type: ignore[override]
        def __init__(self, name: str, description: str, inputSchema: Dict[str, Any]):
            self.name = name
            self.description = description
            self.inputSchema = inputSchema

    class TextContent:  # type: ignore[override]
        def __init__(self, type: str, text: str):
            self.type = type
            self.text = text

    class Server:  # type: ignore[override]
        def __init__(self, name: str):
            self.name = name

        def list_tools(self):
            def decorator(func):
                return func
            return decorator

        def call_tool(self):
            def decorator(func):
                return func
            return decorator

        def create_initialization_options(self):
            return {}

        async def run(self, *_args, **_kwargs):
            raise RuntimeError("MCP runtime is not installed in this environment")

    class _StdioServerShim:
        async def __aenter__(self):
            return None, None

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def stdio_server():
        return _StdioServerShim()

SERVICE_ROOT = Path(__file__).resolve().parent
MEDIA_COMMERCE_ROOT = SERVICE_ROOT / "media-commerce"
if str(MEDIA_COMMERCE_ROOT) not in sys.path:
    sys.path.insert(0, str(MEDIA_COMMERCE_ROOT))

from app.agents import (  # type: ignore  # noqa: E402
    ChiefPulseAgent,
    ContentEngineAgent,
    DealFlowAgent,
    MediaCommerceAgent,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
app = Server("fullstackarkham")

# Agent definitions
AGENTS = {
    "ContentEngine": {
        "description": "Create and optimize content across all verticals",
        "tools": [
            {
                "name": "create_content_strategy",
                "description": "Create content strategy for a topic",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string", "description": "Tenant ID"},
                        "vertical": {"type": "string", "description": "Business vertical"},
                        "topic": {"type": "string", "description": "Content topic"},
                    },
                    "required": ["tenant_id", "vertical", "topic"],
                },
            },
            {
                "name": "generate_content",
                "description": "Generate content asset",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "vertical": {"type": "string"},
                        "content_type": {"type": "string"},
                        "topic": {"type": "string"},
                    },
                    "required": ["tenant_id", "vertical", "content_type", "topic"],
                },
            },
            {
                "name": "optimize_for_ai_seo",
                "description": "Optimize content for AI search engines",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "content_id": {"type": "string"},
                    },
                    "required": ["tenant_id", "content_id"],
                },
            },
        ],
    },
    "DealFlow": {
        "description": "Manage lead-to-revenue conversion and cross-vertical routing",
        "tools": [
            {
                "name": "score_lead",
                "description": "Score lead based on fit and intent",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "lead_id": {"type": "string"},
                        "vertical": {"type": "string"},
                    },
                    "required": ["tenant_id", "lead_id", "vertical"],
                },
            },
            {
                "name": "route_lead",
                "description": "Route lead to highest-LTV vertical (Scenario 5)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "lead_id": {"type": "string"},
                        "intent_signals": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["tenant_id", "lead_id", "intent_signals"],
                },
            },
            {
                "name": "generate_proposal",
                "description": "Generate sales proposal",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "deal_id": {"type": "string"},
                    },
                    "required": ["tenant_id", "deal_id"],
                },
            },
        ],
    },
    "MediaCommerce": {
        "description": "Monitor EPC and auto-optimize content monetization",
        "tools": [
            {
                "name": "monitor_epc",
                "description": "Monitor Earnings Per Click for content",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "content_id": {"type": "string"},
                    },
                    "required": ["tenant_id"],
                },
            },
            {
                "name": "auto_optimize_content",
                "description": "Auto-optimize content based on EPC (retire losers, scale winners)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "content_id": {"type": "string"},
                    },
                    "required": ["tenant_id", "content_id"],
                },
            },
            {
                "name": "repurpose_content",
                "description": "Repurpose top-performing content across formats",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "content_id": {"type": "string"},
                        "formats": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["tenant_id", "content_id"],
                },
            },
        ],
    },
    "ChiefPulse": {
        "description": "AI Chief of Staff - executive briefing and anomaly detection",
        "tools": [
            {
                "name": "generate_daily_briefing",
                "description": "Generate daily executive briefing",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "executive_id": {"type": "string"},
                    },
                    "required": ["tenant_id", "executive_id"],
                },
            },
            {
                "name": "get_approval_queue",
                "description": "Get items requiring executive approval",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "executive_id": {"type": "string"},
                    },
                    "required": ["tenant_id", "executive_id"],
                },
            },
            {
                "name": "detect_anomalies",
                "description": "Detect anomalies across metrics",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tenant_id": {"type": "string"},
                        "threshold": {"type": "number", "description": "Deviation threshold (default 0.20)"},
                    },
                    "required": ["tenant_id"],
                },
            },
        ],
    },
}

AGENT_CLASSES = {
    "ContentEngine": ContentEngineAgent,
    "DealFlow": DealFlowAgent,
    "MediaCommerce": MediaCommerceAgent,
    "ChiefPulse": ChiefPulseAgent,
}

_AGENT_INSTANCES: Dict[str, Any] = {}


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available agent tools"""
    tools = []
    
    for agent_name, agent_data in AGENTS.items():
        for tool in agent_data["tools"]:
            tools.append(
                Tool(
                    name=f"{agent_name}.{tool['name']}",
                    description=f"{agent_data['description']}: {tool['description']}",
                    inputSchema=tool["input_schema"],
                )
            )
    
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute agent tool"""
    logger.info(f"Tool called: {name} with args: {arguments}")
    
    # Parse agent and tool name
    parts = name.split(".", 1)
    if len(parts) != 2:
        return [TextContent(type="text", text=json.dumps(_error_payload(
            error_type="invalid_tool_name",
            message=f"Invalid tool name: {name}",
        ), indent=2))]
    
    agent_name, tool_name = parts
    
    if agent_name not in AGENTS:
        return [TextContent(type="text", text=json.dumps(_error_payload(
            error_type="unknown_agent",
            message=f"Unknown agent: {agent_name}",
            agent=agent_name,
            tool=tool_name,
        ), indent=2))]

    result = await _execute_agent_tool(agent_name, tool_name, arguments)
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _execute_agent_tool(
    agent_name: str,
    tool_name: str,
    arguments: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute agent tool using the concrete media-commerce agent classes."""

    agent = _get_agent(agent_name)
    if agent is None:
        return _error_payload(
            error_type="unknown_agent",
            message=f"Unknown agent: {agent_name}",
            agent=agent_name,
            tool=tool_name,
        )

    valid_tools = {tool["name"] for tool in AGENTS.get(agent_name, {}).get("tools", [])}
    if tool_name not in valid_tools:
        return _error_payload(
            error_type="unknown_tool",
            message=f"Unknown tool for {agent_name}: {tool_name}",
            agent=agent_name,
            tool=tool_name,
        )

    if not hasattr(agent, tool_name):
        return _error_payload(
            error_type="unknown_tool",
            message=f"Unknown tool for {agent_name}: {tool_name}",
            agent=agent_name,
            tool=tool_name,
        )

    method = getattr(agent, tool_name)
    try:
        data = await method(**arguments)
    except TypeError as exc:
        return _error_payload(
            error_type="invalid_arguments",
            message=str(exc),
            agent=agent_name,
            tool=tool_name,
            details={"arguments": arguments},
        )
    except ValueError as exc:
        return _error_payload(
            error_type="invalid_arguments",
            message=str(exc),
            agent=agent_name,
            tool=tool_name,
            details={"arguments": arguments},
        )
    except Exception as exc:  # pragma: no cover - defensive catch for dispatcher
        logger.exception("Agent execution failed for %s.%s", agent_name, tool_name)
        return _error_payload(
            error_type="execution_failed",
            message=str(exc),
            agent=agent_name,
            tool=tool_name,
            details={"arguments": arguments},
        )

    return {
        "agent": agent_name,
        "tool": tool_name,
        "status": "success",
        "data": data,
    }


def _get_agent(agent_name: str) -> Any:
    if agent_name in _AGENT_INSTANCES:
        return _AGENT_INSTANCES[agent_name]

    agent_class = AGENT_CLASSES.get(agent_name)
    if agent_class is None:
        return None

    instance = agent_class()
    _AGENT_INSTANCES[agent_name] = instance
    return instance


def _error_payload(
    error_type: str,
    message: str,
    agent: Optional[str] = None,
    tool: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "agent": agent,
        "tool": tool,
        "status": "error",
        "error": {
            "type": error_type,
            "message": message,
        },
    }
    if details:
        payload["error"]["details"] = details
    return payload


async def main():
    """Run MCP server"""
    logger.info("Starting FullStackArkham MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
