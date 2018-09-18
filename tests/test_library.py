"""Tests for the mutalyzer-client library."""
from mutalyzer_client import Mutalyzer


class TestLibrary(object):
    def setup(self):
        self._mutalyzer = Mutalyzer('GRCh37')

    def test_hgvs_to_db_subst(self):
        assert (
            self._mutalyzer.hgvs_to_db('NC_000001.10:g.100000C>T') ==
            ('chr1', 100000, 'C', 'T'))

    def test_hgvs_to_db_del(self):
        assert (
            self._mutalyzer.hgvs_to_db('NC_000001.10:g.100001del') ==
            ('chr1', 100001, 'A', '.'))

    def test_hgvs_to_db_ins(self):
        assert (
            self._mutalyzer.hgvs_to_db('NC_000001.10:g.100000_100001insT') ==
            ('chr1', 100000, '.', 'T'))

    def test_vcf_to_db_subst(self):
        assert (
            self._mutalyzer.vcf_to_db('chr1', 100000, 'C', 'T') ==
            ('chr1', 100000, 'C', 'T'))

    def test_vcf_to_db_del(self):
        assert (
            self._mutalyzer.vcf_to_db('chr1', 100000, 'CA', 'C') ==
            ('chr1', 100001, 'A', '.'))

    def test_vcf_to_db_ins(self):
        assert (
            self._mutalyzer.vcf_to_db('chr1', 100000, 'C', 'CT') ==
            ('chr1', 100000, '.', 'T'))

    def test_vcf_to_hgvs_subst(self):
        assert (
            self._mutalyzer.vcf_to_hgvs('chr1', 100000, 'C', 'T') ==
            'NC_000001.10:g.100000C>T')

    def test_vcf_to_hgvs_del(self):
        assert (
            self._mutalyzer.vcf_to_hgvs('chr1', 100000, 'CA', 'C') ==
            'NC_000001.10:g.100001del')

    def test_vcf_to_hgvs_ins(self):
        assert (
            self._mutalyzer.vcf_to_hgvs('chr1', 100000, 'C', 'CT') ==
            'NC_000001.10:g.100000_100001insT')
