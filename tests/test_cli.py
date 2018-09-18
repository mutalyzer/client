"""Tests for the mutalyzer-client CLI."""
from io import StringIO

from mutalyzer_client.cli import hgvs_to_db, vcf_to_db, vcf_to_hgvs

from shared import md5_check


class TestCLI(object):
    def setup(self):
        self._output = StringIO()
        self._build = 'GRCh37'

    def _md5_check(self, md5sum):
        return md5_check(self._output.getvalue(), md5sum)

    def test_hgvs_to_db(self):
        hgvs_to_db(self._build, open('data/sample.hgvs'), self._output)
        assert self._md5_check('5580158f1c21262ba8e7330553e8b3bf')

    def test_vcf_to_db(self):
        vcf_to_db(self._build, open('data/sample.vcf'), self._output)
        assert self._md5_check('5580158f1c21262ba8e7330553e8b3bf')

    def test_vcf_to_hgvs(self):
        vcf_to_hgvs(self._build, open('data/sample.vcf'), self._output)
        assert self._md5_check('6ffc5de8b730ef1436d98a779101e205')
