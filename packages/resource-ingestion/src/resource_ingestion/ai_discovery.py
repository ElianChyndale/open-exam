from __future__ import annotations

import json
import os
from typing import Any


PROMPT_VERSION = "resource-ai-discovery-v1"


def openai_web_search(query: str) -> dict[str, Any]:
    """Discover public URL candidates with the hosted OpenAI web-search tool."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise PermissionError("OpenAI Web Search requires OPENAI_API_KEY.")
    from agents import Agent, Runner, WebSearchTool

    prompt = (
        "Find public internet resources relevant to the query. Return JSON only with a "
        "'candidates' array. Each candidate must contain url, title, confidence from 0 to 1, "
        "and citations as a list of source URLs. Do not include login-only resources.\n\n"
        f"Query: {query}"
    )
    agent = Agent(
        name="resource_discovery",
        instructions="Use web search for discovery only. Return compact JSON and preserve citations.",
        model=os.environ.get("OPENEXAM_OPENAI_WEB_SEARCH_MODEL", "gpt-5-mini"),
        tools=[WebSearchTool()],
    )
    result = Runner.run_sync(agent, prompt)
    output = str(result.final_output).strip()
    if output.startswith("```"):
        output = output.strip("`")
        if output.startswith("json"):
            output = output[4:].lstrip()
    parsed = json.loads(output)
    if not isinstance(parsed, dict) or not isinstance(parsed.get("candidates"), list):
        raise ValueError("OpenAI Web Search returned an invalid discovery payload.")
    return {"model": agent.model, "cost": 0.0, "candidates": parsed["candidates"]}
