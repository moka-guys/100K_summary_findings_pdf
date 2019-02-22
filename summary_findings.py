"""
v1.0 - AB 2019/02/18
Requirements:
    Python 3.6
    BeautifulSoup
    pdfkit
    Access to CIPAPI
    JellyPy (in PYTHONPATH)

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
"""

import sys
import argparse
from bs4 import BeautifulSoup
import pdfkit
from pyCIPAPI.auth import AuthenticatedCIPAPISession
from pyCIPAPI.interpretation_requests import get_interpretation_request_list

def process_arguments():
    """
    Uses argparse module to define and handle command line input arguments and help menu
    """
    # Create ArgumentParser object. Description message will be displayed as part of help message if script is run with -h flag
    parser = argparse.ArgumentParser(description='Downloads summary of findings for given interpretation request')
    # Define the arguments that will be taken.
    parser.add_argument('--ir_id', required=True, help='Interpretation request ID')
    parser.add_argument('--ir_version', required=True, help='Interpretation request version')
    parser.add_argument('-o', '--output_file', required=True, help='Output PDF')
    # Return the arguments
    return parser.parse_args()

class SummaryFindings(object):
    def __init__(self):
        self.html = None
        self.soup = None

    def download_sum_findings(self, ir_id, ir_ver):
        """
        Downloads summary of findings using JellyPy
        """
        ir_details = get_interpretation_request_list(interpretation_request_id=ir_id, version=ir_ver)
        # Check only one record is returned
        if len(ir_details) == 1:
            # Check that there's only one summary of findings report
            if len(ir_details[0]["clinical_reports"]) == 1:
                # Download the report from CIP API
                session = AuthenticatedCIPAPISession()
                response = session.get(ir_details[0]["clinical_reports"][0]['url'])
                # Check response code is 200
                if response.status_code == 200:
                    # Store the returned html for use by other methods
                    self.html = response.text
                else: 
                    sys.exit(f'response code {response.status_code}')
            else:
                sys.exit(f'number of clinical reports {len(ir_details[0]["clinical_reports"])}')
        else:
            sys.exit(f'number of interpretation requests {len(ir_details)}')

    def expand_coverage(self):
        '''Expand the coverage section'''
        # find the coverage div and delete so coverage seciton no longer needs to be clicked to be visible
        for section in self.soup.find_all('div', id = "coverage"):
            del(section['hidden'])
        # find the section header and remove text/hyperlink properties
        for section in self.soup.find_all('a'):
            # find the coverage section
            if "Coverage Metrics" in section.get_text():
                # remove the extra styles no longer needed
                del(section['onclick'])
                del(section['style'])
        # remove the 'Click to collapse/expand' text
        for section in self.soup.find_all('small'):
            if "Click to collapse/expand" in section.get_text():
                section.decompose()

    def stop_annex_tables_splitting_over_page(self):
        '''This script takes the referenced databases and software version tables and stops these being broken over pages'''
        # find all tables
        for table in self.soup.find_all('table'):
            #find the table head
            for head in table.find_all('thead'):
                # find each column in the header
                for col in head.find_all('th'):
                    # if there is a column called name 
                    if col.get_text() == "Name":
                        # prevent page breaks
                        table['style'] = " page-break-inside: avoid !important"

    def fix_logo(self):
        # find the img tag where class == logo (should only be one)
        for img in self.soup.find_all('img', {'class':"logo"}):
            # Need to ensure the image doesn't shrink
            img['style'] = "height:85px;"

    def stop_overheader_line_split(self):
        # Find div containing top header with participant ID and generated on date
        for div in self.soup.find_all('div', {'class':"over-header content-div"}):
            # prevent 'Generated on: ...' text wrapping over two lines
            div['style'] = "white-space:nowrap;"

    def remove_dropshadow(self):
        # Find report div
        for div in self.soup.find_all('div', id = "report"):
            # prevent 'Generated on: ...' text wrapping over two lines
            div['style'] = "box-shadow:none;"
 
    def fix_formatting(self):
        # Read html into a beautiful soup object
        self.soup = BeautifulSoup(self.html, "html.parser")
        # Coverage section is collapsed by default, we want it expanded
        self.expand_coverage()
        # Information can be lost when a table cell is split over pages, so fix this
        self.stop_annex_tables_splitting_over_page()
        # Logo and banner shrink, so need to fix this
        self.fix_logo()
        # Top line with 'Generated on:...' date splits over two lines, stop this happening
        self.stop_overheader_line_split()
        # Get rid of the dropshadow border
        self.remove_dropshadow()
        # Turn back into a string    
        self.html = str(self.soup)

    def write_pdf(self, pdfreport_path, wkhtmltopdf):
        '''
        Given the name of a html file, look in the folder containing these files (specified in config) and convert to a pdf, saving at the specified location.
        Uses pdfkit and wkthmltopdf
        Adds a footer to pages stating page number and date stamp.
        '''
        # add the path to wkhtmltopdf to the pdfkit config settings
        pdfkitconfig = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
        # create dictionary of options that will be passed to the wkhtmltopdf command (see https://wkhtmltopdf.org/usage/wkhtmltopdf.txt for list of options)
        options = {
            'quiet': ''
            }
        # create the pdf using template.render to populate variables from dictionary created in read_geneworks
        pdfkit.from_string(self.html, pdfreport_path, options=options, configuration=pdfkitconfig)

def main():
    # Get command line arguments
    args = process_arguments()
    # Download summary of findings
    sof = SummaryFindings()
    sof.download_sum_findings(ir_id=args.ir_id, ir_ver=args.ir_version)
    # Write out to a pdf
    sof.fix_formatting()
    sof.write_pdf(pdfreport_path=args.output_file, wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

if __name__ == '__main__':
    main()