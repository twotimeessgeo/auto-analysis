# Auto Analysis

PDF 시험지를 문항별 이미지로 자르고, Gemini API로 사회탐구 지리 문항 해설 CSV를 생성하는 로컬 GUI입니다.

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
- 기본 모델은 `gemini-3.1-pro-preview`입니다.
- Gemini Pro 계열은 타임아웃을 줄이기 위해 동시 요청 수를 2개 이하로 제한합니다.
