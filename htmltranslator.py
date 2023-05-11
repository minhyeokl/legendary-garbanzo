import os
import argparse
from bs4 import BeautifulSoup
from google.cloud import translate
from dotenv import load_dotenv

load_dotenv(verbose=True)
PROJECT_ID = os.getenv('PROJECT_ID')
MODEL_ID = os.getenv('MODEL_ID')
def translate_text_with_model(
    text="",
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
):
    client = translate.TranslationServiceClient()

    location = 'us-central1',
    parent = f"projects/{project_id}/locations/{location}"
    model_path = f"{parent}/models/{model_id}"

    response = client.translate_text(
        request={
            "contents": [text],
            "model": model_path,
            "source_language_code": "en",
            "target_language_code": "ko",
            "parent": parent,
            "mime_type": "text/html",  # mime types: text/plain, text/html
        })
    for translation in response.translations:
        if translation == None:
            continue
        return translation.translated_text

def check_html(input_file):
    with open(input_file, "r") as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text, "html.parser")
    elements = soup.children
    result = ''
    for element in elements:
        if element.name == None or element.name == "pre":
            result += str(element) + '\n'

        else:
            #번역 넘기기
            translated_par = translate_text_with_model(text=str(element))
            result += translated_par + '\n'
    return result

def save_file(result, input_file, output_dir):
    output_filename = os.path.basename(input_file)
    output_filename = os.path.join(output_dir, os.path.splitext(output_filename)[0] + "_result.html")
    with open(output_filename, "w") as r:
        r.write(result)


def process_files(input, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    result = ''
    if os.path.isdir(input):
        for filename in os.listdir(input):
            file_path = os.path.join(input, filename)
            if os.path.isdir(file_path):
                process_files(file_path, output_dir)  # 디렉터리인 경우 재귀적으로 처리
            else:
                result = check_html(file_path)
                save_file(result, file_path, output_dir)
    else:
        result = check_html(input)
        save_file(result, input, output_dir)
        


def init():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('source', metavar='SOURCE', type=str, help='path to the source')
    parser.add_argument('output', metavar='OUTPUT', type=str, 
	                default = "output/", help='path to the output ')
    args = parser.parse_args()

    process_files(args.source, args.output)
    
if __name__ == "__main__":
    init()
