import os
import tempfile
import unittest
from unittest.mock import patch

import main


class AssistantTests(unittest.TestCase):
    def test_env_loader(self):
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('MODEL=test-model\nAPI_KEY=sample\n# comment\n')
            path = f.name
        try:
            with patch.dict(os.environ, {}, clear=True):
                main.load_env(path)
                self.assertEqual(os.environ['MODEL'], 'test-model')
                self.assertEqual(os.environ['API_KEY'], 'sample')
        finally:
            os.unlink(path)

    def test_history_disabled_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(main.history_enabled())

    def test_history_enabled_flag(self):
        with patch.dict(os.environ, {'SAVE_HISTORY': 'true'}):
            self.assertTrue(main.history_enabled())

    def test_history_load_missing_file(self):
        system = {'role': 'system', 'content': 'test'}
        with patch.dict(os.environ, {'SAVE_HISTORY': 'false'}):
            self.assertEqual(main.load_history(system), [system])

    def test_history_reset_behavior_independent(self):
        system = {'role': 'system', 'content': 'test'}
        with patch.dict(os.environ, {'SAVE_HISTORY': 'false'}):
            messages = main.load_history(system)
            self.assertEqual(messages, [system])


if __name__ == '__main__':
    unittest.main()
