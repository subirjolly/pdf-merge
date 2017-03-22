# pdf-merge
PDF Merge Utility

## Development
```
virtualenv .venv
# OR
pyvenv .venv

. .venv/bin/activate
pip install -r development.txt
python setup.py develop
```

## Running Tests
```
# After running the Development steps, run:
py.test
```

## Style Check
```
# After running the Development steps, run:
flake8
```

## Usage
```
merge_pdf -i pdf1.pdf -i pdf2.pdf ... -i pdfN.pdf -o out.pdf

# For help
merge_pdf -h
```
