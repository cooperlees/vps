#!/usr/bin/env python3

import unittest

from click.testing import CliRunner

from vps import main


class TestVps(unittest.TestCase):
    def test_help_output(self):
        runner = CliRunner()
        result = runner.invoke(main.main, ["--help"])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
