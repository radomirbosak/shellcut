import os
import textwrap
import tempfile

from unittest import TestCase
from unittest.mock import patch

from shellcut import main


class TestShellcut(TestCase):

    @patch('shellcut.main.get_match')
    def test_check_shortcuts(self, mock_get_match):
        """
        Test that check_shortcuts returns the shell string for the first
        matching shortcut
        """
        mock_get_match.side_effect = [None, 'shell2', 'shell3']

        shortcuts = ['shortcut1', 'shortcut2', 'shortcut3']
        result = main.check_shortcuts('input_data', shortcuts, label=None)

        expected_result = [('shortcut2', 'shell2'), ('shortcut3', 'shell3')]
        self.assertEqual(result, expected_result)

    def test_label_matches_no_cli_label(self):
        """
        Test when label is not supplied it matches anything
        """
        res = main.label_matches(None, 'l1')
        self.assertTrue(res)

    def test_label_matches_success(self):
        """
        Test success if CLI label matches pattern label
        """
        res = main.label_matches('l1', 'l1')
        self.assertTrue(res)

    def test_label_matches_fail(self):
        """
        Test for failure if CLI label doesn't match pattern label
        """
        res = main.label_matches('l1', 'l2')
        self.assertFalse(res)

    def test_label_matches_multi_success(self):
        """
        Test for success if CLI label is in list of pattern labels
        """
        res = main.label_matches('l1', ['l1', 'l2'])
        self.assertTrue(res)

    def test_label_matches_no_pattern_label(self):
        """
        Test case when CLI label is supplied, but pattern has none
        """
        res = main.label_matches('l1', None)
        self.assertFalse(res)

    def test_label_matches_multi_fail(self):
        """
        Test case when CLI label does not match list of pattern labels
        """
        res = main.label_matches('l1', ['l2', 'l3'])
        self.assertFalse(res)

    def test_get_match_no_label(self):
        """
        Test that a query with specific label does not match a shortcut with no
        label
        """
        shortcut = {
            'match': '',
            'shell': '',
        }

        result = main.get_match('input_data', shortcut, label='some_label')
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

        result = main.get_match('input_data', shortcut, label='some_label')
        self.assertIsNone(result)

    def test_get_match_multilabel(self):
        """
        Test that a pattern is picked when given label is in pattern's label
        list
        """
        shortcut = {
            'match': 'input_data',
            'shell': 'command',
            'label': ['l1', 'l2']
        }

        result = main.get_match('input_data', shortcut, label='l2')
        self.assertEqual(result, 'command')

    def test_get_match_multilabel_fail(self):
        """
        Test that a pattern is not picked if given label is not in the
        pattern's label list
        """
        shortcut = {
            'match': 'input_data',
            'shell': 'command',
            'label': ['l1', 'l2']
        }

        result = main.get_match('input_data', shortcut, label='l3')
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
        result = main.get_match(input_data, shortcut)
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
        result = main.get_match(input_data, shortcut)
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
        result = main.get_match(input_data, shortcut)
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
        result = main.get_match(input_data, shortcut)
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
        result = main.get_match(input_data, shortcut, shell='dash')
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
        result = main.get_match(input_data, shortcut, shell='dash')
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
        result = main.get_match(input_data, shortcut, shell='dash')
        self.assertEqual(result, 'touch "Dumble"')

    def test_get_match_multiple_match(self):
        """
        Test one of multiple 'parse' patterns matches
        """
        shortcut = {
            'match': ['m1', 'm2'],
            'shell': 'result'
        }
        input_data = 'm1'
        result = main.get_match(input_data, shortcut)
        self.assertEqual(result, 'result')

    def test_get_match_multiple_match_fail(self):
        """
        Test one of multiple 'parse' patterns matches
        """
        shortcut = {
            'match': ['m1', 'm2'],
            'shell': 'result'
        }
        input_data = 'm3'
        result = main.get_match(input_data, shortcut)
        self.assertIsNone(result)

    def test_get_match_multiple_regex(self):
        """
        Test one of multiple 'regex' patterns matches
        """
        shortcut = {
            'regex': ['m1', 'm2'],
            'shell': 'result'
        }
        input_data = 'm1'
        result = main.get_match(input_data, shortcut)
        self.assertEqual(result, 'result')

    def test_get_match_multiple_regex_fail(self):
        """
        Test one of multiple 'regex' patterns matches
        """
        shortcut = {
            'regex': ['m1', 'm2'],
            'shell': 'result'
        }
        input_data = 'm3'
        result = main.get_match(input_data, shortcut)
        self.assertIsNone(result)

    def test_load_shortcuts_empty(self):
        """
        Test that an empty config dir loads no shortcuts
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            shortcuts = main.load_shortcuts([tmpdir])
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

            shortcuts = main.load_shortcuts([tmpdir])
            self.assertCountEqual(shortcuts, expected)

    def test_load_shortcuts_multiple_dirs(self):
        """
        Test that shortcuts are loaded correctly from multiple yaml files
        """
        tmpdir1 = tempfile.TemporaryDirectory()
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
        with open(os.path.join(tmpdir1.name, 'file1.yaml'), 'w') as fd:
            fd.write(textwrap.dedent(content))

        tmpdir2 = tempfile.TemporaryDirectory()
        # create the second yaml file
        content = """\
        ---
        shortcuts:
        - name: ron
          attr: weasley
        """
        with open(os.path.join(tmpdir2.name, 'file2.yaml'), 'w') as fd:
            fd.write(textwrap.dedent(content))

        # expect shortcuts from both dirs
        expected = [
            {'attr': 'value', 'name': 'harry'},
            {'attr': 'value2', 'label': 'giant', 'name': 'hagrid'},
            {'attr': 'weasley', 'name': 'ron'},
        ]

        shortcuts = main.load_shortcuts([tmpdir1.name, tmpdir2.name])
        self.assertCountEqual(shortcuts, expected)

        tmpdir1.cleanup()
        tmpdir2.cleanup()

    @patch('shellcut.main.os.environ')
    def test_get_active_shell_fish(self, mock_environ):
        """
        Test that fish shell gets recognized
        """
        mock_environ.__getitem__.side_effect = ['/path/to/fish']

        shell = main.get_active_shell()
        self.assertEqual(shell, 'fish')

    @patch('shellcut.main.os.environ')
    def test_get_active_shell_bash(self, mock_environ):
        """
        Test that bash shell gets recognized
        """
        mock_environ.__getitem__.side_effect = ['/i/am/complicated_bash']

        shell = main.get_active_shell()
        self.assertEqual(shell, 'bash')

    @patch('shellcut.main.os.environ')
    def test_get_active_shell_unknown(self, mock_environ):
        """
        Test that an unknown shell returns None
        """
        mock_environ.__getitem__.side_effect = ['/some/weird/shell']

        shell = main.get_active_shell()
        self.assertIsNone(shell)

    @patch('shellcut.main.os.environ')
    def test_get_config_dirs_envset(self, mock_environ):
        """
        Test SHELLCUT_CONFIG environment variable is read
        """
        mock_environ.__contains__ = lambda self, x: x == 'SHELLCUT_CONFIG'
        mock_environ.__getitem__.return_value = '/path/to/blab'
        config_dir = main.get_config_dirs()

        self.assertIn('/path/to/blab', config_dir)

    @patch('shellcut.main.os.environ')
    @patch('shellcut.main.os.path.join')
    def test_get_config_dirs_xdg(self, mock_join, mock_environ):
        """
        Test XDG_CONFIG_HOME variable is used if SHELLCUT_CONFIG is not
        specified
        """
        mock_environ.__contains__.return_value = False
        mock_join.return_value = '/path/to/xdg/config'
        config_dir = main.get_config_dirs()

        self.assertIn('/path/to/xdg/config', config_dir)

    @patch('shellcut.main.os.environ')
    @patch('shellcut.main.os.path.dirname')
    def test_get_config_dirs_module(self, mock_dirname, mock_environ):
        """
        Test XDG_CONFIG_HOME variable is used if SHELLCUT_CONFIG is not
        specified
        """
        mock_environ.__contains__.return_value = False
        mock_dirname.return_value = '/path/to/module_dir'
        config_dir = main.get_config_dirs()

        self.assertIn('/path/to/module_dir/config', config_dir)

    @patch('shellcut.main.get_input')
    def test_choose_match_single(self, mock_input):
        """
        Test correct option is chose in there is only one option
        """
        mock_input.return_value = 1
        matches = [({'name': 'a'}, 'm')]
        command = main.choose_match(matches)
        self.assertEqual(command, 'm')

    @patch('shellcut.main.get_input')
    def test_choose_match_multiple(self, mock_input):
        """
        Test choosing from multiple options
        """
        mock_input.return_value = 2
        matches = [({'name': 'a'}, 'm'), ({'name': 'b'}, 'm2')]
        command = main.choose_match(matches)
        self.assertEqual(command, 'm2')

    @patch('shellcut.main.get_input')
    def test_choose_match_invalid(self, mock_input):
        """
        Test invalid option chosen by user
        """
        mock_input.return_value = 3
        matches = [({'name': 'a'}, 'm'), ({'name': 'b'}, 'm2')]

        with self.assertRaises(ValueError):
            main.choose_match(matches)

        mock_input.return_value = 'abc'
        with self.assertRaises(ValueError):
            main.choose_match(matches)
