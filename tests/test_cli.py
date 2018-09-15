"""Tests for the mutalyzer-client CLI."""
import StringIO

from mutalyzer_client import mutalyzer_client

from shared import md5_check


class TestCLI(object):
    def setup(self):
        self._output = StringIO.StringIO()

    def _md5_check(self, md5sum):
        return md5_check(self._output.getvalue(), md5sum)

    def test_1(self):
        pass
