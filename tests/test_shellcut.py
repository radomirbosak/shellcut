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

        self.assertEquals(result, 'shell2')
