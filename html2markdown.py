import os
import argparse
import markdownify


def convert_html_to_markdown(input_file, output_dir):
    output_filename = os.path.basename(input_file)
    output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + ".md")
    
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    md_content = markdownify.markdownify(html_content)
    with open(output_filename, "w") as markdown_file:
        markdown_file.write(md_content)

def process_files(input_path, output_dir):
    if os.path.isfile(input_path):
        file_ext = os.path.splitext(input_path)[1]
        if file_ext != ".html":
            print(f"Skipping file {input_path} - Invalid file extension")
            return
        
        output_filename = os.path.basename(input_path)
        output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + "_tokenized.txt")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        convert_html_to_markdown(input_path, output_dir)
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