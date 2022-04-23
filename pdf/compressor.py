from PyPDF2 import PdfFileMerger
import os
from argparse import ArgumentParser
import os
import sys
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet


def parse_args():
    """Get command line arguments"""
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input', action='store',
        required=True, dest='source', help='Input file.')
    parser.add_argument(
        '-o', '--output', required=True, dest='destination',
        help='Output file.')
    args = parser.parse_args()

    return args


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor

    return f"{b:.2f}Y{suffix}"

def compress(args):
    compress_file(args.source, args.destination)

def compress_file(input_file: str, output_file: str):
    """Compress PDF file"""
    if not output_file:
        output_file = input_file
    initial_size = os.path.getsize(input_file)
    try:
        # Initialize the library
        PDFNet.Initialize()
        doc = PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(output_file, SDFDoc.e_linearized)
        doc.Close()
    except Exception as e:
        print("Error compress_file=", e)
        doc.Close()
        return False
    compressed_size = os.path.getsize(output_file)
    ratio = 1 - (compressed_size / initial_size)
    summary = {
        "Input File": input_file, "Initial Size": get_size_format(initial_size),
        "Output File": output_file, f"Compressed Size": get_size_format(compressed_size),
        "Compression Ratio": "{0:.3%}.".format(ratio)
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return True

def validate_args(args):
    if args.source[-4:].lower() != '.pdf':
        raise Exception('Invalid input')

def main():
    args = parse_args()
    try:
        validate_args(args)
        compress(args)
    except Exception as e:
        print('Error: {0}'.format(str(e)))
        return 1

    return 0
