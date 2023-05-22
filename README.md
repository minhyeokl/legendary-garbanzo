# Tools for Machine Translation

기계 번역을 위한 각종 도구를 모아놓은 저장소.

## tokenizer.py
```
python tokenizer.py <INPUT> <OUTPUT>
```
txt, md 파일을 문장별로 토크나이징한다. `<INPUT>`에 디렉터리를 입력하면 디렉터리 내의 모든 txt, md 파일을 찾아 작업을 진행한다.

## html2markdown.py
```
python html2markdown.py <INPUT> <OUTPUT>
```
html 파일을 마크다운 파일로 변환한다. `<INPUT>`에 디렉터리를 입력하면 디렉터리 내의 모든 html 파일을 찾아 작업을 진행한다.

## htmltranslator.py
```
python htmltranslator.py <INPUT> <OUTPUT>
```
html 파일을 구글 번역기를 사용해 번역한다(html 내 pre 태그는 번역에서 제외).  `<INPUT>`에 디렉터리를 입력하면 디렉터리 내의 모든 html 파일을 찾아 작업을 진행한다.

## mathml2latex.py
```
python htmltranslator.py <INPUT> <OUTPUT>
```
html 파일에서 MathML로 작성된 수식을 찾아 LaTeX로 변환한 결과물을 엑셀파일로 저장한다. `<INPUT>`에 디렉터리를 입력하면 디렉터리 내의 모든 html 파일을 찾아 작업을 진행한다.
