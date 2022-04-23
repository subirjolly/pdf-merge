import PyPDF2
import os
from argparse import ArgumentParser


def parse_args():
    """Get command line arguments"""
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input', action='store',
        required=True, dest='file', help='Input file.')
    parser.add_argument(
        '-d', '--degree', action='store',
        required=True, dest='degree', help='Rotation degree. Default is 90.',
        type=int, default=90)
    parser.add_argument(
        '-o', '--output', required=True, dest='destination',
        help='Output file.')
    args = parser.parse_args()

    return args


def rotate(args):
    pdf_in = open(args.file, 'rb')

    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(args.degree)
        pdf_writer.addPage(page)

    pdf_out = open(args.destination, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    print('Merged into: {0}'.format(args.destination))


def validate_args(args):
    if args.degree < 0 or args.degree > 360:
        raise Exception('Invalid degree')

    if args.file[-4:].lower() != '.pdf':
        raise Exception('Invalid input')


def main():
    args = parse_args()
    try:
        validate_args(args)
        rotate(args)
    except Exception as e:
        print('Error: {0}'.format(str(e)))
        return 1

    return 0
