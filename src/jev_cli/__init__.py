#!/usr/bin/env python3
"""Small, dependency-free CLI for TypeSafe Jev."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://api.typesafe.ai/v1/systemone"
CREDENTIALS_FILE = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "jev-cli" / "credentials.json"


class CliError(Exception):
    def __init__(self, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def api_key() -> str:
    if value := os.environ.get("TYPESAFE_API_KEY"):
        return value
    try:
        data = json.loads(CREDENTIALS_FILE.read_text())
        value = data["api_key"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise CliError(
            "TypeSafe API key is not stored; run: pbpaste | jev-cli auth set",
            3,
        ) from exc
    if not isinstance(value, str) or not value:
        raise CliError("stored TypeSafe API key is empty", 3)
    return value


def set_api_key() -> None:
    if sys.stdin.isatty():
        raise CliError("API key must be piped to stdin; example: pbpaste | jev-cli auth set")
    value = sys.stdin.read().strip()
    if not value:
        raise CliError("API key is empty")
    CREDENTIALS_FILE.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        fd, temporary = tempfile.mkstemp(dir=CREDENTIALS_FILE.parent)
        with os.fdopen(fd, "w") as file:
            json.dump({"api_key": value}, file)
            file.write("\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, CREDENTIALS_FILE)
    except OSError as exc:
        raise CliError("could not write the Jev credential store", 3) from exc


def read_text(value: str | None) -> str:
    if value is None or value == "-":
        if sys.stdin.isatty():
            raise CliError("state is required as an argument, @file, or stdin")
        return sys.stdin.read()
    if value.startswith("@"):
        try:
            return Path(value[1:]).read_text()
        except OSError as exc:
            raise CliError(f"cannot read state file: {exc}") from exc
    return value


def state_value(value: str | None, force_json: bool) -> Any:
    text = read_text(value)
    if force_json:
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise CliError(f"invalid JSON state: {exc}") from exc
    return text


def split_pair(value: str) -> tuple[str, str]:
    key, separator, description = value.partition("=")
    if not separator or not key or not description:
        raise argparse.ArgumentTypeError("expected KEY=DESCRIPTION")
    return key, description


def load_request(path: str) -> dict[str, Any]:
    text = read_text("-" if path == "-" else f"@{path}")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid request JSON: {exc}") from exc
    if not isinstance(payload, dict) or "state" not in payload or "questions" not in payload:
        raise CliError("request must be an object containing state and questions")
    return payload


def call(payload: dict[str, Any], endpoint: str) -> dict[str, Any]:
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode(),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "User-Agent": "jev-cli/0.2.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        try:
            detail = json.loads(body)
        except json.JSONDecodeError:
            detail = body
        code = 3 if exc.code in (401, 403) else 4 if exc.code in (429, 500, 502, 503, 504) else 1
        raise CliError(f"API HTTP {exc.code}: {json.dumps(detail, ensure_ascii=False)}", code) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise CliError(f"API connection failed: {exc}", 4) from exc
    if not isinstance(result, dict):
        raise CliError("API returned a non-object response", 1)
    return result


def common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--model", default="jev-latest", help="model name (default: jev-latest)")
    parser.add_argument("--json-state", action="store_true", help="parse state as JSON")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    parser.add_argument("--value", action="store_true", help="print only the primary answer value")
    parser.add_argument("--endpoint", default=os.environ.get("TYPESAFE_API_URL", API_URL), help=argparse.SUPPRESS)
    return parser


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="jev-cli",
        description="Evaluate text or JSON with TypeSafe Jev. Uses its own local credential store.",
    )
    root.add_argument("--version", action="version", version="jev-cli 0.2.0")
    sub = root.add_subparsers(dest="command", required=True)
    common = common_parser()

    auth = sub.add_parser("auth", help="manage the API key in the Jev credential store")
    auth_sub = auth.add_subparsers(dest="auth_command", required=True)
    auth_sub.add_parser("set", help="store an API key read from stdin")
    auth_sub.add_parser("status", help="check whether an API key is stored")

    noul = sub.add_parser("noul", parents=[common], help="answer one yes/no question with a probability")
    noul.add_argument("question")
    noul.add_argument("state", nargs="?", help="text, @file, or - for stdin")

    choice = sub.add_parser("choice", parents=[common], help="choose one option")
    choice.add_argument("question")
    choice.add_argument("state", nargs="?", help="text, @file, or - for stdin")
    choice.add_argument("-o", "--option", action="append", type=split_pair, required=True, metavar="KEY=DESCRIPTION")

    score = sub.add_parser("score", parents=[common], help="score against ordered levels")
    score.add_argument("question")
    score.add_argument("state", nargs="?", help="text, @file, or - for stdin")
    score.add_argument("-l", "--level", action="append", required=True, metavar="DESCRIPTION")

    run = sub.add_parser("run", parents=[common], help="send a complete request JSON for batched questions")
    run.add_argument("request", help="JSON file or - for stdin")
    return root


def request_for(args: argparse.Namespace) -> tuple[dict[str, Any], str | None]:
    if args.command == "run":
        payload = load_request(args.request)
        payload.setdefault("model", args.model)
        return payload, None

    question: dict[str, Any] = {"type": args.command, "instructions": args.question}
    if args.command == "choice":
        question["criteria"] = dict(args.option)
    elif args.command == "score":
        question["criteria"] = args.level
    payload = {
        "state": state_value(args.state, args.json_state),
        "model": args.model,
        "questions": {"answer": question},
    }
    return payload, args.command


def primary_value(result: dict[str, Any], kind: str | None) -> Any:
    if kind is None:
        raise CliError("--value is available only for noul, choice, and score")
    answer = result["answers"]["answer"]
    return answer[{"noul": "noul", "choice": "choice", "score": "score"}[kind]]


def main() -> int:
    try:
        args = parser().parse_args()
        if args.command == "auth":
            if args.auth_command == "set":
                set_api_key()
                print(json.dumps({"ok": True, "stored": True, "store": str(CREDENTIALS_FILE)}))
            else:
                api_key()
                print(json.dumps({"ok": True, "stored": True, "store": str(CREDENTIALS_FILE)}))
            return 0
        payload, kind = request_for(args)
        result = call(payload, args.endpoint)
        if args.value:
            print(primary_value(result, kind))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0
    except CliError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return exc.exit_code
    except (KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": f"unexpected API response: {exc}"}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
