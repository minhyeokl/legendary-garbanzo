import os
import re
import argparse
from openpyxl import Workbook

def save_eqs_to_excel(inline, block, filename):
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    wb = Workbook()
    # Create a new sheet named 'inline'
    sheet = wb.active
    sheet.title = 'inline'
    inline_count = 0
    for row in inline:
        inline_count += 1
        sheet.append([inline_count, row])
    # Create a new sheet named 'block'
    sheet = wb.create_sheet(title='block')
    block_count = 0
    for row in block:
        block_count += 1
        sheet.append([block_count, row])
    wb.save(filename)

def extract_all_latex_blocks(file_content):
    # Extract latexmath:[$...$] blocks
    inline_latex_blocks = re.findall(r'latexmath:\[\$(.*?)\$\]', file_content, re.DOTALL)
    inline_latex_blocks = [block.replace('{aligned}', '{align}') for block in inline_latex_blocks]
    
    # Extract [latexmath]++++{...}++++ blocks
    block_latex_blocks = re.findall(r'\[latexmath\]\n\+\+\+\+\n(.*?)\n\+\+\+\+\n', file_content, re.DOTALL)
    block_latex_blocks = [block.replace('{aligned}', '{align}') for block in block_latex_blocks]

    return inline_latex_blocks, block_latex_blocks

def process_files(input_path, output_dir):
    if os.path.isfile(input_path):
        file_ext = os.path.splitext(input_path)[1]
        if file_ext != ".asciidoc":
            print(f"Skipping file {input_path} - Invalid file extension")
            return

        output_filename = os.path.basename(input_path)
        output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + "_equations.xlsx")

        with open(input_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        inline, block = extract_all_latex_blocks(file_content)
        # skip if inline and block is empty
        if not inline and not block:
            return
        save_eqs_to_excel(inline, block, output_filename)
        return
    
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        output_path = os.path.join(output_dir, os.path.basename(input_path))
        process_files(file_path, output_path)


def init():
    input_path = os.getcwd()
    # make output directory under current working directory as 'equations'
    output_dir = os.path.join(os.getcwd(), "equations")
    
    parser = argparse.ArgumentParser(description='Extract latex equations from asciidoc files and save them to an excel file')
    parser.add_argument('-i', '--input', help='Input file or directory path', required=False)
    parser.add_argument('-o', '--output', help='Output directory path', required=False)
    args = parser.parse_args()
    if args.input:
        input_path = args.input
    if args.output:
        output_dir = args.output
    process_files(input_path, output_dir)
    
if __name__ == "__main__":
    init()