import PyPDF2
import os
from argparse import ArgumentParser


def parse_args():
    """Get command line arguments"""
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input', action='store',
        required=True, dest='file', help='Input files.')
    parser.add_argument(
        '-p', '--pages', action='store',
        required=True, dest='pages', help='Pages.')
    parser.add_argument(
        '-o', '--output', required=True, dest='destination',
        help='Output file.')
    args = parser.parse_args()

    return args


def extract(args):
    pdf_in = open(args.file, 'rb')

    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()
    pages = set([int(page) for page in args.pages.split(',')])

    for pagenum in range(pdf_reader.numPages):
        if (pagenum + 1) in pages:
            page = pdf_reader.getPage(pagenum)
            pdf_writer.addPage(page)

    pdf_out = open(args.destination, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    print('Extracted into: {0}'.format(args.destination))


def validate_args(args):
    if args.file[-4:].lower() != '.pdf':
        raise Exception('Invalid input')


def main():
    args = parse_args()
    try:
        validate_args(args)
        extract(args)
    except Exception as e:
        print('Error: {0}'.format(str(e)))
        return 1

    return 0
