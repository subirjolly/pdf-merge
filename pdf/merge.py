from PyPDF2 import PdfFileMerger
import os
from argparse import ArgumentParser


def parse_args():
    """Get command line arguments"""
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input', action='append',
        required=True, dest='files', help='Input files.')
    parser.add_argument(
        '-o', '--output', required=True, dest='destination',
        help='Output file.')
    args = parser.parse_args()

    return args


def append_page(in_file, out_file):
    for page_num in range(in_file.numPages):
        out_file.addPage(in_file.getPage(page_num))


def merge(args):
    merger = PdfFileMerger(strict=False)
    for f in args.files:
        merger.append(f)

    merger.write(open(args.destination, 'wb'))
    merger.close()
    print('Merged into: {0}'.format(args.destination))


def validate_args(args):
    for f in args.files:
        if f[-4:].lower() != '.pdf':
            raise Exception('Invalid input')


def main():
    args = parse_args()
    try:
        validate_args(args)
        merge(args)
    except Exception as e:
        print('Error: {0}'.format(str(e)))
        return 1

    return 0
