import os
import argparse

def process_files(directory, output_dir):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            process_files(file_path, output_dir)  # 디렉터리인 경우 재귀적으로 처리
        else:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # 여기부터
            
def init():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('source', metavar='SOURCE', type=str, help='path to the source')
    parser.add_argument('output', metavar='OUTPUT', type=str, 
	                    default = "output/", help='path to the output ')
    args = parser.parse_args()

    process_files(args.source, args.output)
    
if __name__ == "__main__":
    init()