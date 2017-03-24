import os
import textwrap
import tempfile

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

    def test_get_match_shell_found(self):
        """
        Test the pattern with correct shell is returned
        """
        shortcut = {
            'match': r'My name is {}dore',
            'dash': 'echo "{}"'
        }
        input_data = 'My name is Dumbledore'
        result = shellcut.get_match(input_data, shortcut, shell='dash')
        self.assertEqual(result, 'echo "Dumble"')

    def test_get_match_shell_notfound(self):
        """
        Test get_match returns None when appropriate shell script is not found
        """
        shortcut = {
            'match': r'My name is {}dore',
            'hash': 'echo "{}"'
        }
        input_data = 'My name is Dumbledore'
        result = shellcut.get_match(input_data, shortcut, shell='dash')
        self.assertIsNone(result)

    def test_get_match_shell_default(self):
        """
        Test get_match defaults to 'shell', when provided shell is not
        supported by the pattern
        """
        shortcut = {
            'match': r'My name is {}dore',
            'hash': 'echo "{}"',
            'shell': 'touch "{}"',
        }
        input_data = 'My name is Dumbledore'
        result = shellcut.get_match(input_data, shortcut, shell='dash')
        self.assertEqual(result, 'touch "Dumble"')

    def test_load_shortcuts_empty(self):
        """
        Test that an empty config dir loads no shortcuts
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            shortcuts = shellcut.load_shortcuts(tmpdir)
            self.assertEqual(shortcuts, [])

    def test_load_shortcuts_multiple_files(self):
        """
        Test that shortcuts are loaded correctly from multiple yaml files
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # create the first yaml file
            content = """\
            ---
            shortcuts:
            - name: harry
              attr: value
            - name: hagrid
              attr: value2
              label: giant
            """
            with open(os.path.join(tmpdir, 'file1.yaml'), 'w') as fd:
                fd.write(textwrap.dedent(content))

            # create the second yaml file
            content = """\
            ---
            shortcuts:
            - name: ron
              attr: weasley
            """
            with open(os.path.join(tmpdir, 'file2.yaml'), 'w') as fd:
                fd.write(textwrap.dedent(content))

            # create the third (not a yaml) file
            content = """\
            ---
            shortcuts:
            - name: hermione
              attr: granger
            """
            with open(os.path.join(tmpdir, 'file3.notayaml'), 'w') as fd:
                fd.write(textwrap.dedent(content))

            # expect only shortcuts from the first two files
            expected = [
                {'attr': 'value', 'name': 'harry'},
                {'attr': 'value2', 'label': 'giant', 'name': 'hagrid'},
                {'attr': 'weasley', 'name': 'ron'},
            ]

            shortcuts = shellcut.load_shortcuts(tmpdir)
            self.assertCountEqual(shortcuts, expected)

    @patch('shellcut.os.environ')
    def test_get_active_shell_fish(self, mock_environ):
        """
        Test that fish shell gets recognized
        """
        mock_environ.__getitem__.side_effect = ['/path/to/fish']

        shell = shellcut.get_active_shell()
        self.assertEqual(shell, 'fish')

    @patch('shellcut.os.environ')
    def test_get_active_shell_bash(self, mock_environ):
        """
        Test that bash shell gets recognized
        """
        mock_environ.__getitem__.side_effect = ['/i/am/complicated_bash']

        shell = shellcut.get_active_shell()
        self.assertEqual(shell, 'bash')

    @patch('shellcut.os.environ')
    def test_get_active_shell_unknown(self, mock_environ):
        """
        Test that an unknown shell returns None
        """
        mock_environ.__getitem__.side_effect = ['/some/weird/shell']

        shell = shellcut.get_active_shell()
        self.assertIsNone(shell)
