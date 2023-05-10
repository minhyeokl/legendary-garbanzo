import os
import argparse
from nltk.tokenize import sent_tokenize

def tokenize_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    # 문장을 토크나이징
    sentences = sent_tokenize(text)

    return sentences

def save_tokenized_sentences(sentences, output_filename):
    with open(output_filename, "w", encoding="utf-8") as f:
        for sentence in sentences:
            # 각 토큰을 하나의 문자열로 결합하여 한 줄로 만듦
            line = sentence.strip() + "\n"
            f.write(line)

def process_files(directory, output_dir):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            process_files(file_path, output_dir)  # 디렉터리인 경우 재귀적으로 처리
        else:
            sentences = tokenize_file(file_path)
            output_filename = os.path.basename(file_path)
            output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + "_tokenized.txt")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            save_tokenized_sentences(sentences=sentences, output_filename=output_filename)


def init():
    parser = argparse.ArgumentParser(description='Tokenize files in a directory or a single file.')
    parser.add_argument('source', metavar='SOURCE', type=str, help='path to the source directory or file')
    parser.add_argument('output', metavar='OUTPUT', type=str, default = "output/" ,help='path to the output directory')
    args = parser.parse_args()

    process_files(args.source, args.output)
    
if __name__ == "__main__":
    init()