from argparse import ArgumentParser, FileType, RawDescriptionHelpFormatter

from vcf import Reader

from . import doc_split, usage, version
from .mutalyzer_client import build, Mutalyzer


def vcf_to_hgvs(build_name, input_handle, output_handle):
    """
    Convert all variants in a VCF file to HGVS.

    :arg str build_name: Build name.
    :arg stream input_handle: Open readable handle to a VCF file.
    :arg stream output_handle: Open writeable handle to a text file.
    """
    mutalyzer = Mutalyzer(build_name)

    for record in Reader(input_handle):
        for alt in record.ALT:
            output_handle.write('{}\n'.format(mutalyzer.vcf_to_hgvs(
                record.CHROM, record.POS, record.REF, alt)))


def vcf_to_details(build_name, input_handle, output_handle):
    """
    Convert all variants in a VCF file to details.

    :arg str build_name: Build name.
    :arg stream input_handle: Open readable handle to a VCF file.
    :arg stream output_handle: Open writeable handle to a text file.
    """
    mutalyzer = Mutalyzer(build_name)

    for record in Reader(input_handle):
        for alt in record.ALT:
            output_handle.write('{}\n'.format('\t'.join(mutalyzer.check_genomic(
                record.CHROM, record.POS, record.REF, alt))))


def hgvs_to_details(build_name, input_handle, output_handle):
    """
    Convert all HGVS variants in a text file to details.

    :arg str build_name: Build name.
    :arg stream input_handle: Open readable handle to a text file.
    :arg stream output_handle: Open writeable handle to a text file.
    """
    mutalyzer = Mutalyzer(build_name)

    for record in input_handle.readlines():
        output_handle.write('{}\n'.format('\t'.join(mutalyzer.hgvs_to_vcf(
            record))))


def main():
    """Main entry point."""
    build_parser = ArgumentParser(add_help=False)
    build_parser.add_argument(
        'build_name', metavar='BUILD', type=str, choices=build.keys(),
        help='build name')

    input_parser = ArgumentParser(add_help=False)
    input_parser.add_argument(
        'input_handle', metavar='INPUT', type=FileType('r'), help='input file')

    output_parser = ArgumentParser(add_help=False)
    output_parser.add_argument(
        'output_handle', metavar='OUTPUT', type=FileType('w'),
        help='output file')

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter, description=usage[0],
        epilog=usage[1])
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    subparser = subparsers.add_parser(
        'vcf_to_hgvs', parents=[build_parser, input_parser, output_parser],
        description=doc_split(vcf_to_hgvs))
    subparser.set_defaults(func=vcf_to_hgvs)

    subparser = subparsers.add_parser(
        'vcf_to_details', parents=[build_parser, input_parser, output_parser],
        description=doc_split(vcf_to_details))
    subparser.set_defaults(func=vcf_to_details)

    subparser = subparsers.add_parser(
        'hgvs_to_details', parents=[build_parser, input_parser, output_parser],
        description=doc_split(hgvs_to_details))
    subparser.set_defaults(func=hgvs_to_details)

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    try:
        args.func(
            **{k: v for k, v in vars(args).items()
            if k not in ('func', 'subcommand')})
    except (ValueError, IOError) as error:
        parser.error(error)


if __name__ == '__main__':
    main()
