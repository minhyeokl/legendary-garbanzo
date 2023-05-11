# Tools for Machine Translation

기계 번역을 위한 각종 도구를 모아놓은 저장소.

## tokenizer.py
```
python tokenizer.py source/ output/
```
txt 파일이 들어있는 디렉터리를 입력하면 모든 txt 파일들을 읽어 문장별로 토크나이징한다.

## html2markdown.py
```
python html2markdown.py source/ output/
```
html 파일이 들어있는 디렉터리를 입력하면 모든 html 파일을 읽어 마크다운 파일로 변환합니다.

## htmltranslator.py
```
python htmltranslator.py source/ output/
```
html 파일이 들어있는 디렉터리를 입력하면 모든 html 파일을 읽어 번역합니다. (html 내 pre 태그는 번역에서 제외)
