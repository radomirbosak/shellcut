from unittest import TestCase
from unittest.mock import patch

import shellcut


class TestShellcut(TestCase):

    @patch('shellcut.get_match')
    def test_check_shortcuts(self, mock_get_match):
        """
        Test that check_shortcuts returns the shell string for the first
        matching shortcut
        """
        mock_get_match.side_effect = [None, 'shell2', 'shell3']

        shortcuts = ['shortcut1', 'shortcut2', 'shortcut3']
        result = shellcut.check_shortcuts('input_data', shortcuts, label=None)

        self.assertEqual(result, 'shell2')

    def test_get_match_no_label(self):
        """
        Test that a query with specific label does not match a shortcut with no
        label
        """
        shortcut = {
            'match': '',
            'shell': '',
        }

        result = shellcut.get_match('input_data', shortcut, label='some_label')
        self.assertIsNone(result)

    def test_get_match_bad_label(self):
        """
        Test that a query with specific label does not match a shortcut with a
        different label
        """
        shortcut = {
            'match': '',
            'shell': '',
            'label': 'other_label'
        }

        result = shellcut.get_match('input_data', shortcut, label='some_label')
        self.assertIsNone(result)

    def test_get_match_parse_match(self):
        """
        Test that "format" matching works correctly
        """
        shortcut = {
            'match': 'My name is {} Potter',
            'shell': 'echo "Hello {}!"',
        }
        input_data = 'My name is Harry Potter'
        result = shellcut.get_match(input_data, shortcut)
        self.assertEqual(result, 'echo "Hello Harry!"')

    def test_get_match_parse_regex(self):
        """
        Test that "regex" matching works correctly
        """
        shortcut = {
            'regex': r'My name is (\w+) Potter',
            'shell': 'echo "Hello {}!"',
        }
        input_data = 'My name is Harry Potter'
        result = shellcut.get_match(input_data, shortcut)
        self.assertEqual(result, 'echo "Hello Harry!"')

    def test_get_match_parse_no_match(self):
        """
        Test that "format" matching works correctly
        """
        shortcut = {
            'match': r'My name is {} Potter',
            'shell': 'echo "Hello {}!"',
        }
        input_data = "My name isn't Harry Potter"
        result = shellcut.get_match(input_data, shortcut)
        self.assertIsNone(result)

    def test_get_match_regex_no_match(self):
        """
        Test that "format" matching works correctly
        """
        shortcut = {
            'match': r'My name is (\w+) Potter',
            'shell': 'echo "Hello {}!"',
        }
        input_data = 'My name is not Harry Potter'
        result = shellcut.get_match(input_data, shortcut)
        self.assertIsNone(result)
