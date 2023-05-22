import os
import argparse
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook

def save_list_to_excel(lst, filename):
    wb = Workbook()
    sheet = wb.active
    for row in lst:
        sheet.append(row)
    wb.save(filename)

def mathml2latex(equation):
    xslt_file = os.path.join('mathconverter', 'xsl_yarosh', 'mmltex.xsl')
    dom = etree.fromstring(equation.encode('utf-8'))
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom

def parse_mathmls_from_html_file(input_file):
    # parse mathmls from html file with beautifulsoup
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    mathmls = soup.find_all('math')
    return mathmls

def convert_mathmls_to_latex(mathmls):
    # convert mathmls to latex
    latex_equations = []
    for mathml in mathmls:
        latex_equation = mathml2latex(str(mathml))
        latex_equations.append(latex_equation)
    return latex_equations
    

def process_files(input_path, output_dir):
    if os.path.isfile(input_path):
        result = []
        output_filename = os.path.basename(input_path)
        output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + "_equations.xlsx")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        equations = parse_mathmls_from_html_file(input_path)
        latex_equations = convert_mathmls_to_latex(equations)
        i = 0
        for equation in latex_equations:
            i += 1
            result.append([i, str(equation)])
        save_list_to_excel(result, output_filename)
        return

    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        output_path = os.path.join(output_dir, os.path.basename(input_path))
        process_files(file_path, output_path)

def init():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('source', metavar='SOURCE', type=str, help='path to the source')
    parser.add_argument('output', metavar='OUTPUT', type=str,
                        default = "output/", help='path to the output ')
    args = parser.parse_args()

    process_files(args.source, args.output)
    
if __name__ == "__main__":
    init()