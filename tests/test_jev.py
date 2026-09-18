import io
import json
import os
import unittest
import urllib.error
from email.message import Message
from unittest.mock import patch

import jev_cli as jev


class JevTest(unittest.TestCase):
    def test_choice_request(self):
        args = jev.parser().parse_args(
            [
                "choice",
                "--question",
                "Route?",
                "--state",
                "broken",
                "-o",
                "tech=Bug",
                "-o",
                "sales=Purchase",
            ]
        )
        payload, kind = jev.request_for(args)
        self.assertEqual(kind, "choice")
        self.assertEqual(payload["questions"]["answer"]["criteria"], {"tech": "Bug", "sales": "Purchase"})

    def test_short_options_for_question_and_state(self):
        args = jev.parser().parse_args(["noul", "-q", "Urgent?", "-s", "today", "--value"])
        payload, kind = jev.request_for(args)
        self.assertEqual(kind, "noul")
        self.assertEqual(payload["questions"]["answer"]["instructions"], "Urgent?")
        self.assertEqual(payload["state"], "today")
        self.assertTrue(args.value)

    def test_json_state_from_stdin(self):
        args = jev.parser().parse_args(
            ["noul", "--question", "Urgent?", "--state", "-", "--json-state"]
        )
        with patch("sys.stdin", io.StringIO('{"message":"today"}')):
            payload, _ = jev.request_for(args)
        self.assertEqual(payload["state"], {"message": "today"})

    def test_api_key_reads_credential_store(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(jev, "CREDENTIALS_FILE") as path:
            path.read_text.return_value = '{"api_key":"test-key"}'
            self.assertEqual(jev.api_key(), "test-key")

    def test_api_key_prefers_environment(self):
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "environment-key"}), patch.object(
            jev, "CREDENTIALS_FILE"
        ) as path:
            self.assertEqual(jev.api_key(), "environment-key")
            path.read_text.assert_not_called()

    def test_set_api_key_writes_private_credential_store(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory, patch.object(
            jev, "CREDENTIALS_FILE", Path(directory) / "jev-cli" / "credentials.json"
        ), patch("sys.stdin", io.StringIO("test-key\n")), patch.dict(os.environ, {}, clear=True):
            jev.set_api_key()
            self.assertEqual(jev.api_key(), "test-key")
            if os.name == "posix":
                self.assertEqual(jev.CREDENTIALS_FILE.stat().st_mode & 0o777, 0o600)
                self.assertEqual(jev.CREDENTIALS_FILE.parent.stat().st_mode & 0o777, 0o700)

    def test_set_api_key_prompts_without_echo_on_tty(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory, patch.object(
            jev, "CREDENTIALS_FILE", Path(directory) / "jev-cli" / "credentials.json"
        ), patch("sys.stdin.isatty", return_value=True), patch.object(
            jev.getpass, "getpass", return_value="prompted-key"
        ) as prompt, patch.dict(os.environ, {}, clear=True):
            jev.set_api_key()
            prompt.assert_called_once_with("TypeSafe API key: ")
            self.assertEqual(jev.api_key(), "prompted-key")

    def test_primary_values(self):
        result = {"answers": {"answer": {"noul": 0.9, "choice": "a", "score": 1.5}}}
        self.assertEqual(jev.primary_value(result, "noul"), 0.9)
        self.assertEqual(jev.primary_value(result, "choice"), "a")
        self.assertEqual(jev.primary_value(result, "score"), 1.5)

    def test_call_maps_authentication_failure_to_exit_code_3(self):
        error = urllib.error.HTTPError(
            "https://example.test", 401, "Unauthorized", Message(), io.BytesIO(b'{"error":"bad key"}')
        )
        with patch.object(jev, "api_key", return_value="test-key"), patch(
            "urllib.request.urlopen", side_effect=error
        ):
            with self.assertRaisesRegex(jev.CliError, "API HTTP 401") as raised:
                jev.call({"state": "test", "questions": {}}, "https://example.test")
        self.assertEqual(raised.exception.exit_code, 3)

    def test_call_maps_connection_failure_to_exit_code_4(self):
        with patch.object(jev, "api_key", return_value="test-key"), patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("offline")
        ):
            with self.assertRaisesRegex(jev.CliError, "API connection failed") as raised:
                jev.call({"state": "test", "questions": {}}, "https://example.test")
        self.assertEqual(raised.exception.exit_code, 4)

    def test_main_prints_only_primary_value(self):
        argv = ["jev", "noul", "--question", "Urgent?", "--state", "today", "--value"]
        with patch("sys.argv", argv), patch.object(
            jev, "call", return_value={"answers": {"answer": {"noul": 0.9}}}
        ), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.assertEqual(jev.main(), 0)
        self.assertEqual(stdout.getvalue(), "0.9\n")

    def test_main_emits_structured_error(self):
        with patch("sys.argv", ["jev", "run", "missing.json"]), patch(
            "sys.stderr", new_callable=io.StringIO
        ) as stderr:
            self.assertEqual(jev.main(), 2)
        self.assertEqual(json.loads(stderr.getvalue())["ok"], False)


if __name__ == "__main__":
    unittest.main()
