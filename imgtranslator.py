import argparse
import os
import base64
import requests

from openai import OpenAI

def main():
  parser = argparse.ArgumentParser(description="Process a directory path.")
  parser.add_argument('directory', type=str, help='The path to the directory')

  args = parser.parse_args()

  if os.path.isdir(args.directory):
    translate_images(args.directory)
  else:
    print(f"The provided path is not a directory: {args.directory}")

def translate_images(directory):
  # get the list of png, jpg, jpeg, gif in the directory
  image_files = [f for f in os.listdir(directory) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.gif')]
  for image_file in image_files:
    image_path = os.path.join(directory, image_file)
    result = translate_image(image_path)
    # save result as txt file with same file name without extension in source directory
    if result == "None":
      continue
    with open(os.path.join(directory, os.path.splitext(image_file)[0] + '.txt'), 'w') as f:
      f.write(result)
    print(result)

def translate_image(image_path):
  #use openai assistant api to translate the image
  image_data = encode_image(image_path)
  # api_key = 
  headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
  }
  prompt = '''
**시스템 프롬프트:**

당신은 텍스트 이미지에서 텍스트를 추출하고, 이를 원문-번역문 형태로 제공하는 GPT 어시스턴트입니다. 사용자가 이미지를 업로드하면 이미지를 분석하여 텍스트를 추출하고, 이를 원문과 번역문 형태로 정리해서 반환합니다. 모든 작업은 정확하고 신속하게 이루어져야 하며, 사용자가 제공한 언어로 텍스트를 번역해야 합니다.

작업 지침:
1. 사용자가 이미지를 업로드하면, 이미지를 분석하여 모든 텍스트를 추출합니다.
2. 추출한 텍스트를 원문-번역문 형태로 변환합니다.
3. 번역은 가능한 한 정확하게 수행하며, 의미를 명확하게 전달해야 합니다.
4. 결과는 사용자에게 원문-번역문 형태로 반환합니다.
5. 결과만 출력합니다. 다른 내용은 담지 않습니다.
6. 이 텍스트는 컴퓨터 과학과 관련된 텍스트로 소프트웨어 아키텍처에 관한 내용을 담았습니다. 이에 맞게 번역을 수행해야 합니다.
7. 이미지가 없거나 이미지에 텍스트가 없으면, "None"이라고 반환합니다.

예시:
- 사용자가 업로드한 이미지에 "Output probabilities" 텍스트가 포함되어 있다면:
  Output probabilities - 출력 확률
- 사용자가 업로드한 이미지에 "Softmax" 텍스트가 포함되어 있다면:
  Softmax - 소프트맥스

언어:
- 기본 언어는 영어이며, 번역은 한국어로 합니다. 필요 시, 사용자가 다른 언어로 번역을 요청할 수 있습니다.

추가 지침:
- 이미지를 분석할 때, 모든 텍스트를 빠짐없이 추출합니다.
- 번역이 어려운 경우, 가능한 한 유사한 의미를 전달하는 번역을 시도합니다.
- 항상 친절하고 전문적인 태도로 응대합니다.

이 시스템 프롬프트를 바탕으로 텍스트 추출 및 번역 작업을 정확하게 수행하십시오.'''
  payload = {
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{image_data}"
            }
          }
        ]
      }
    ]
  }
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  response_data = response.json()
  return response_data['choices'][0]['message']['content']

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')




if __name__ == "__main__":
  main()
