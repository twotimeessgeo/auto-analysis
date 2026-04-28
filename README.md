# Auto Analysis

PDF 시험지를 문항별 이미지로 자르고, Gemini API로 사회탐구 지리 문항 해설 CSV를 생성하는 로컬 GUI입니다.
해설 편집 화면에서 문항별 단원 분류를 붙이고, 원본 분류표 형식의 XLSX로 내보낼 수 있습니다.

## GitHub Pages

GitHub Pages는 정적 파일만 호스팅하므로 Flask 서버, PDF 분할, Gemini 프록시 API는 Pages에서 직접 실행되지 않습니다.

공개 Pages에는 API 키가 포함되지 않은 안내 페이지를 배포합니다. 실제 분석 기능은 로컬에서 실행합니다.

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

브라우저에서 `http://127.0.0.1:5057/`을 엽니다.

macOS에서는 `start_gui.command`를 실행해도 됩니다.
처음 실행할 때 필요한 패키지를 자동으로 설치한 뒤 브라우저를 엽니다.

## Team Sharing

프로그래밍에 익숙하지 않은 팀원에게는 아래 방식이 가장 단순합니다.

공유 ZIP은 아래 명령으로 만듭니다.

```bash
python3 make_share_package.py
```

그러면 `dist/Auto_Analysis_공유용.zip`이 생성됩니다. 이 ZIP에는 실행에 필요한 파일과 샘플 `4월 NEW` 하나만 들어가며, Gemini API 키는 포함되지 않습니다.

팀원 사용 방법:

1. `Auto_Analysis_공유용.zip`을 풀어 둡니다.
2. Windows 사용자는 `Auto Analysis 실행 - Windows.bat`을 더블클릭합니다.
3. macOS 사용자는 `Auto Analysis 실행 - macOS.command`를 더블클릭합니다.
4. 브라우저가 열리면 Gemini API 키를 입력하고 사용합니다.
5. 샘플은 `모의고사 보관함`에서 `4월 NEW`를 불러오면 됩니다.

API 키는 ZIP에 넣지 않는 편이 안전합니다. 팀원이 각자 GUI 입력칸에 붙여 넣거나, 로컬 전용 `local_settings.json`을 각자 만들어 쓰는 방식이 좋습니다.

## Gemini API Key

API 키는 저장소에 커밋하지 않습니다.

사용 방법:

- GUI의 `Gemini API 키` 입력칸에 직접 입력합니다.
- 또는 로컬 전용 `local_settings.json`에 저장합니다. 이 파일은 `.gitignore`에 포함되어 커밋되지 않습니다.
- 또는 환경변수 `GEMINI_API_KEY`로 지정합니다.

예시:

```bash
export GEMINI_API_KEY="YOUR_KEY"
python3 app.py
```

## Notes

- 기본 사이트 제목은 `Auto Analysis`입니다.
- 기본 과목은 `세계지리`입니다.
- 기본 모델은 `gemini-3.1-pro-preview`입니다.
- Gemini Pro 계열은 타임아웃을 줄이기 위해 동시 요청 수를 2개 이하로 제한합니다.
