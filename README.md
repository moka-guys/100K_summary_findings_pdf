# 100K_summary_findings_pdf v1.0

This script downloads the summary of findings html for a 100k case, performs some minor reformatting and converts it to a pdf.

Requirements:
* Python 3.6
* BeautifulSoup
* pdfkit
* wkhtmlpdfkit
* Access to CIPAPI
* JellyPy

On `SV-TE-GENAPP01` activate the `jellypy_py3` conda environment so that above requirements are met:

```
source activate jellypy_py3
```

Rename `example_summary_findings_config.py` to `summary_findings_config.py` and update config as required.

Then run the script, supplying the interpretation request ID, version, output file path and (optional) header for the PDF.

```
usage: summary_findings.py [-h] --ir_id IR_ID --ir_version IR_VERSION -o
                           OUTPUT_FILE [--header HEADER]

Downloads summary of findings for given interpretation request

optional arguments:
  -h, --help            show this help message and exit
  --ir_id IR_ID         Interpretation request ID
  --ir_version IR_VERSION
                        Interpretation request version
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output PDF
  --header HEADER       Text for header of report

```