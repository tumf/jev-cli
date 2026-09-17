import io
import json
import os
import unittest
from unittest.mock import patch

import jev_cli as jev


class JevTest(unittest.TestCase):
    def test_choice_request(self):
        args = jev.parser().parse_args(
            ["choice", "Route?", "broken", "-o", "tech=Bug", "-o", "sales=Purchase"]
        )
        payload, kind = jev.request_for(args)
        self.assertEqual(kind, "choice")
        self.assertEqual(payload["questions"]["answer"]["criteria"], {"tech": "Bug", "sales": "Purchase"})

    def test_json_state_from_stdin(self):
        args = jev.parser().parse_args(["noul", "Urgent?", "-", "--json-state"])
        with patch("sys.stdin", io.StringIO('{"message":"today"}')):
            payload, _ = jev.request_for(args)
        self.assertEqual(payload["state"], {"message": "today"})

    def test_api_key_prefers_environment(self):
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "test-key"}):
            self.assertEqual(jev.api_key(), "test-key")

    def test_primary_values(self):
        result = {"answers": {"answer": {"noul": 0.9, "choice": "a", "score": 1.5}}}
        self.assertEqual(jev.primary_value(result, "noul"), 0.9)
        self.assertEqual(jev.primary_value(result, "choice"), "a")
        self.assertEqual(jev.primary_value(result, "score"), 1.5)


if __name__ == "__main__":
    unittest.main()
