from requests import Session


build = {
    'GRCh37': {
        # https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.13/
        'chr1': 'NC_000001.10',
        'chr2': 'NC_000002.11',
        'chr3': 'NC_000003.11',
        'chr4': 'NC_000004.11',
        'chr5': 'NC_000005.9',
        'chr6': 'NC_000006.11',
        'chr7': 'NC_000007.13',
        'chr8': 'NC_000008.10',
        'chr9': 'NC_000009.11',
        'chr10': 'NC_000010.10',
        'chr11': 'NC_000011.9',
        'chr12': 'NC_000012.11',
        'chr13': 'NC_000013.10',
        'chr14': 'NC_000014.8',
        'chr15': 'NC_000015.9',
        'chr16': 'NC_000016.9',
        'chr17': 'NC_000017.10',
        'chr18': 'NC_000018.9',
        'chr19': 'NC_000019.9',
        'chr20': 'NC_000020.10',
        'chr21': 'NC_000021.8',
        'chr22': 'NC_000022.10',
        'chrX': 'NC_000023.10',
        'chrY': 'NC_000024.9'},
    'GRCh38': {
        # https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.38
        'chr1': 'NC_000001.11',
        'chr2': 'NC_000002.12',
        'chr3': 'NC_000003.12',
        'chr4': 'NC_000004.12',
        'chr5': 'NC_000005.10',
        'chr6': 'NC_000006.12',
        'chr7': 'NC_000007.14',
        'chr8': 'NC_000008.11',
        'chr9': 'NC_000009.12',
        'chr10':'NC_000010.11',
        'chr11':'NC_000011.10',
        'chr12':'NC_000012.12',
        'chr13':'NC_000013.11',
        'chr14':'NC_000014.9',
        'chr15':'NC_000015.10',
        'chr16':'NC_000016.10',
        'chr17':'NC_000017.11',
        'chr18':'NC_000018.10',
        'chr19':'NC_000019.10',
        'chr20':'NC_000020.11',
        'chr21':'NC_000021.9',
        'chr22':'NC_000022.11',
        'chrX': 'NC_000023.11',
        'chrY': 'NC_000024.10'}}


class Mutalyzer(object):
    def __init__(self, build_name):
        self._chromosome_to_accession = build[build_name]
        self._accession_to_chromosome = dict(
            map(lambda x: x[::-1], self._chromosome_to_accession.items()))
        self._session = Session()

    def _request(self, **kwargs):
        return self._session.get(
            'https://mutalyzer.nl/json/runMutalyzerLight',
            params={**kwargs, 'extras.varDetails': True}).json()

    def _check_vcf_genomic(self, chromosome, start, ref, alt):
        return self._request(variant='{}:g.{}_{}delins{}'.format(
            self._chromosome_to_accession[chromosome],
            start, start + len(ref) - 1, alt))

    def _details_to_db(self, details):
        return (
            self._accession_to_chromosome[details['reference_file']],
            details['start'], details['ref'], details['alt'])

    def hgvs_to_db(self, variant):
        return self._details_to_db(
            self._request(variant=variant)['varDetails'])

    def vcf_to_db(self, chromosome, start, ref, alt):
        return self._details_to_db(
            self._check_vcf_genomic(chromosome, start, ref, alt)['varDetails'])

    def vcf_to_hgvs(self, chromosome, start, ref, alt):
        return self._check_vcf_genomic(
            chromosome, start, ref, alt)['genomicDescription']
