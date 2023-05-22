import os
import argparse
from nltk.tokenize import sent_tokenize

def tokenize_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    # 문장 토크나이징
    sentences = sent_tokenize(text)

    return sentences

def save_tokenized_sentences(sentences, output_filename):
    with open(output_filename, "w", encoding="utf-8") as f:
        for sentence in sentences:
            # 각 토큰을 하나의 문자열로 결합하여 한 줄로 만듦
            line = sentence.strip() + "\n"
            f.write(line)

def process_files(input_path, output_dir):
    if os.path.isfile(input_path):
        file_ext = os.path.splitext(input_path)[1]
        if file_ext != ".txt" and file_ext != ".md" :
            print(f"Skipping file {input_path} - Invalid file extension")
            return
        sentences = tokenize_file(input_path)
        output_filename = os.path.basename(input_path)
        output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + "_tokenized.txt")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        save_tokenized_sentences(sentences=sentences, output_filename=output_filename)
        return

    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        output_path = os.path.join(output_dir, os.path.basename(input_path))
        process_files(file_path, output_path)


def init():
    parser = argparse.ArgumentParser(description='Tokenize files in a directory or a single file.')
    parser.add_argument('source', metavar='SOURCE', type=str, help='path to the source directory or file')
    parser.add_argument('output', metavar='OUTPUT', type=str, default = "output/" ,help='path to the output directory')
    args = parser.parse_args()

    process_files(args.source, args.output)
    
if __name__ == "__main__":
    init()
