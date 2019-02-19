# 100K_summary_findings_pdf v1.0

This script downloads the summary of findings html for a 100k case, performs some minor reformatting and converts it to a pdf.

Requirements:
* Python 3.6
* BeautifulSoup
* pdfkit
* Access to CIPAPI
* JellyPy (in PYTHONPATH)

On `SV-TE-GENAPP01` activate the `jellypy_py3` conda environment so that above requirements are met:

```
source activate jellypy_py3
```

Then run the script, supplying the interpretation request ID, version and output file path for the PDF.

```
usage: download_summary_findings.py [-h] --ir_id IR_ID --ir_version IR_VERSION
                                    -o OUTPUT_FILE

Downloads summary of findings for given interpretation request

optional arguments:
  -h, --help            show this help message and exit
  --ir_id IR_ID         Interpretation request ID
  --ir_version IR_VERSION
                        Interpretation request version
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output PDF
```