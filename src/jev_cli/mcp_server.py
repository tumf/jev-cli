#!/usr/bin/env python3
"""Stdio MCP server exposing TypeSafe Jev judgments as typed tools.

The adapter owns only the MCP schema, input validation, transport startup, and the
translation of `CliError` into MCP tool errors. Provider selection, credential lookup,
request translation, and response normalization stay in `jev_cli` and are called
directly; the `jev` CLI is never spawned as a subprocess.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from . import (
    PROVIDERS,
    CliError,
    call,
    provider_endpoint,
    provider_model,
    question_request,
)

Provider = Literal["official", "vercel", "openrouter", "custom"]

logger = logging.getLogger(__name__)

mcp = MCPServer(
    name="jev",
    title="TypeSafe Jev",
    version="0.5.0",
    instructions=(
        "Ask TypeSafe Jev typed questions about text or JSON state. Use noul for a yes/no "
        "probability, choice for one key from explicit options, score for an ordered level, "
        "and run for a complete multi-question request. State is sent verbatim."
    ),
)


def selected_provider(provider: str | None) -> str:
    """Resolve the provider exactly as the CLI does: explicit value, then JEV_PROVIDER, then official."""
    value = provider or os.environ.get("JEV_PROVIDER", "official")
    if value not in PROVIDERS:
        raise ToolError(f"invalid JEV_PROVIDER: {value}")
    return value


def evaluate(payload: dict[str, Any], provider: str, endpoint: str | None) -> dict[str, Any]:
    """Send a prepared request through the shared client and bound every failure to a tool error."""
    try:
        return call(payload, provider_endpoint(provider, endpoint), provider)
    except CliError as exc:
        raise ToolError(str(exc)) from exc
    except (KeyError, TypeError) as exc:
        raise ToolError(f"unexpected API response: {exc}") from exc


def judge(
    kind: str,
    state: Any,
    question: str,
    criteria: Any,
    provider: str | None,
    model: str | None,
    endpoint: str | None,
) -> dict[str, Any]:
    selected = selected_provider(provider)
    payload = question_request(kind, state, question, criteria, model or provider_model(selected))
    return evaluate(payload, selected, endpoint)


@mcp.tool()
def noul(
    state: Any,
    question: str,
    provider: Provider | None = None,
    model: str | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Answer one yes/no question about the state with a probability from 0 to 1.

    The state is sent verbatim; `-` and `@path` are literal strings here, not stdin or a file.
    """
    return judge("noul", state, question, None, provider, model, endpoint)


@mcp.tool()
def choice(
    state: Any,
    question: str,
    options: dict[str, str],
    provider: Provider | None = None,
    model: str | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Select exactly one option key for the state from a map of at least two key/description pairs.

    The state is sent verbatim; `-` and `@path` are literal strings here, not stdin or a file.
    """
    # A single option is not a choice, so the minimum useful cardinality is two.
    if len(options) < 2:
        raise ToolError("choice requires an options map with at least two entries")
    if any(not key or not description for key, description in options.items()):
        raise ToolError("choice options require a non-empty key and description")
    return judge("choice", state, question, options, provider, model, endpoint)


@mcp.tool()
def score(
    state: Any,
    question: str,
    levels: list[str],
    provider: Provider | None = None,
    model: str | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Score the state against at least two ordered levels, numbered from zero in the supplied order.

    The state is sent verbatim; `-` and `@path` are literal strings here, not stdin or a file.
    """
    # A single level is not a scale, so the minimum useful cardinality is two.
    if len(levels) < 2:
        raise ToolError("score requires a levels list with at least two entries")
    if any(not level for level in levels):
        raise ToolError("score levels require a non-empty description")
    return judge("score", state, question, levels, provider, model, endpoint)


@mcp.tool()
def run(
    request: dict[str, Any],
    provider: Provider | None = None,
    model: str | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Send a complete System One request object containing `state` and `questions`.

    An explicit `model` overrides the request model; otherwise the request model is kept and
    the provider default is added only when the request omits it.
    """
    if not isinstance(request, dict) or "state" not in request or "questions" not in request:
        raise ToolError("request must be an object containing state and questions")
    selected = selected_provider(provider)
    payload = dict(request)
    if model:
        payload["model"] = model
    else:
        payload.setdefault("model", provider_model(selected))
    return evaluate(payload, selected, endpoint)


def main() -> int:
    # stdout carries MCP protocol frames only, so diagnostics go to stderr.
    logging.basicConfig(level=os.environ.get("JEV_MCP_LOG_LEVEL", "WARNING"), stream=sys.stderr)
    mcp.run("stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
