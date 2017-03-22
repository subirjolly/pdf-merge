import pytest

from mock import MagicMock, patch
from pdf.merge import main, validate_args, merge, append_page


@patch('pdf.merge.parse_args')
@patch('pdf.merge.merge')
def test_main(merge, parse_args):
    args = MagicMock()
    args.files = ['test1.pdf', 'test2.pdf']
    args.destination = 'out.pdf'
    parse_args.return_value = args

    assert 0 == main()


@patch('pdf.merge.parse_args')
def test_main_with_exception(parse_args):
    args = MagicMock()
    args.files = ['test1.pdf', 'test2.pdf']
    args.destination = 'out.pdf'
    parse_args.return_value = args

    assert 1 == main()


def test_validate_args():
    args = MagicMock()
    args.files = ['test1.pdf', 'test2.pdf']
    args.destination = 'out.pdf'

    validate_args(args)


def test_validate_args_raises():
    args = MagicMock()
    args.files = ['test1', 'test2.pdf']
    args.destination = 'out.pdf'

    with pytest.raises(Exception) as ei:
        validate_args(args)

    assert str(ei.value) == 'Invalid input'


@patch('pdf.merge.open'.format(__name__), create=True)
@patch('pyPdf.PdfFileWriter')
@patch('pyPdf.PdfFileReader')
def test_merge(pdf_reader, pdf_writer, opn):
    pdf_read = MagicMock()
    pdf_read.numPages = 1
    pdf_read.getPage = MagicMock(return_value='page')
    pdf_reader.return_value = pdf_read

    pdf_write = MagicMock()
    pdf_write.write = MagicMock()
    pdf_write.addPage = MagicMock()
    pdf_writer.return_value = pdf_write

    args = MagicMock()
    args.files = ['test1.pdf', 'test2.pdf']
    args.destination = 'out.pdf'
    merge(args)

    pdf_writer.assert_called_once_with()
    assert 1 == pdf_write.write.call_count
    assert 2 == pdf_write.addPage.call_count

    assert 2 == pdf_reader.call_count
    assert 2 == pdf_read.getPage.call_count

    assert 3 == opn.call_count
    assert ('test1.pdf', 'rb') == opn.call_args_list.pop(0)[0]
    assert ('test2.pdf', 'rb') == opn.call_args_list.pop(0)[0]
    assert ('out.pdf', 'wb') == opn.call_args_list.pop(0)[0]


@patch('pyPdf.PdfFileWriter')
@patch('pyPdf.PdfFileReader')
def test_merge_open_raises(pdf_reader, pdf_writer):
    pdf_read = MagicMock()
    pdf_read.numPages = 1
    pdf_read.getPage = MagicMock(return_value='page')
    pdf_reader.return_value = pdf_read

    pdf_write = MagicMock()
    pdf_write.write = MagicMock()
    pdf_write.addPage = MagicMock()
    pdf_writer.return_value = pdf_write

    args = MagicMock()
    args.files = ['test1.pdf', 'test2.pdf']
    args.destination = 'out.pdf'

    with pytest.raises(IOError):
        merge(args)

    pdf_writer.assert_called_once_with()
    assert 0 == pdf_reader.call_count


def test_append_page():
    in_file = MagicMock()
    in_file.numPages = 2
    in_file.getPage = MagicMock(return_value='page')
    out_file = MagicMock()
    out_file.addPage = MagicMock()

    append_page(in_file, out_file)

    assert 2 == in_file.getPage.call_count
    assert 2 == out_file.addPage.call_count
