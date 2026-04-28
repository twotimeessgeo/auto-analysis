#!/usr/bin/env python3
"""Local GUI for splitting exam PDFs into question images."""

from __future__ import annotations

import json
import base64
import csv
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Callable
from uuid import uuid4

from flask import Flask, jsonify, render_template, request, send_file, send_from_directory
from PIL import Image, ImageDraw, ImageOps
from werkzeug.utils import secure_filename

from geo_cut_predictor import (
    PredictionError,
    historical_exam_payload,
    model_public_payload,
    predict_cut,
    question_image_path,
    refresh_question_bank,
    search_question_bank,
)
from split_exam_questions import split_pdf


class GeminiRequestError(RuntimeError):
    attempts: list[str]

    def __init__(self, message: str, attempts: list[str]):
        super().__init__(message)
        self.attempts = attempts


class ApiRequestError(ValueError):
    status_code: int
    payload: dict[str, object]

    def __init__(self, payload: dict[str, object], status_code: int = 400):
        super().__init__(str(payload.get("error") or "요청을 처리하지 못했습니다."))
        self.payload = payload
        self.status_code = status_code


ROOT = Path(__file__).resolve().parent
DESIGN_DIR = ROOT / "design-system"
RUNS_DIR = ROOT / "gui_runs"
ARCHIVES_DIR = ROOT / "archives"
LOCAL_SETTINGS_PATH = ROOT / "local_settings.json"
RUNS_DIR.mkdir(exist_ok=True)
ARCHIVES_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 80 * 1024 * 1024

SOLUTION_COLUMNS = [
    "문항 번호",
    "정답",
    "예상 정답률",
    "선택 비율 예상",
    "추정 변별도",
    "추정 타당도",
    "오류 가능성",
    "해설",
    "정답 풀이",
    "오답 풀이",
    "검토 메모(장점)",
    "검토 메모(약점)",
    "수정 필요 여부",
    "수정 제안",
    "Comment 제목",
    "Comment 내용",
]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
GEMINI_DEFAULT_MODEL = "gemini-3.1-pro-preview"
GEMINI_MODEL_ALIASES = {
    "gemini-flash-latest": "gemini-flash-latest",
    "gemini-pro-latest": "gemini-pro-latest",
    "gemini-3-flash": "gemini-3-flash-preview",
    "gemini-3-flash-preview": "gemini-3-flash-preview",
    "gemini-3-pro": "gemini-3-pro-preview",
    "gemini-3-pro-preview": "gemini-3-pro-preview",
    "gemini-3.1-pro": "gemini-3.1-pro-preview",
    "gemini-3.1-pro-preview": "gemini-3.1-pro-preview",
    "gemini-2.5-flash": "gemini-2.5-flash",
    "gemini-2.5-pro": "gemini-2.5-pro",
    "gemini-2.5-flash-lite": "gemini-2.5-flash-lite",
    "gemini-3.0-flash-preview": "gemini-3-flash-preview",
    "gemini-1.5-flash": "gemini-2.5-flash",
    "gemini-1.5-pro": "gemini-2.5-pro",
}
GEMINI_DEFAULT_PROMPT = """역할
너는 사회탐구 지리 문항 전용 해설·검수 GPT이다.
사용자가 올린 문제 이미지, PDF, 또는 캡처를 읽고, 사용자의 해설지 문체와 양식에 맞춰 문항별 해설을 작성한다.
동시에 문항의 예상 정답률, 선택 비율 예상, 추정 변별도, 추정 타당도, 오류 가능성을 점검한다.

최우선 원칙
- 출력은 사용자의 해설지 스타일을 따른다.
- 문체는 단정적이고 건조하며 설명 밀도가 높아야 한다.
- 과장, 감탄, 홍보성 표현, 교사식 장황한 친절체를 쓰지 않는다.
- 자료의 핵심 요소를 먼저 특정한 뒤 풀이에 들어간다.
- 정답률·선택 비율·변별도·타당도는 실제 응답 데이터가 없으면 반드시 추정으로 취급한다.
- 이미지 판독이 불충분하면 억지로 추측하지 말고 판독 보류를 명시한다.
- 해설은 사실 관계만 간결하게 적는다.
- 해설에는 F, 핵심 단서이다, 낚시 포인트이다, 옳은 진술이다, 틀린 진술이다 같은 메타 표현을 쓰지 않는다.
- 정답 풀이에서는 불필요한 총평이나 메타 설명 없이 사실관계만 쓴다.
- 합답형/조합형에서는 정답 풀이에 ㄱ., ㄴ., ㄷ.만 표시하고, 정답 번호를 다시 반복하지 않는다.
- 단순 5지선다에서는 정답 풀이 첫머리를 ⑤처럼 번호만 쓰고, 번호 뒤에 마침표를 찍지 않는다.
- 조합형에서는 오답 풀이를 원칙적으로 생략한다.
- 오류 가능성은 반드시 따로 점검한다.
- Comment 섹션은 예외적으로 짧은 구어체를 허용한다.
- Comment는 해설의 반복이 아니라, 문제에서 추가로 얻어갈 수 있는 배경지식(a.k.a 썰)을 짧게 제시한다.

작업 절차
1단계. 문항 판독
- 문제 번호, 단원, 자료 유형(지도/표/그래프/사진/대화문 등), 선택지 형식을 파악한다.
- (가)(나)(다), A/B/C, 갑/을/병/정, 국가/지역/도시/시기 등을 먼저 특정한다.
- 판독이 불충분하면 무엇이 안 보이는지 짧게 밝힌다.

2단계. 정답 판단
- 문제의 핵심 개념과 판정 기준을 분명히 잡는다.
- 5지선다이면 각 선택지를 판정한다.
- ㄱ/ㄴ/ㄷ 조합형이면 ㄱ, ㄴ, ㄷ의 참거짓을 먼저 판정한 뒤 최종 정답 번호를 도출한다.

3단계. 해설 작성
- 해설은 한두 문장으로 짧게 쓴다.
- 첫 문장은 자료 속 대상 특정에 쓴다.
- 필요할 때만 둘째 문장에서 풀이의 출발점을 덧붙인다.
- 해설은 사실 관계만 적고, 평가적·주관적 표현은 쓰지 않는다.

4단계. 정답 풀이 작성
- 단순 5지선다에서는 정답 번호만 적고 바로 이유를 쓴다. 예: ⑤ 이스라엘은 ...
- ㄱ/ㄴ/ㄷ 조합형에서는 ㄱ., ㄴ., ㄷ.만 쓰고 각 진술의 사실관계만 적는다.
- 조합형에서 ⑤., ㄱ은 옳다, ㄴ은 틀리다, 옳은 진술이다, 틀린 진술이다 같은 표현은 금지한다.
- 조합형에서는 사실관계 설명만으로 참/거짓이 드러나게 쓴다.

5단계. 오답 풀이 작성
- 단순 5지선다일 때 각 오답 선택지가 왜 틀렸는지 한 줄씩 짧게 쓴다.
- 조합형에서는 오답 풀이를 원칙적으로 생략한다.

6단계. 문항 진단
- 예상 정답률을 전국 기준 체감 정답률로 5% 단위 추정한다.
- 선택 비율 예상은 ①~⑤ 전체가 합쳐 100%가 되도록 제시한다.
- 정답률과 정답 선택지 비율은 일치해야 한다.
- 추정 변별도는 상/중/하와 5점 척도를 함께 제시한다.
- 추정 타당도는 상/중/하와 5점 척도를 함께 제시한다.
- 오류 가능성은 낮음/보통/높음으로 제시하고, 이유를 짧게 덧붙인다.
- 오류 가능성이 보통 이상이면 수정 제안을 짧게 덧붙인다.

7단계. Comment 작성
- 해설과 중복되지 않는 짧은 배경지식(썰)을 뽑는다.
- 제목은 짧게 쓴다.
- 내용은 2~4문장 이내의 짧은 구어체로 쓴다.
- 단순 감상, 칭찬, 억지 드립은 금지한다.

출력 형식
- 정답, 예상 정답률, 선택 비율 예상, 추정 변별도, 추정 타당도, 오류 가능성, 해설, 정답 풀이, 오답 풀이, 검토 메모, Comment를 반드시 작성한다.
- 단순 5지선다는 정답 풀이 첫 줄을 ⑤처럼 번호만 쓰고, 번호 뒤에 마침표를 찍지 않는다.
- 오답 풀이에서는 ①~④ 또는 해당 오답 번호만 쓴다.
- ㄱ/ㄴ/ㄷ 조합형 정답 풀이에는 ㄱ., ㄴ., ㄷ.만 쓴다.
- 조합형에서는 정답 번호를 다시 쓰지 않고, 옳은 진술이다/틀린 진술이다/정답은 ㄱ, ㄴ, ㄷ이다 같은 표현을 쓰지 않는다.

변별도 추정 기준
- 상, 4.0~5.0/5: 개념은 명확하지만 오답 매력도 높고 상위권과 중위권이 갈릴 가능성이 큰 문항
- 중, 2.5~3.5/5: 정답 고정은 가능하지만 자료 외피나 일부 오답이 기능하는 문항
- 하, 1.0~2.0/5: 지나치게 직선적이거나, 반대로 애매해서 실력보다 운이 많이 개입하는 문항

타당도 추정 기준
- 상, 4.0~5.0/5: 교과 핵심 개념을 정확히 측정하고, 정답 판단에 불필요한 잡지식 의존이 적은 문항
- 중, 2.5~3.5/5: 개념은 맞지만 자료 표현이나 선지 구성상 불필요한 부담이 섞인 문항
- 하, 1.0~2.0/5: 핵심 개념보다 지엽, 표현 함정, 최신 통계 암기, 애매한 자료 판독이 더 크게 작용하는 문항

오류 가능성 점검 기준
- 정답이 둘 이상으로 읽힐 여지
- 자료의 범례/축/지도상 위치가 불명확한지
- 최신 시사/통계/국제기구 회원국처럼 시점 민감성이 큰지
- 선지 문장이 과도하게 단정적이거나 예외를 무시하는지
- 정답의 근거가 문제 내부 자료보다 바깥 지식에 과도하게 의존하는지
- 출제 의도와 실제 정답 판단 기준이 어긋나는지
- 지리적 표현이 부정확하거나 다른 단원 개념이 섞여 혼동되는지

문체 규칙
- ~이다, ~않다만 사용한다.
- 필요 없는 수식어를 줄이고 정보 밀도를 높인다.
- 해설은 사실 관계만 적는다.
- 핵심 단서이다, 낚시 포인트이다, 중요하다, 옳다, 틀리다 같은 메타 서술은 원칙적으로 금지한다.
- 사용자의 해설지처럼 먼저 대상을 고정하고 그다음 선지를 판정한다.
- 최근 기출과의 연결은 자연스러울 때만 한 줄 정도 언급한다.
- 자신 없으면 단정하지 말고 판독 보류 또는 오류 가능성 보통 이상으로 처리한다.

판독 불가 시 예외 출력
- 정답: 판독 보류
- 예상 정답률: 판독 보류
- 선택 비율 예상: 판독 보류
- 추정 변별도: 판독 보류
- 추정 타당도: 판독 보류
- 오류 가능성: 높음. 이미지 해상도 또는 자료 일부가 불분명하여 정답 판단 근거가 부족하다.
- 해설/정답 풀이/오답 풀이: 판독 보류
- 검토 메모: 장점은 판독 보류, 약점은 자료 또는 선택지 식별 불가, 수정 필요 여부는 필요, 수정 제안은 더 선명한 이미지 또는 원문 텍스트 필요
- Comment: 제목은 판독 보류, 내용은 더 선명한 이미지가 필요하다.

절대 금지
- 이미지에 없는 정보를 멋대로 추가하지 말 것
- 최근 통계나 시사 정보를 단정적으로 끼워 넣지 말 것
- 좋은 문제, 훌륭한 문제 같은 감상 위주 문장을 길게 쓰지 말 것
- 실측 통계가 없는데 정답률, 선택 비율, 변별도, 타당도를 확정값처럼 말하지 말 것
- 핵심 단서이다, 낚시 포인트이다, 옳은 진술이다, 틀린 진술이다를 쓰지 말 것
- 조합형에서 ⑤.처럼 정답 번호를 다시 쓰지 말 것"""
GEMINI_JSON_FORMAT_INSTRUCTION = """
반드시 JSON 객체 하나만 출력한다. 코드블록, 설명문, 인사말을 추가하지 않는다.
키 이름을 바꾸지 않는다. 값은 CSV 한 칸에 들어갈 수 있는 문자열 또는 숫자만 사용한다.
판독 보류일 때도 모든 키를 채운다.

{
  \"문항 번호\": 1,
  \"정답\": \"1\",
  \"예상 정답률\": 37,
  \"선택 비율 예상\": \"① 15%, ② 20%, ③ 25%, ④ 25%, ⑤ 15%\",
  \"추정 변별도\": \"중, 3.2/5\",
  \"추정 타당도\": \"상, 4.1/5\",
  \"오류 가능성\": \"보통\",
  \"해설\": \"...\",
  \"정답 풀이\": \"...\",
  \"오답 풀이\": \"...\",
  \"검토 메모(장점)\": \"...\",
  \"검토 메모(약점)\": \"...\",
  \"수정 필요 여부\": \"불필요\",
  \"수정 제안\": \"없음\",
  \"Comment 제목\": \"...\",
  \"Comment 내용\": \"...\",
  \"예측 점수\": 0.73
}
"""
GEMINI_JSON_FALLBACK_LABELS = (
    "문항 번호",
    "정답",
    "예상 정답률",
    "선택 비율 예상",
    "추정 변별도",
    "추정 타당도",
    "오류 가능성",
    "해설",
    "정답 풀이",
    "오답 풀이",
    "검토 메모(장점)",
    "검토 메모(약점)",
    "수정 필요 여부",
    "수정 제안",
    "Comment 제목",
    "Comment 내용",
    "예측 점수",
)
AUTO_GENERATED_SOLUTION_COLUMNS = SOLUTION_COLUMNS + ["예측 점수"]
GEMINI_DEFAULT_MAX_REQUESTS = 20
GEMINI_DEFAULT_CONCURRENCY = 3
GEMINI_EXECUTION_LOG_FILENAME = "gemini_execution_log.json"
GEMINI_GENERATED_CSV = "auto_generated_solutions.csv"
GEMINI_CUT_LOG_FILENAME = "predicted_cut_log.json"
GEMINI_API_TIMEOUT_SECONDS = 180
GEMINI_RETRY_TIMEOUT_SECONDS = 240
GEMINI_MAX_ATTEMPTS_PER_QUESTION = 2
GEMINI_DEFAULT_MIME = "image/png"
GEMINI_REQUEST_PATHS = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
)
GEMINI_MODELS_LIST_URL = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_PREFERRED_MODEL_ORDER = (
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-3-pro-preview",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-pro-latest",
)
JOB_PROGRESS_FILENAME = "progress.json"
JOB_RESULT_FILENAME = "result.json"
JOB_ERROR_FILENAME = "error.json"
JOB_PROGRESS_LOCK = threading.Lock()
GEMINI_FIELD_SYNONYMS: dict[str, str] = {
    "번호": "문항 번호",
    "문항번호": "문항 번호",
    "문항_id": "문항 번호",
    "문항번호는": "문항 번호",
    "정답": "정답",
    "정답번호": "정답",
    "정답률": "예상 정답률",
    "정답률예상": "예상 정답률",
    "예상 정답률": "예상 정답률",
    "예상정답률": "예상 정답률",
    "정답률 예측": "예상 정답률",
    "예상 정답률(%)": "예상 정답률",
    "선택비율예상": "선택 비율 예상",
    "선택 비율": "선택 비율 예상",
    "선택 비율예상": "선택 비율 예상",
    "변별도": "추정 변별도",
    "추정변별도": "추정 변별도",
    "타당도": "추정 타당도",
    "추정타당도": "추정 타당도",
    "오류가능성": "오류 가능성",
    "예측 점수": "예측 점수",
    "예측점수": "예측 점수",
    "score": "예측 점수",
    "해설": "해설",
    "해설 내용": "해설",
    "문항 판독": "해설",
    "문항_판독": "해설",
    "해설 작성": "해설",
    "해설_작성": "해설",
    "정답설명": "정답 풀이",
    "답안 해설": "해설",
    "정답 판단": "정답 판단",
    "정답_판단": "정답 판단",
    "정답 풀이": "정답 풀이",
    "정답_풀이": "정답 풀이",
    "오답 풀이": "오답 풀이",
    "오답_풀이": "오답 풀이",
    "오답해설": "오답 풀이",
    "검토 메모(장점)": "검토 메모(장점)",
    "문항의 장점": "검토 메모(장점)",
    "검토 메모 장점": "검토 메모(장점)",
    "검토 메모(약점)": "검토 메모(약점)",
    "문항의 약점": "검토 메모(약점)",
    "검토 메모 약점": "검토 메모(약점)",
    "수정 필요 여부": "수정 필요 여부",
    "수정필요여부": "수정 필요 여부",
    "수정 필요": "수정 필요 여부",
    "수정 제안": "수정 제안",
    "수정제안": "수정 제안",
    "comment 제목": "Comment 제목",
    "comment 제목(짧게)": "Comment 제목",
    "comment 내용": "Comment 내용",
    "comment": "Comment 내용",
    "Comment": "Comment 내용",
    "문항 진단": "문항 진단",
    "문항_진단": "문항 진단",
}


def uploaded_suffix(filename: str | None) -> str:
    return Path(filename or "").suffix.lower()


def safe_upload_filename(filename: str | None, fallback: str, suffix: str | None = None) -> str:
    target_suffix = suffix or uploaded_suffix(filename) or Path(fallback).suffix
    safe_name = secure_filename(filename or "")
    fallback_path = Path(fallback)
    if not safe_name:
        safe_name = fallback_path.stem

    safe_path = Path(safe_name)
    if target_suffix and safe_path.suffix.lower() != target_suffix:
        if safe_name.lower() == target_suffix.lstrip(".") or not safe_path.stem:
            stem = fallback_path.stem
        else:
            stem = safe_path.stem if safe_path.suffix else safe_name
        safe_name = f"{stem}{target_suffix}"
    return safe_name


def clean_int(value: str | None, default: int, low: int, high: int) -> int:
    try:
        parsed = int(value or default)
    except (TypeError, ValueError):
        return default
    return max(low, min(high, parsed))


def clean_text(value: str | None) -> str:
    return (value or "").strip()


def load_local_settings() -> dict[str, object]:
    if not LOCAL_SETTINGS_PATH.exists():
        return {}
    try:
        payload = json.loads(LOCAL_SETTINGS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def local_setting_text(settings: dict[str, object], key: str) -> str:
    return clean_text(str(settings.get(key) or ""))


def env_setting_text(key: str) -> str:
    return clean_text(os.environ.get(key, ""))


def configured_setting_text(settings: dict[str, object], key: str, env_key: str) -> str:
    return local_setting_text(settings, key) or env_setting_text(env_key)


def build_gemini_prompt(prompt: str, question_number: int, strict: bool = False) -> str:
    base_prompt = clean_text(prompt) or GEMINI_DEFAULT_PROMPT
    retry_note = "\n\n이전 응답이 CSV 양식 키를 충분히 채우지 못했다. 아래 JSON 키 이름을 정확히 사용한다." if strict else ""
    return (
        f"{base_prompt}\n\n현재 처리 문항: {question_number}번.\n"
        "출력 규칙은 JSON 객체 하나만, 추가 텍스트 없음(코드블록 포함)이다.\n"
        "아래 JSON 키 이름을 그대로 사용해야 CSV 열에 들어간다.\n"
        f"{GEMINI_JSON_FORMAT_INSTRUCTION}{retry_note}"
    )


def _strip_outer_code_fence(raw: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.IGNORECASE).strip()


def _extract_json_blocks(raw: str) -> list[str]:
    stripped = raw.strip()
    if not stripped:
        return []

    blocks: list[str] = []
    for match in re.finditer(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.IGNORECASE | re.DOTALL):
        candidate = _strip_outer_code_fence(match.group(1))
        if candidate:
            blocks.append(candidate)

    # JSON-like balanced-brace blocks, including plain text and nested cases
    depth = 0
    start: int | None = None
    in_string = False
    escape = False
    for index, char in enumerate(stripped):
        if escape:
            escape = False
            continue
        if char == "\\" and in_string:
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(stripped[start : index + 1].strip())
                start = None

    # 마지막으로 전체 텍스트도 후보로 둔다.
    blocks.append(stripped)
    # 중복 제거
    dedupe: list[str] = []
    for block in blocks:
        if block and block not in dedupe:
            dedupe.append(block)
    return dedupe


def _repair_json_text(candidate: str) -> list[str]:
    normalized = _strip_outer_code_fence(candidate).strip()
    if not normalized:
        return []

    repairs = [
        normalized,
        re.sub(r",\s*([}\]])", r"\1", normalized),
    ]
    return list({item for item in repairs if item})


def _clean_loose_json_value(value: str) -> object:
    cleaned = value.strip().rstrip(",")
    if not cleaned:
        return ""
    if cleaned.startswith('"') and cleaned.endswith('"'):
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return cleaned.strip('"')
    if cleaned in {"null", "None"}:
        return ""
    if re.fullmatch(r"-?\d+(?:\.\d+)?", cleaned):
        return float(cleaned) if "." in cleaned else int(cleaned)
    return cleaned.strip('"')


def _extract_loose_json_pairs(raw: str) -> dict[str, object]:
    fallback: dict[str, object] = {}
    pair_pattern = re.compile(
        r'(?m)^\s*,?\s*"([^"]+)"\s*:\s*('
        r'"(?:\\.|[^"\\])*"|'
        r"-?\d+(?:\.\d+)?|"
        r"null|None|"
        r"[^,\n}]+"
        r")\s*,?\s*$"
    )
    for match in pair_pattern.finditer(raw):
        key = match.group(1).strip()
        if key:
            fallback[key] = _clean_loose_json_value(match.group(2))
    return fallback


def clean_json_from_text(value: str | None) -> dict[str, object] | None:
    if not value:
        return None
    raw = str(value).strip().replace("\ufeff", "")
    for candidate in _extract_json_blocks(raw):
        for fixed in _repair_json_text(candidate):
            try:
                parsed = json.loads(fixed)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    # 마지막 안전장치: 제목:값 형태의 줄 단위 응답도 한 번 파싱
    labels = "|".join(re.escape(label) for label in GEMINI_JSON_FALLBACK_LABELS)
    if not labels:
        return None
    line_pattern = re.compile(
        rf"(?m)^(?:[\t ]*[-*\d.]*)?\s*({labels})\s*[:：]\s*(.+?)\s*(?:$|\n(?:[\t ]*[-*\d.]*)?\s*(?:{labels})\s*[:：])",
        re.DOTALL,
    )
    fallback: dict[str, object] = {}
    for match in line_pattern.finditer(raw):
        fallback_key = match.group(1).strip()
        fallback_value = match.group(2).strip()
        if fallback_value.endswith("\n"):
            fallback_value = fallback_value.strip()
        if fallback_key and fallback_value:
            fallback[fallback_key] = fallback_value
    if not fallback:
        fallback = _extract_loose_json_pairs(raw)
    if fallback:
        return fallback
    return None


def utcish_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_question_number(value: str | None) -> int | None:
    match = re.search(r"\d+", value or "")
    if not match:
        return None
    return int(match.group())


def parse_rate_percent(value: str | None) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", value or "")
    if not match:
        return None
    parsed = float(match.group())
    if parsed < 0 or parsed > 100:
        return None
    return round(parsed, 2)


def parse_score_fraction(value: str | None) -> str:
    match = re.search(r"\d+(?:\.\d+)?", value or "")
    if not match:
        return ""
    value_number = float(match.group())
    if not (value_number >= 0):
        return ""
    if value_number <= 1:
        return str(round(value_number, 4))
    if value_number <= 100:
        return str(round(value_number / 100, 4))
    return str(round(min(value_number, 1), 4))


def normalize_gemini_fields(value: dict[str, object], question_number: int) -> dict[str, str]:
    fields: dict[str, str] = {
        "문항 번호": str(question_number),
        "정답": "",
        "예상 정답률": "",
        "예측 점수": "",
        "해설": "",
        "정답 풀이": "",
        "오답 풀이": "",
    }
    for key, raw_value in value.items():
        if not isinstance(key, str):
            continue
        canonical_key = GEMINI_FIELD_SYNONYMS.get(key.strip())
        if not canonical_key:
            canonical_key = GEMINI_FIELD_SYNONYMS.get(key.replace(" ", ""))
        if not canonical_key:
            canonical_key = key.strip()

        if canonical_key == "정답 판단":
            answer = normalize_answer_value(str(raw_value))
            if answer in {"1", "2", "3", "4", "5"} and not fields.get("정답"):
                fields["정답"] = answer
            continue

        if canonical_key == "문항 진단":
            diagnostic_text = clean_text(str(raw_value))
            if not fields.get("예상 정답률"):
                parsed = parse_rate_percent(diagnostic_text)
                fields["예상 정답률"] = str(parsed) if parsed is not None else ""
            if not fields.get("오류 가능성") and ("오류" in diagnostic_text or "가능성" in diagnostic_text):
                fields["오류 가능성"] = normalize_error_risk(diagnostic_text)
            continue

        if canonical_key not in fields:
            fields[canonical_key] = clean_text(str(raw_value))
            continue

        if canonical_key == "문항 번호":
            fields["문항 번호"] = clean_text(str(raw_value)) or str(question_number)
        elif canonical_key == "정답":
            fields["정답"] = normalize_answer_value(str(raw_value))
        elif canonical_key == "예상 정답률":
            parsed = parse_rate_percent(str(raw_value))
            fields["예상 정답률"] = str(parsed) if parsed is not None else ""
        elif canonical_key == "예측 점수":
            score = parse_score_fraction(str(raw_value))
            fields["예측 점수"] = score
        else:
            fields[canonical_key] = clean_text(str(raw_value))

    return fields


def parse_gemini_http_error_body(raw_body: str | None) -> dict[str, str]:
    if not raw_body:
        return {"status": "", "message": "", "code": ""}
    payload = None
    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return {"status": "", "message": raw_body.strip(), "code": ""}
    if not isinstance(payload, dict):
        return {"status": "", "message": raw_body.strip()[:1200], "code": ""}

    error_obj = payload.get("error")
    if not isinstance(error_obj, dict):
        return {"status": "", "message": raw_body.strip(), "code": ""}
    message = clean_text(str(error_obj.get("message", "")))
    status = clean_text(str(error_obj.get("status", "")))
    code = clean_text(str(error_obj.get("code", "")))
    if not code and isinstance(error_obj.get("details"), list):
        for item in error_obj["details"]:
            if not isinstance(item, dict):
                continue
            reason = clean_text(str(item.get("reason", "")))
            if reason:
                code = reason
                break
    return {"status": status, "message": message, "code": code}


def build_gemini_attempt_label(model: str, request_url: str) -> str:
    endpoint = request_url.split("?")[0].replace("https://generativelanguage.googleapis.com", "")
    return f"{model} @ {endpoint}"


def classify_gemini_api_error(message: str, status_code: int | None, error_status: str | None) -> tuple[str, str]:
    normalized_status = (error_status or "").strip().lower()
    if status_code == 404 or normalized_status == "not_found":
        hint = (
            "Gemini 모델 이름/형식이 잘못되었습니다. 예: gemini-2.5-flash 또는 gemini-2.5-pro"
        )
        return ("NOT_FOUND", hint)
    if status_code == 401:
        hint = "API 키가 유효하지 않거나 권한이 없습니다. 키를 다시 확인해 주세요."
        return ("UNAUTHORIZED", hint)
    if status_code == 403:
        hint = "API 키 권한이 제한되었거나 과금/사용 정책 이슈입니다."
        return ("FORBIDDEN", hint)
    if status_code == 429:
        hint = "요청이 과도하게 많아 제한됨(429). 잠시 후 재시도해 주세요."
        return ("RATE_LIMITED", hint)
    return ("", "")


def normalize_subject(value: str | None) -> str:
    value = clean_text(value)
    if not value:
        return ""
    if value in ("한국지리", "world", "korea", "세계지리", "korean geography"):
        return value
    no_space = value.replace(" ", "")
    if no_space in ("한국지리", "한국", "한국지리전문", "한국지리과목", "한국지리/세계지리"):
        return "한국지리"
    if no_space in ("세계지리", "세계", "세계지리전문", "세계지리과목"):
        return "세계지리"
    return value


ANSWER_DIGITS = {
    "①": "1",
    "②": "2",
    "③": "3",
    "④": "4",
    "⑤": "5",
    "❶": "1",
    "❷": "2",
    "❸": "3",
    "❹": "4",
    "❺": "5",
    "➀": "1",
    "➁": "2",
    "➂": "3",
    "➃": "4",
    "➄": "5",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
}


def normalize_answer_value(value: str | None) -> str:
    text = clean_text(value)
    if not text:
        return ""
    for source, digit in ANSWER_DIGITS.items():
        if source in text:
            return digit
    match = re.search(r"[1-5]", text)
    return match.group(0) if match else text


def normalize_score_value(value: str | None) -> str:
    text = clean_text(value)
    if not text:
        return ""
    match = re.search(r"\d+(?:\.\d+)?", text)
    return match.group(0) if match else text


def normalize_error_risk(value: str | None) -> str:
    text = clean_text(value)
    if not text:
        return ""
    compact = re.sub(r"\s+", "", text)
    if "낮" in compact or "없" in compact or "높지않" in compact or "높지는않" in compact:
        return "낮음"
    if "높" in compact or "큼" in compact:
        return "높음"
    if "중" in compact or "보통" in compact:
        return "보통"
    return re.split(r"[\s,./:;|]+", text, maxsplit=1)[0]


def normalize_solution_fields(fields: dict[str, object]) -> dict[str, str]:
    normalized = {
        str(key): clean_text("" if value is None else str(value))
        for key, value in fields.items()
    }
    if "정답" in normalized:
        normalized["정답"] = normalize_answer_value(normalized.get("정답"))
    if "추정 변별도" in normalized:
        normalized["추정 변별도"] = normalize_score_value(normalized.get("추정 변별도"))
    if "추정 타당도" in normalized:
        normalized["추정 타당도"] = normalize_score_value(normalized.get("추정 타당도"))
    if "오류 가능성" in normalized:
        normalized["오류 가능성"] = normalize_error_risk(normalized.get("오류 가능성"))
    return normalized


def normalize_solution_rows(solutions: list[dict[str, object]]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for index, item in enumerate(solutions, start=1):
        if not isinstance(item, dict):
            continue
        raw_fields = item.get("fields")
        fields = normalize_solution_fields(raw_fields if isinstance(raw_fields, dict) else {})
        raw_label = fields.get("문항 번호") or clean_text(
            str(item.get("label") or item.get("number") or index)
        )
        number = parse_question_number(raw_label) or parse_question_number(str(item.get("number"))) or index
        fields["문항 번호"] = raw_label
        try:
            row = int(item.get("row") or index + 1)
        except (TypeError, ValueError):
            row = index + 1
        normalized.append(
            {
                "number": number,
                "label": raw_label,
                "row": row,
                "fields": fields,
            }
        )

    normalized.sort(key=lambda row: int(row["number"]))
    return normalized


def parse_solutions_csv(csv_path: Path) -> tuple[list[str], list[dict[str, object]], str]:
    last_decode_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            with csv_path.open("r", encoding=encoding, newline="") as handle:
                reader = csv.DictReader(handle)
                fieldnames = reader.fieldnames or []
                if not fieldnames:
                    raise ValueError("CSV 헤더를 찾지 못했습니다.")

                rows: list[dict[str, object]] = []
                for index, row in enumerate(reader, start=2):
                    fields = normalize_solution_fields(
                        {name: clean_text(row.get(name)) for name in fieldnames}
                    )
                    number = parse_question_number(fields.get("문항 번호"))
                    if number is None:
                        continue
                    rows.append(
                        {
                            "number": number,
                            "label": fields.get("문항 번호") or str(number),
                            "row": index,
                            "fields": fields,
                        }
                    )

                return fieldnames, normalize_solution_rows(rows), encoding
        except UnicodeDecodeError as exc:
            last_decode_error = exc

    if last_decode_error:
        raise ValueError("CSV 인코딩을 읽지 못했습니다. UTF-8 또는 CP949 CSV로 저장해주세요.")
    raise ValueError("CSV를 읽지 못했습니다.")


def question_numbers(output_dir: Path) -> set[int]:
    numbers: set[int] = set()
    for path in output_dir.glob("q*.png"):
        try:
            numbers.add(int(path.stem.replace("q", "")))
        except ValueError:
            continue
    return numbers


def safe_job_dir(job_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", job_id):
        raise ValueError("잘못된 작업 ID입니다.")
    return RUNS_DIR / job_id


def read_json_file(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return payload if isinstance(payload, dict) else None


def progress_file(job_dir: Path) -> Path:
    return job_dir / JOB_PROGRESS_FILENAME


def result_file(job_dir: Path) -> Path:
    return job_dir / JOB_RESULT_FILENAME


def error_file(job_dir: Path) -> Path:
    return job_dir / JOB_ERROR_FILENAME


def append_job_progress(
    job_id: str,
    job_dir: Path,
    *,
    status: str,
    stage: str,
    message: str,
    progress: int | None = None,
    level: str = "info",
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    now = utcish_now()
    with JOB_PROGRESS_LOCK:
        current = read_json_file(progress_file(job_dir)) or {
            "job_id": job_id,
            "events": [],
            "created_at": now,
        }
        events = current.get("events")
        if not isinstance(events, list):
            events = []
        events.append(
            {
                "time": now,
                "stage": stage,
                "message": message,
                "level": level,
                "progress": progress,
                **(details or {}),
            }
        )
        payload: dict[str, object] = {
            **current,
            "job_id": job_id,
            "status": status,
            "stage": stage,
            "message": message,
            "progress": progress,
            "updated_at": now,
            "events": events[-240:],
        }
        progress_file(job_dir).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return payload


def progress_callback_for_job(
    job_id: str,
    job_dir: Path,
    requested: int,
) -> Callable[[dict[str, object]], None]:
    total = max(1, requested)

    def callback(event: dict[str, object]) -> None:
        event_type = str(event.get("type") or "")
        question_number = event.get("question_number", "-")
        processed = int(event.get("processed") or 0)
        if event_type == "request_start":
            percent = min(94, 35 + int((processed / total) * 58))
            concurrency = int(event.get("concurrency") or 1)
            suffix = f" (동시 {concurrency}개)" if concurrency > 1 else ""
            append_job_progress(
                job_id,
                job_dir,
                status="running",
                stage="GEMINI",
                message=f"Gemini {question_number}번 문항 요청 중{suffix}",
                progress=percent,
                level="info",
            )
            return

        if event_type == "request_done":
            percent = min(96, 35 + int((processed / total) * 60))
            status_text = "성공" if event.get("status") == "ok" else "실패"
            answer = clean_text(str(event.get("answer") or ""))
            error = clean_text(str(event.get("error") or ""))
            suffix = f" / 정답 {answer}" if answer else f" / {error}" if error else ""
            append_job_progress(
                job_id,
                job_dir,
                status="running",
                stage="GEMINI",
                message=f"Gemini {question_number}번 문항 {status_text}{suffix}",
                progress=percent,
                level="success" if event.get("status") == "ok" else "error",
            )

    return callback


def safe_archive_dir(archive_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", archive_id):
        raise ValueError("잘못된 아카이브 ID입니다.")
    return ARCHIVES_DIR / archive_id


def archive_index_path() -> Path:
    return ARCHIVES_DIR / "index.json"


def read_archive_index() -> list[dict[str, object]]:
    index_path = archive_index_path()
    if not index_path.exists():
        return []
    try:
        items = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return items if isinstance(items, list) else []


def write_archive_index(items: list[dict[str, object]]) -> None:
    archive_index_path().write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def archive_metadata_path(archive_id: str) -> Path:
    return safe_archive_dir(archive_id) / "archive.json"


def read_archive_payload(archive_id: str) -> dict[str, object]:
    path = archive_metadata_path(archive_id)
    if not path.exists():
        raise FileNotFoundError("아카이브를 찾지 못했습니다.")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("아카이브 정보를 읽지 못했습니다.") from exc
    if not isinstance(payload, dict):
        raise ValueError("아카이브 정보 형식이 올바르지 않습니다.")
    return payload


def update_archive_index_item(updated: dict[str, object]) -> None:
    items = read_archive_index()
    archive_id = updated.get("archive_id")
    replaced = False
    for index, item in enumerate(items):
        if isinstance(item, dict) and item.get("archive_id") == archive_id:
            items[index] = updated
            replaced = True
            break
    if not replaced:
        items.append(updated)
    write_archive_index(items)


def solution_cut_rates(solutions: list[dict[str, object]]) -> list[dict[str, float | int]]:
    rates: list[dict[str, float | int]] = []
    for item in solutions:
        fields = item.get("fields")
        if not isinstance(fields, dict):
            continue
        rate = parse_rate_percent(str(fields.get("예상 정답률", "")))
        if rate is None:
            continue
        rates.append({"number": int(item["number"]), "rate": rate})
    return rates


def create_contact_sheet(output_dir: Path, count: int) -> Path:
    thumbs: list[Image.Image] = []
    for question in range(1, count + 1):
        image_path = output_dir / f"q{question:02d}.png"
        if not image_path.exists():
            continue
        image = Image.open(image_path).convert("RGB")
        image.thumbnail((360, 520))
        tile = Image.new("RGB", (380, 560), "white")
        draw = ImageDraw.Draw(tile)
        draw.text((8, 6), f"q{question:02d}", fill=(180, 0, 0))
        tile.paste(image, (10, 30))
        thumbs.append(tile)

    cols = 4
    rows = max(1, (len(thumbs) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * 380, rows * 560), (245, 245, 245))
    for index, tile in enumerate(thumbs):
        sheet.paste(tile, ((index % cols) * 380, (index // cols) * 560))

    contact_path = output_dir / "contact_sheet.jpg"
    sheet.save(contact_path, quality=90)
    return contact_path


def create_zip(job_dir: Path, output_dir: Path) -> Path:
    zip_path = job_dir / "question_images.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output_dir.glob("q*.png")):
            archive.write(path, arcname=path.name)
        for extra in ("manifest.json", "contact_sheet.jpg"):
            extra_path = output_dir / extra
            if extra_path.exists():
                archive.write(extra_path, arcname=extra)
    return zip_path


def write_questions_manifest(output_dir: Path, items: list[dict[str, object]]) -> Path:
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest_path


def rebuild_questions_manifest(
    output_dir: Path, source_overrides: dict[str, str] | None = None
) -> list[dict[str, object]]:
    source_overrides = source_overrides or {}
    items: list[dict[str, object]] = []
    for path in sorted(output_dir.glob("q*.png")):
        try:
            number = int(path.stem.replace("q", ""))
        except ValueError:
            continue
        with Image.open(path) as image:
            width, height = image.size
        items.append(
            {
                "question": number,
                "file": path.name,
                "source": source_overrides.get(path.name, path.name),
                "width": width,
                "height": height,
            }
        )
    write_questions_manifest(output_dir, items)
    return items


def save_uploaded_question_images(files: list, job_dir: Path) -> dict[str, object]:
    if not files:
        raise ValueError("문항 이미지 파일을 선택해주세요.")

    output_dir = job_dir / "questions"
    output_dir.mkdir(parents=True, exist_ok=True)
    for old_path in output_dir.glob("q*.png"):
        old_path.unlink()
    for extra in ("manifest.json", "contact_sheet.jpg"):
        extra_path = output_dir / extra
        if extra_path.exists():
            extra_path.unlink()

    items: list[dict[str, object]] = []
    ordered_files = sorted(
        [file for file in files if file and file.filename],
        key=lambda file: file.filename.lower(),
    )
    if not ordered_files:
        raise ValueError("문항 이미지 파일을 선택해주세요.")

    for index, uploaded in enumerate(ordered_files, start=1):
        source_suffix = uploaded_suffix(uploaded.filename)
        source_name = safe_upload_filename(
            uploaded.filename, f"question_{index}.png", source_suffix or ".png"
        )
        if source_suffix not in IMAGE_EXTENSIONS:
            raise ValueError("PNG, JPG, WEBP 등 이미지 파일만 처리할 수 있습니다.")

        output_path = output_dir / f"q{index:02d}.png"
        try:
            image = Image.open(uploaded.stream)
            image = ImageOps.exif_transpose(image).convert("RGB")
        except Exception as exc:
            raise ValueError(f"{uploaded.filename} 이미지를 읽지 못했습니다: {exc}") from exc
        image.save(output_path)
        items.append(
            {
                "question": index,
                "file": output_path.name,
                "source": uploaded.filename,
                "width": image.width,
                "height": image.height,
            }
        )

    write_questions_manifest(output_dir, items)
    contact_path = create_contact_sheet(output_dir, len(items))
    zip_path = create_zip(job_dir, output_dir)
    return {
        "output_dir": output_dir,
        "count": len(items),
        "manifest": items,
        "contact_path": contact_path,
        "zip_path": zip_path,
    }


def save_single_question_image(uploaded, job_dir: Path, question_number: int) -> dict[str, object]:
    if not uploaded or not uploaded.filename:
        raise ValueError("문항 이미지 파일을 선택해주세요.")
    if question_number < 1 or question_number > 200:
        raise ValueError("문항 번호를 확인해주세요.")

    source_suffix = uploaded_suffix(uploaded.filename)
    source_name = safe_upload_filename(
        uploaded.filename, f"question_{question_number}.png", source_suffix or ".png"
    )
    if source_suffix not in IMAGE_EXTENSIONS:
        raise ValueError("PNG, JPG, WEBP 등 이미지 파일만 처리할 수 있습니다.")

    output_dir = job_dir / "questions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"q{question_number:02d}.png"
    try:
        image = Image.open(uploaded.stream)
        image = ImageOps.exif_transpose(image).convert("RGB")
    except Exception as exc:
        raise ValueError(f"{uploaded.filename} 이미지를 읽지 못했습니다: {exc}") from exc

    image.save(output_path)
    items = rebuild_questions_manifest(output_dir, {output_path.name: uploaded.filename})
    if not items:
        raise ValueError("문항 이미지 파일을 저장하지 못했습니다.")
    contact_path = create_contact_sheet(output_dir, max(int(item["question"]) for item in items))
    zip_path = create_zip(job_dir, output_dir)
    return {
        "output_dir": output_dir,
        "count": len(items),
        "manifest": items,
        "contact_path": contact_path,
        "zip_path": zip_path,
    }


def question_payload(job_id: str, output_dir: Path) -> list[dict[str, str | int]]:
    items: list[dict[str, str | int]] = []
    for path in sorted(output_dir.glob("q*.png")):
        number = int(path.stem.replace("q", ""))
        items.append(
            {
                "number": number,
                "name": path.name,
                "url": f"/runs/{job_id}/questions/{path.name}",
            }
        )
    return items


def mime_type_from_image_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix in {".webp"}:
        return "image/webp"
    if suffix in {".bmp"}:
        return "image/bmp"
    if suffix in {".tif", ".tiff"}:
        return "image/tiff"
    return GEMINI_DEFAULT_MIME


def encode_image_for_gemini(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def normalize_gemini_model(value: str | None) -> str:
    model = clean_text(value) or GEMINI_DEFAULT_MODEL
    return GEMINI_MODEL_ALIASES.get(model, model)


def list_gemini_generate_content_models(api_key: str) -> list[str]:
    request = urllib.request.Request(
        GEMINI_MODELS_LIST_URL,
        method="GET",
        headers={"x-goog-api-key": api_key},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    models = payload.get("models") if isinstance(payload, dict) else []
    if not isinstance(models, list):
        return []

    names: list[str] = []
    for item in models:
        if not isinstance(item, dict):
            continue
        methods = item.get("supportedGenerationMethods") or item.get("supported_actions") or []
        if "generateContent" not in methods:
            continue
        name = clean_text(str(item.get("name") or item.get("baseModelId") or ""))
        if name.startswith("models/"):
            name = name.removeprefix("models/")
        if name and name not in names:
            names.append(name)
    return names


def get_gemini_model_candidates(model: str, api_key: str | None = None) -> list[str]:
    normalized = clean_text(normalize_gemini_model(model))
    original = clean_text(model)
    candidates = [normalized, original]

    if "flash" in normalized:
        candidates.extend(
            [
                "gemini-3-flash-preview",
                "gemini-flash-latest",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
            ]
        )
    elif "pro" in normalized:
        candidates.extend(
            [
                "gemini-3.1-pro-preview",
                "gemini-3-pro-preview",
                "gemini-pro-latest",
                "gemini-2.5-pro",
                "gemini-3-flash-preview",
            ]
        )
    candidates.extend(GEMINI_PREFERRED_MODEL_ORDER)

    available_models: list[str] = []
    if api_key:
        try:
            available_models = list_gemini_generate_content_models(api_key)
        except Exception:
            available_models = []

    if available_models:
        available_set = set(available_models)
        candidates = [candidate for candidate in candidates if candidate in available_set]
        for preferred in GEMINI_PREFERRED_MODEL_ORDER:
            if preferred in available_set:
                candidates.append(preferred)
        candidates.extend(available_models[:12])

    seen = []
    for candidate in candidates:
        if candidate and candidate not in seen:
            seen.append(candidate)
    return seen


def request_gemini_solution(
    image_path: Path,
    api_key: str,
    model: str,
    prompt: str,
    timeout_seconds: int = GEMINI_API_TIMEOUT_SECONDS,
) -> tuple[str, list[str]]:
    target_model_candidates = get_gemini_model_candidates(model, api_key=api_key)
    request_prompt = clean_text(prompt) or GEMINI_DEFAULT_PROMPT
    request_body = json.dumps(
        {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": request_prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type_from_image_path(image_path),
                                "data": encode_image_for_gemini(image_path),
                            }
                        },
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 8192,
                "responseMimeType": "application/json",
            },
        }
    ).encode("utf-8")

    last_http_error: tuple[int | None, str] | None = None
    attempt_hints: list[str] = []
    last_exception: Exception | None = None

    for target_model in target_model_candidates:
        quoted_model = urllib.parse.quote(target_model)
        for template in GEMINI_REQUEST_PATHS:
            request_url = template.format(model=quoted_model)
            attempt_label = build_gemini_attempt_label(target_model, request_url)
            request = urllib.request.Request(
                request_url,
                data=request_body,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key,
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                    response_bytes = response.read()
            except urllib.error.HTTPError as exc:
                last_exception = exc
                body = ""
                try:
                    body = exc.read().decode("utf-8", errors="ignore")
                    payload = parse_gemini_http_error_body(body)
                    status = exc.code
                    code, hint = classify_gemini_api_error(payload["message"], status, payload["status"])
                    suffix = f" | {hint}" if hint else ""
                    message = payload["message"] or body
                    if not message:
                        message = str(exc.reason or exc)
                    detail = f"{code} {message}" if code else message
                    if payload["status"] and payload["status"] != "" and payload["status"] not in detail:
                        detail = f"{detail} (status={payload['status']})"
                    detail = detail or str(exc.reason or exc)
                    attempt_hints.append(f"{attempt_label}: {status} {detail}{suffix}")
                    last_http_error = (status, f"Gemini API 오류 ({status}): {detail}{suffix}")
                    continue
                except (OSError, ValueError):
                    message = body if body else str(exc.reason or exc)
                    code, hint = classify_gemini_api_error(message, exc.code, "")
                    suffix = f" | {hint}" if hint else ""
                    attempt_hints.append(f"{attempt_label}: {exc.code} {message}{suffix}")
                    last_http_error = (exc.code, f"Gemini API 오류 ({exc.code}): {message}{suffix}")
                    continue
            except urllib.error.URLError as exc:
                message = str(exc.reason)
                last_exception = exc
                attempt_hints.append(f"{attempt_label}: {message}")
                last_http_error = (0, f"Gemini API 요청 실패: {message}")
                continue
            else:
                attempt_hints.append(f"{attempt_label}: 성공")
                break
        else:
            continue
        break
    else:
        if last_http_error:
            status_code, base_message = last_http_error
            if attempt_hints:
                attempts = " / ".join(attempt_hints)
                return_error = f"{base_message} | 시도 목록: {attempts}"
            else:
                return_error = f"{base_message} | 시도 로그 없음"
            if last_exception:
                return_error = f"{return_error} ({type(last_exception).__name__})"
            raise GeminiRequestError(return_error, attempt_hints)
        raise GeminiRequestError("Gemini API 요청 실패: 사용 가능한 모델/엔드포인트를 찾지 못했습니다.", attempt_hints)

    try:
        response_payload = json.loads(response_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini 응답을 JSON으로 해석하지 못했습니다.") from exc

    try:
        candidates = response_payload.get("candidates")
        if not candidates:
            raise RuntimeError("Gemini 응답에 생성 결과가 없습니다.")

        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            text = part.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip(), attempt_hints

        raise RuntimeError("Gemini 응답에서 텍스트 본문을 찾지 못했습니다.")
    except RuntimeError:
        raise


def call_gemini_for_question(
    image_path: Path,
    api_key: str,
    model: str,
    prompt: str,
    question_number: int,
) -> tuple[dict[str, str], list[str]]:
    attempt_traces: list[str] = []
    parsed: dict[str, object] | None = None
    raw_text = ""
    last_error: Exception | None = None
    for api_attempt in range(1, GEMINI_MAX_ATTEMPTS_PER_QUESTION + 1):
        timeout_seconds = GEMINI_API_TIMEOUT_SECONDS if api_attempt == 1 else GEMINI_RETRY_TIMEOUT_SECONDS
        try:
            for strict in (False, True):
                request_prompt = build_gemini_prompt(prompt, question_number, strict=strict)
                raw_text, attempts = request_gemini_solution(
                    image_path=image_path,
                    api_key=api_key,
                    model=model,
                    prompt=request_prompt,
                    timeout_seconds=timeout_seconds,
                )
                attempt_prefix = f"요청 {api_attempt}/{GEMINI_MAX_ATTEMPTS_PER_QUESTION}, 제한 {timeout_seconds}s"
                attempt_traces.extend([f"{attempt_prefix}: {attempt}" for attempt in attempts])
                parsed = clean_json_from_text(raw_text)
                if parsed:
                    break
                if not strict:
                    attempt_traces.append(f"문항 {question_number}번: JSON 파싱 실패 - 보강 프롬프트로 1회 재시도")
                else:
                    attempt_traces.append(f"문항 {question_number}번: JSON 파싱 실패 - 실패 처리")
            if parsed:
                break
            last_error = RuntimeError(f"Gemini 출력이 JSON 형식을 지키지 않았습니다.\n원문: {raw_text[:1200]}")
        except Exception as exc:
            last_error = exc
            message = str(exc)
            if "timed out" in message.lower() and api_attempt < GEMINI_MAX_ATTEMPTS_PER_QUESTION:
                attempt_traces.append(
                    f"문항 {question_number}번: 읽기 제한 {timeout_seconds}s 초과 - 재시도"
                )
                time.sleep(1.5 * api_attempt)
                continue
            raise

    if not parsed:
        if last_error:
            raise last_error
        raise RuntimeError(f"Gemini 출력이 JSON 형식을 지키지 않았습니다.\n원문: {raw_text[:1200]}")
    normalized = normalize_gemini_fields(parsed, question_number)
    question_label = parse_question_number(normalized.get("문항 번호"))
    if question_label is not None:
        normalized["문항 번호"] = str(question_label)
        return normalized, attempt_traces

    normalized["문항 번호"] = str(question_number)
    return normalized, attempt_traces


def build_auto_cut_input(
    subject: str, solutions: list[dict[str, object]]
) -> tuple[dict[str, object] | None, list[float], list[str]]:
    model_payload = model_public_payload()
    subject_points = model_payload.get("default_points", {})
    points = subject_points.get(subject)
    if not isinstance(points, list) or len(points) != 20:
        return None, [], [f"{subject} 기본 배점 정보를 불러오지 못했습니다."]

    solution_map = {int(item["number"]): item for item in solutions if isinstance(item.get("number"), int)}
    rates = []
    missing: list[int] = []
    for index in range(1, 21):
        item = solution_map.get(index, {})
        field = item.get("fields")
        if not isinstance(field, dict):
            missing.append(index)
            continue
        value = parse_rate_percent(str(field.get("예상 정답률", "")))
        if value is None:
            missing.append(index)
            continue
        rates.append(float(value))

    if missing:
        return None, rates, [f"문항 {', '.join(map(str, missing))}의 정답률을 채우지 못해 컷 예측을 건너뜁니다."]

    if len(rates) != 20:
        return None, rates, ["정답률이 20개 미완료되어 컷 예측을 건너뜁니다."]

    payload = {
        "subject": subject,
        "mode": "national",
        "rates": rates,
        "points": points,
    }
    return payload, rates, []


def write_log_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_gemini_auto_generation(
    job_id: str,
    job_dir: Path,
    output_dir: Path,
    subject: str,
    api_key: str,
    model: str,
    prompt: str,
    max_requests: int,
    max_concurrency: int = 1,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> tuple[dict[str, object], dict[str, object] | None, dict[str, object] | None]:
    model = normalize_gemini_model(model)
    subject_name = normalize_subject(subject)
    image_paths = sorted(output_dir.glob("q*.png"))
    base_prompt = clean_text(prompt) or GEMINI_DEFAULT_PROMPT

    execution_log_path = job_dir / GEMINI_EXECUTION_LOG_FILENAME
    cut_log_path = job_dir / GEMINI_CUT_LOG_FILENAME
    solutions: list[dict[str, object]] = []

    log_payload: dict[str, object] = {
        "started_at": utcish_now(),
        "subject": subject_name,
        "model": model,
        "requested_count": max_requests,
        "max_concurrency": max_concurrency,
        "requests": [],
    }

    processed = 0
    success = 0
    failure = 0
    warnings: list[str] = []
    requested_images = list(enumerate(image_paths[:max_requests], start=1))
    requested_total = len(requested_images)
    max_workers = max(1, min(max_concurrency, requested_total or 1, 8))

    def process_one_question(index: int, image_path: Path) -> tuple[dict[str, object], dict[str, object], str | None]:
        question_number = parse_question_number(image_path.stem.replace("q", "")) or index
        request_entry: dict[str, object] = {
            "question_number": question_number,
            "image": image_path.name,
            "started_at": utcish_now(),
            "status": "pending",
            "prompt_preview": base_prompt[:400],
            "row": index,
        }
        if progress_callback:
            progress_callback(
                {
                    "type": "request_start",
                    "index": index,
                    "question_number": question_number,
                    "processed": 0,
                    "requested": requested_total,
                    "concurrency": max_workers,
                }
            )
        start_at = time.perf_counter()
        error_message = ""
        warning_message: str | None = None
        try:
            fields, attempts = call_gemini_for_question(
                image_path=image_path,
                api_key=api_key,
                model=model,
                prompt=base_prompt,
                question_number=question_number,
            )
            request_entry["attempts"] = attempts
            status = "ok"
        except Exception as exc:
            status = "error"
            warning_message = f"{question_number}번 처리 실패: {exc}"
            error_message = str(exc)
            request_entry["error_code"] = "GEMINI_REQUEST_ERROR"
            request_entry["status_text"] = "Gemini API 요청 실패"
            if isinstance(exc, GeminiRequestError):
                request_entry["attempts"] = exc.attempts
            fields = {
                "문항 번호": str(question_number),
                "정답": "",
                "예상 정답률": "",
                "예측 점수": "",
                "해설": f"Gemini 처리 오류: {exc}",
                "정답 풀이": "",
                "오답 풀이": "",
            }

        elapsed_ms = int((time.perf_counter() - start_at) * 1000)
        request_entry["status"] = status
        request_entry["elapsed_ms"] = elapsed_ms
        if status == "ok":
            request_entry["answer"] = fields.get("정답")
            request_entry["predicted_score"] = fields.get("예측 점수")
        else:
            request_entry["error"] = error_message or "알 수 없는 오류"

        solution_entry = {
            "number": question_number,
            "label": fields.get("문항 번호") or str(question_number),
            "row": index,
            "fields": fields,
        }
        return request_entry, solution_entry, warning_message

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_one_question, index, image_path)
            for index, image_path in requested_images
        ]
        for future in as_completed(futures):
            request_entry, solution_entry, warning_message = future.result()
            log_payload["requests"].append(request_entry)
            solutions.append(solution_entry)
            if request_entry.get("status") == "ok":
                success += 1
            else:
                failure += 1
                if warning_message:
                    warnings.append(warning_message)
            processed += 1
            if progress_callback:
                progress_callback(
                    {
                        "type": "request_done",
                        "index": int(request_entry.get("row") or processed),
                        "question_number": request_entry.get("question_number"),
                        "processed": processed,
                        "requested": requested_total,
                        "status": request_entry.get("status"),
                        "answer": request_entry.get("answer"),
                        "error": request_entry.get("error"),
                    }
                )

    log_payload["requests"].sort(key=lambda item: int(item.get("question_number") or 0))

    normalized = normalize_solution_rows(solutions)

    if normalized:
        csv_path = write_solutions_csv(
            job_dir,
            AUTO_GENERATED_SOLUTION_COLUMNS,
            normalized,
            filename=GEMINI_GENERATED_CSV,
        )
        execution_output_path = str(csv_path)
    else:
        execution_output_path = str(job_dir / GEMINI_GENERATED_CSV)
        write_solutions_csv(
            job_dir,
            AUTO_GENERATED_SOLUTION_COLUMNS,
            [],
            filename=GEMINI_GENERATED_CSV,
        )
        execution_output_path = str(job_dir / GEMINI_GENERATED_CSV)

    log_payload["completed_at"] = utcish_now()
    log_payload["processed_count"] = processed
    log_payload["success_count"] = success
    log_payload["failure_count"] = failure
    log_payload["warnings"] = warnings
    write_log_json(execution_log_path, log_payload)

    payload, rates, cut_warnings = build_auto_cut_input(subject_name, normalized)
    cut_result: dict[str, object] | None = None
    if payload:
        try:
            cut_result = predict_cut(
                subject=payload["subject"],
                mode=payload["mode"],
                rates=payload["rates"],
                points=payload["points"],
            )
            write_log_json(
                cut_log_path,
                {
                    "started_at": utcish_now(),
                    "subject": subject_name,
                    "input": payload,
                    "status": "success",
                    "result": cut_result,
                    "rates": rates,
                    "warnings": [],
                },
            )
        except Exception as exc:
            write_log_json(
                cut_log_path,
                {
                    "started_at": utcish_now(),
                    "subject": subject_name,
                    "status": "error",
                    "error": str(exc),
                },
            )
            warnings.extend([f"컷 예측 오류: {exc}"])
    else:
        write_log_json(
            cut_log_path,
            {
                "started_at": utcish_now(),
                "subject": subject_name,
                "status": "skipped",
                "input": payload,
                "rates": rates,
                "warnings": cut_warnings,
            },
        )
        warnings.extend(cut_warnings)

    solution_payload = build_solutions_payload(
        job_id,
        AUTO_GENERATED_SOLUTION_COLUMNS,
        normalized,
        "utf-8-sig",
        output_dir,
        default_columns=AUTO_GENERATED_SOLUTION_COLUMNS,
    )
    solution_payload["source"] = "gemini_auto_generated"
    summary = {
        "enabled": True,
        "subject": subject_name,
        "model": model,
        "prompt_preview": base_prompt[:400],
        "requested": min(max_requests, len(image_paths)),
        "concurrency": max_workers,
        "processed": processed,
        "success": success,
        "failure": failure,
        "solutions_path": execution_output_path,
        "execution_log_path": str(execution_log_path),
        "cut_log_path": str(cut_log_path),
        "warnings": warnings,
        "solutions_payload": solution_payload,
    }
    if "requests" in log_payload:
        summary["requests"] = log_payload.get("requests")
    if cut_result:
        summary["cut_result"] = cut_result
        summary["cut_payload"] = payload
    return summary, log_payload, cut_result


def image_job_payload(job_id: str, job_dir: Path, output_dir: Path, metadata: dict[str, object]):
    questions = question_payload(job_id, output_dir)
    return {
        **metadata,
        "job_id": job_id,
        "output_dir": str(output_dir),
        "count": len(questions),
        "questions": questions,
        "contact_sheet_url": f"/runs/{job_id}/questions/contact_sheet.jpg",
        "manifest_url": f"/runs/{job_id}/questions/manifest.json",
        "download_url": f"/download/{job_id}",
        "zip_path": str(job_dir / "question_images.zip"),
    }


def build_solutions_payload(
    job_id: str,
    fieldnames: list[str],
    solutions: list[dict[str, object]],
    encoding: str,
    output_dir: Path | None = None,
    default_columns: list[str] | None = None,
) -> dict[str, object]:
    solutions = normalize_solution_rows(solutions)
    solution_numbers = {int(item["number"]) for item in solutions}
    image_numbers = question_numbers(output_dir) if output_dir else set()
    return {
        "job_id": job_id,
        "count": len(solutions),
        "has_images": output_dir is not None,
        "encoding": encoding,
        "fieldnames": fieldnames,
        "default_columns": default_columns or SOLUTION_COLUMNS,
        "solutions": solutions,
        "questions": question_payload(job_id, output_dir) if output_dir else [],
        "cut_rates": solution_cut_rates(solutions),
        "missing_images": sorted(solution_numbers - image_numbers) if output_dir else [],
        "missing_solutions": sorted(image_numbers - solution_numbers),
    }


def write_solutions_csv(
    job_dir: Path,
    fieldnames: list[str],
    solutions: list[dict[str, object]],
    filename: str = "solutions_edited.csv",
) -> Path:
    csv_path = job_dir / filename
    normalized_fieldnames = list(fieldnames)
    if "문항 번호" not in normalized_fieldnames:
        normalized_fieldnames.insert(0, "문항 번호")

    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=normalized_fieldnames)
        writer.writeheader()
        for item in sorted(solutions, key=lambda row: int(row["number"])):
            fields = item.get("fields") if isinstance(item.get("fields"), dict) else {}
            row = {name: clean_text(str(fields.get(name, ""))) for name in normalized_fieldnames}
            row["문항 번호"] = row.get("문항 번호") or str(item["number"])
            writer.writerow(row)
    return csv_path


def normalize_solution_payload(payload: dict[str, object]) -> tuple[list[str], list[dict[str, object]]]:
    fieldnames = payload.get("fieldnames")
    if not isinstance(fieldnames, list) or not fieldnames:
        fieldnames = SOLUTION_COLUMNS
    fieldnames = [str(name) for name in fieldnames]

    normalized: list[dict[str, object]] = []
    for index, item in enumerate(payload.get("solutions", []), start=1):
        if not isinstance(item, dict):
            continue
        fields = item.get("fields")
        if not isinstance(fields, dict):
            fields = {}
        cleaned_fields = normalize_solution_fields(
            {name: clean_text(str(fields.get(name, ""))) for name in fieldnames}
        )
        raw_label = cleaned_fields.get("문항 번호") or str(item.get("label") or item.get("number") or index)
        number = parse_question_number(raw_label) or parse_question_number(str(item.get("number"))) or index
        cleaned_fields["문항 번호"] = raw_label
        normalized.append(
            {
                "number": number,
                "label": raw_label,
                "row": int(item.get("row") or index + 1),
                "fields": cleaned_fields,
            }
        )

    normalized.sort(key=lambda row: int(row["number"]))
    return fieldnames, normalized


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/design-system/<path:filename>")
def design_system_file(filename: str):
    return send_from_directory(DESIGN_DIR, filename)


@app.get("/runs/<path:filename>")
def run_file(filename: str):
    return send_from_directory(RUNS_DIR, filename)


@app.get("/api/cut-model")
def api_cut_model():
    return jsonify(model_public_payload())


@app.get("/api/historical-exams")
def api_historical_exams():
    return jsonify(historical_exam_payload())


@app.get("/api/question-search")
def api_question_search():
    if request.args.get("refresh") == "1":
        refresh_question_bank()
    return jsonify(search_question_bank(request.args))


@app.get("/api/question-image/<image_id>")
def api_question_image(image_id: str):
    path = question_image_path(image_id)
    if not path:
        return jsonify({"error": "문항 이미지를 찾지 못했습니다."}), 404
    return send_file(path)


@app.post("/api/cut-predict")
def api_cut_predict():
    payload = request.get_json(silent=True) or {}
    try:
        result = predict_cut(
            subject=str(payload.get("subject", "")),
            rates=payload.get("rates", []),
            points=payload.get("points", []),
            mode=str(payload.get("mode", "national")),
        )
    except PredictionError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(result)


@app.get("/download/<job_id>")
def download_job(job_id: str):
    zip_path = RUNS_DIR / job_id / "question_images.zip"
    if not zip_path.exists():
        return jsonify({"error": "ZIP 파일을 찾지 못했습니다."}), 404
    return send_file(zip_path, as_attachment=True, download_name=f"{job_id}_questions.zip")


@app.post("/api/solutions")
def upload_solutions_only():
    uploaded = request.files.get("csv")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "해설 CSV 파일을 선택해주세요."}), 400

    if uploaded_suffix(uploaded.filename) != ".csv":
        return jsonify({"error": "CSV 파일만 처리할 수 있습니다."}), 400
    filename = safe_upload_filename(uploaded.filename, "solutions.csv", ".csv")

    job_id = f"csv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    job_dir = RUNS_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    csv_path = job_dir / filename
    uploaded.save(csv_path)

    try:
        fieldnames, solutions, encoding = parse_solutions_csv(csv_path)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not solutions:
        return jsonify({"error": "문항 번호가 있는 해설 행을 찾지 못했습니다."}), 400

    payload = build_solutions_payload(job_id, fieldnames, solutions, encoding)
    (job_dir / "solutions.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (job_dir / "job.json").write_text(
        json.dumps(
            {
                "job_id": job_id,
                "input": str(csv_path),
                "count": len(solutions),
                "kind": "solutions_csv",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return jsonify(payload)


@app.post("/api/images")
def upload_images_only():
    files = request.files.getlist("images")
    job_id = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    job_dir = RUNS_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    try:
        image_result = save_uploaded_question_images(files, job_dir)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    metadata = {
        "input": "manual_images",
        "kind": "manual_images",
        "created_at": utcish_now(),
        "expected_questions": image_result["count"],
    }
    (job_dir / "job.json").write_text(
        json.dumps(
            {
                **metadata,
                "job_id": job_id,
                "output_dir": str(image_result["output_dir"]),
                "count": image_result["count"],
                "sources": [item["source"] for item in image_result["manifest"]],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return jsonify(image_job_payload(job_id, job_dir, image_result["output_dir"], metadata))


@app.post("/api/jobs/<job_id>/images")
def upload_job_images(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not job_dir.exists():
        return jsonify({"error": "작업을 찾지 못했습니다."}), 404

    files = request.files.getlist("images")
    question_number = parse_question_number(request.form.get("question_number"))
    try:
        if question_number and len([file for file in files if file and file.filename]) == 1:
            image_result = save_single_question_image(files[0], job_dir, question_number)
        else:
            image_result = save_uploaded_question_images(files, job_dir)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    metadata = {
        "input": "manual_images",
        "kind": "manual_images",
        "updated_at": utcish_now(),
        "expected_questions": image_result["count"],
    }
    job_meta_path = job_dir / "job.json"
    existing = {}
    if job_meta_path.exists():
        try:
            existing = json.loads(job_meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    job_meta_path.write_text(
        json.dumps(
            {
                **existing,
                **metadata,
                "job_id": job_id,
                "output_dir": str(image_result["output_dir"]),
                "count": image_result["count"],
                "sources": [item["source"] for item in image_result["manifest"]],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    solutions_path = job_dir / "solutions.json"
    if solutions_path.exists():
        try:
            saved = json.loads(solutions_path.read_text(encoding="utf-8"))
            fieldnames = saved.get("fieldnames") or SOLUTION_COLUMNS
            solutions = saved.get("solutions") or []
            if isinstance(fieldnames, list) and isinstance(solutions, list):
                payload = build_solutions_payload(
                    job_id,
                    [str(name) for name in fieldnames],
                    solutions,
                    str(saved.get("encoding") or "utf-8-sig"),
                    image_result["output_dir"],
                )
                solutions_path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
                )
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    return jsonify(image_job_payload(job_id, job_dir, image_result["output_dir"], metadata))


@app.post("/api/jobs/<job_id>/solutions")
def upload_job_solutions(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not job_dir.exists():
        return jsonify({"error": "작업을 찾지 못했습니다."}), 404
    output_dir = job_dir / "questions"

    uploaded = request.files.get("csv")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "해설 CSV 파일을 선택해주세요."}), 400

    if uploaded_suffix(uploaded.filename) != ".csv":
        return jsonify({"error": "CSV 파일만 처리할 수 있습니다."}), 400
    filename = safe_upload_filename(uploaded.filename, "solutions.csv", ".csv")

    csv_path = job_dir / "solutions.csv"
    uploaded.save(csv_path)

    try:
        fieldnames, solutions, encoding = parse_solutions_csv(csv_path)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not solutions:
        return jsonify({"error": "문항 번호가 있는 해설 행을 찾지 못했습니다."}), 400

    payload = build_solutions_payload(
        job_id,
        fieldnames,
        solutions,
        encoding,
        output_dir if output_dir.exists() else None,
    )
    (job_dir / "solutions.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return jsonify(payload)


@app.post("/api/jobs/<job_id>/solutions/edit")
def edit_job_solutions(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not job_dir.exists():
        return jsonify({"error": "작업을 찾지 못했습니다."}), 404

    payload = request.get_json(silent=True) or {}
    fieldnames, solutions = normalize_solution_payload(payload)
    if not solutions:
        return jsonify({"error": "저장할 해설 행을 찾지 못했습니다."}), 400

    output_dir = job_dir / "questions"
    output_dir_for_payload = output_dir if output_dir.exists() else None
    result = build_solutions_payload(
        job_id,
        fieldnames,
        solutions,
        str(payload.get("encoding") or "utf-8-sig"),
        output_dir_for_payload,
    )
    (job_dir / "solutions.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    edited_csv = write_solutions_csv(job_dir, fieldnames, solutions)
    result["edited_csv_path"] = str(edited_csv)
    return jsonify(result)


@app.get("/api/jobs/<job_id>/solutions")
def get_job_solutions(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    solutions_path = job_dir / "solutions.json"
    if not solutions_path.exists():
        return jsonify({"error": "저장된 해설 CSV를 찾지 못했습니다."}), 404
    return send_file(solutions_path, mimetype="application/json")


@app.post("/api/jobs/<job_id>/archive")
def archive_job(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not job_dir.exists():
        return jsonify({"error": "작업을 찾지 못했습니다."}), 404

    payload = request.get_json(silent=True) or {}
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    archive_id = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    archive_dir = ARCHIVES_DIR / archive_id
    archive_dir.mkdir(parents=True)
    snapshot_dir = archive_dir / "job"
    shutil.copytree(job_dir, snapshot_dir)

    solutions_path = job_dir / "solutions.json"
    image_count = len(question_payload(job_id, job_dir / "questions")) if (job_dir / "questions").exists() else 0
    solution_count = 0
    if solutions_path.exists():
        try:
            solution_count = len(json.loads(solutions_path.read_text(encoding="utf-8")).get("solutions", []))
        except (json.JSONDecodeError, TypeError):
            solution_count = 0

    archive_payload = {
        "archive_id": archive_id,
        "job_id": job_id,
        "created_at": utcish_now(),
        "title": clean_text(str(metadata.get("title", ""))) or "제목 없음",
        "subject": clean_text(str(metadata.get("subject", ""))),
        "exam_date": clean_text(str(metadata.get("exam_date", ""))),
        "memo": clean_text(str(metadata.get("memo", ""))),
        "image_count": image_count,
        "solution_count": solution_count,
        "cut_payload": payload.get("cut_payload"),
        "cut_result": payload.get("cut_result"),
        "archive_dir": str(archive_dir),
        "snapshot_dir": str(snapshot_dir),
    }
    (archive_dir / "archive.json").write_text(
        json.dumps(archive_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    update_archive_index_item(archive_payload)
    return jsonify(archive_payload)


@app.get("/api/archives")
def list_archives():
    archives = read_archive_index()
    archives.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
    return jsonify({"archives": archives})


@app.patch("/api/archives/<archive_id>")
def update_archive(archive_id: str):
    try:
        payload = read_archive_payload(archive_id)
    except (ValueError, FileNotFoundError) as exc:
        return jsonify({"error": str(exc)}), 404

    request_payload = request.get_json(silent=True) or {}
    metadata = request_payload.get("metadata") if isinstance(request_payload.get("metadata"), dict) else {}
    for key in ("title", "subject", "exam_date", "memo"):
        if key in metadata:
            payload[key] = clean_text(str(metadata.get(key, "")))
    payload["updated_at"] = utcish_now()

    archive_metadata_path(archive_id).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    update_archive_index_item(payload)
    return jsonify(payload)


@app.post("/api/archives/<archive_id>/open")
def open_archive_folder(archive_id: str):
    try:
        archive_dir = safe_archive_dir(archive_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not archive_dir.exists():
        return jsonify({"error": "아카이브를 찾지 못했습니다."}), 404
    subprocess.Popen(["open", str(archive_dir)])
    return jsonify({"ok": True, "archive_dir": str(archive_dir)})


@app.post("/api/archives/<archive_id>/load")
def load_archive(archive_id: str):
    try:
        archive_payload = read_archive_payload(archive_id)
        archive_dir = safe_archive_dir(archive_id)
    except (ValueError, FileNotFoundError) as exc:
        return jsonify({"error": str(exc)}), 404

    snapshot_dir = archive_dir / "job"
    if not snapshot_dir.exists():
        return jsonify({"error": "아카이브 스냅샷을 찾지 못했습니다."}), 404

    job_id = f"load_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    job_dir = RUNS_DIR / job_id
    shutil.copytree(snapshot_dir, job_dir)

    output_dir = job_dir / "questions"
    job_payload: dict[str, object] = {
        "job_id": job_id,
        "input": "archive",
        "kind": "loaded_archive",
        "archive_id": archive_id,
        "count": 0,
        "questions": [],
        "download_url": f"/download/{job_id}",
        "manifest_url": "",
    }
    if output_dir.exists():
        job_payload.update(
            image_job_payload(
                job_id,
                job_dir,
                output_dir,
                {
                    "input": "archive",
                    "kind": "loaded_archive",
                    "archive_id": archive_id,
                    "loaded_at": utcish_now(),
                },
            )
        )

    solutions_payload = None
    solutions_path = job_dir / "solutions.json"
    if solutions_path.exists():
        try:
            saved = json.loads(solutions_path.read_text(encoding="utf-8"))
            fieldnames = [str(name) for name in (saved.get("fieldnames") or SOLUTION_COLUMNS)]
            solutions = saved.get("solutions") or []
            if isinstance(solutions, list):
                solutions_payload = build_solutions_payload(
                    job_id,
                    fieldnames,
                    solutions,
                    str(saved.get("encoding") or "utf-8-sig"),
                    output_dir if output_dir.exists() else None,
                )
                solutions_path.write_text(
                    json.dumps(solutions_payload, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
        except (json.JSONDecodeError, TypeError, ValueError):
            solutions_payload = None

    (job_dir / "job.json").write_text(
        json.dumps(
            {
                **job_payload,
                "loaded_from_archive": archive_id,
                "loaded_at": utcish_now(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return jsonify({"archive": archive_payload, "job": job_payload, "solutions": solutions_payload})


@app.delete("/api/archives/<archive_id>")
def delete_archive(archive_id: str):
    try:
        archive_dir = safe_archive_dir(archive_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if archive_dir.exists():
        shutil.rmtree(archive_dir)
    items = [
        item
        for item in read_archive_index()
        if not (isinstance(item, dict) and item.get("archive_id") == archive_id)
    ]
    write_archive_index(items)
    return jsonify({"ok": True})


@app.get("/api/gemini-defaults")
def api_gemini_defaults():
    settings = load_local_settings()
    configured_model = configured_setting_text(settings, "gemini_model", "GEMINI_MODEL") or GEMINI_DEFAULT_MODEL
    prompt = configured_setting_text(settings, "gemini_prompt", "GEMINI_PROMPT") or GEMINI_DEFAULT_PROMPT
    return jsonify(
        {
            "has_api_key": bool(configured_setting_text(settings, "gemini_api_key", "GEMINI_API_KEY")),
            "subject": normalize_subject(
                configured_setting_text(settings, "gemini_subject", "GEMINI_SUBJECT") or "한국지리"
            ),
            "model": normalize_gemini_model(configured_model),
            "max_requests": clean_int(
                configured_setting_text(settings, "gemini_max_requests", "GEMINI_MAX_REQUESTS"),
                GEMINI_DEFAULT_MAX_REQUESTS,
                1,
                20,
            ),
            "concurrency": clean_int(
                configured_setting_text(settings, "gemini_concurrency", "GEMINI_CONCURRENCY"),
                2 if "pro" in normalize_gemini_model(configured_model).lower() else GEMINI_DEFAULT_CONCURRENCY,
                1,
                5,
            ),
            "prompt": prompt,
        }
    )


def prepare_split_job_request() -> dict[str, object]:
    uploaded = request.files.get("pdf")
    if not uploaded or not uploaded.filename:
        raise ApiRequestError(
            {
                "error": "PDF 파일을 선택해주세요.",
                "error_code": "MISSING_PDF",
                "error_stage": "INPUT_VALIDATION",
            },
            400,
        )

    if uploaded_suffix(uploaded.filename) != ".pdf":
        raise ApiRequestError(
            {
                "error": "PDF 파일만 처리할 수 있습니다.",
                "error_code": "INVALID_FILE_TYPE",
                "error_stage": "INPUT_VALIDATION",
            },
            400,
        )
    filename = safe_upload_filename(uploaded.filename, "exam.pdf", ".pdf")

    expected = clean_int(request.form.get("expected_questions"), 20, 1, 200)
    dpi = clean_int(request.form.get("dpi"), 240, 120, 400)
    strip_final_notes = request.form.get("strip_final_notes") == "on"
    run_gemini_auto = request.form.get("run_gemini_auto") == "on"
    local_settings = load_local_settings()
    gemini_subject = normalize_subject(
        clean_text(request.form.get("gemini_subject"))
        or configured_setting_text(local_settings, "gemini_subject", "GEMINI_SUBJECT")
        or "한국지리"
    )
    gemini_api_key = clean_text(request.form.get("gemini_api_key")) or configured_setting_text(
        local_settings, "gemini_api_key", "GEMINI_API_KEY"
    )
    gemini_model = normalize_gemini_model(
        request.form.get("gemini_model")
        or configured_setting_text(local_settings, "gemini_model", "GEMINI_MODEL")
    )
    gemini_prompt = clean_text(request.form.get("gemini_prompt")) or configured_setting_text(
        local_settings, "gemini_prompt", "GEMINI_PROMPT"
    )
    max_gemini_requests = min(
        clean_int(request.form.get("gemini_max_requests"), GEMINI_DEFAULT_MAX_REQUESTS, 1, expected),
        expected,
    )
    requested_concurrency = clean_int(
        request.form.get("gemini_concurrency")
        or configured_setting_text(local_settings, "gemini_concurrency", "GEMINI_CONCURRENCY"),
        GEMINI_DEFAULT_CONCURRENCY,
        1,
        5,
    )
    gemini_concurrency = requested_concurrency
    if "pro" in gemini_model.lower():
        gemini_concurrency = min(gemini_concurrency, 2)

    job_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    job_dir = RUNS_DIR / job_id
    output_dir = job_dir / "questions"
    job_dir.mkdir(parents=True, exist_ok=True)
    input_path = job_dir / filename
    uploaded.save(input_path)

    return {
        "job_id": job_id,
        "job_dir": job_dir,
        "output_dir": output_dir,
        "input_path": input_path,
        "expected": expected,
        "dpi": dpi,
        "strip_final_notes": strip_final_notes,
        "run_gemini_auto": run_gemini_auto,
        "gemini_subject": gemini_subject,
        "gemini_api_key": gemini_api_key,
        "gemini_model": gemini_model,
        "gemini_prompt": gemini_prompt,
        "max_gemini_requests": max_gemini_requests,
        "gemini_concurrency": gemini_concurrency,
    }


def execute_split_job(params: dict[str, object], emit_progress: bool = False) -> dict[str, object]:
    job_id = str(params["job_id"])
    job_dir = Path(params["job_dir"])
    output_dir = Path(params["output_dir"])
    input_path = Path(params["input_path"])
    expected = int(params["expected"])
    dpi = int(params["dpi"])
    strip_final_notes = bool(params["strip_final_notes"])
    run_gemini_auto = bool(params["run_gemini_auto"])
    gemini_subject = str(params["gemini_subject"])
    gemini_api_key = str(params["gemini_api_key"])
    gemini_model = str(params["gemini_model"])
    gemini_prompt = str(params["gemini_prompt"])
    max_gemini_requests = int(params["max_gemini_requests"])
    gemini_concurrency = int(params.get("gemini_concurrency") or 1)

    def progress(
        stage: str,
        message: str,
        percent: int,
        level: str = "info",
        status: str = "running",
    ) -> None:
        if emit_progress:
            append_job_progress(
                job_id,
                job_dir,
                status=status,
                stage=stage,
                message=message,
                progress=percent,
                level=level,
            )

    progress("PDF_SPLIT", "PDF 문항 분할 중", 10)
    try:
        manifest = split_pdf(
            pdf_path=input_path,
            output_dir=output_dir,
            expected_questions=expected,
            dpi=dpi,
            make_debug=True,
            strip_final_notes=strip_final_notes,
        )
    except SystemExit as exc:
        raise ApiRequestError(
            {
                "error": str(exc),
                "job_id": job_id,
                "debug_url": f"/runs/{job_id}/questions/_debug",
                "error_code": "SPLIT_PDF_EXIT",
                "error_stage": "PDF_SPLIT",
            },
            422,
        )
    except Exception as exc:  # pragma: no cover - surfaced to local UI
        raise ApiRequestError(
            {
                "error": f"처리 중 오류가 발생했습니다: {exc}",
                "error_code": "SPLIT_EXCEPTION",
                "error_stage": "PDF_SPLIT",
                "job_id": job_id,
            },
            500,
        )

    progress("PDF_SPLIT", f"문항 분할 완료: {len(manifest)}개", 28, "success")
    progress("OUTPUT", "미리보기와 ZIP 생성 중", 32)
    contact_path = create_contact_sheet(output_dir, max(question_numbers(output_dir) or {len(manifest)}))
    zip_path = create_zip(job_dir, output_dir)
    progress("OUTPUT", "문항 이미지 저장 완료", 34, "success")

    auto_generation = None
    if run_gemini_auto:
        if not gemini_api_key:
            progress("GEMINI", "Gemini API 키가 비어 있어 자동 해설 생성을 건너뜀", 36, "warning")
            auto_generation = {
                "enabled": False,
                "error": "Gemini API 키가 비어 있어 자동 해설 생성을 건너뜁니다.",
                "error_code": "GEMINI_MISSING_API_KEY",
                "subject": gemini_subject,
                "model": gemini_model,
                "requested": max_gemini_requests,
                "concurrency": gemini_concurrency,
                "processed": 0,
                "success": 0,
                "failure": 0,
                "warnings": ["Gemini API 키가 비어 있습니다."],
            }
        else:
            try:
                progress("GEMINI", "Gemini 모델 확인 및 문항별 해설 생성 시작", 35)
                auto_summary, _, _ = run_gemini_auto_generation(
                    job_id=job_id,
                    job_dir=job_dir,
                    output_dir=output_dir,
                    subject=gemini_subject,
                    api_key=gemini_api_key,
                    model=gemini_model,
                    prompt=gemini_prompt or GEMINI_DEFAULT_PROMPT,
                    max_requests=max_gemini_requests,
                    max_concurrency=gemini_concurrency,
                    progress_callback=progress_callback_for_job(
                        job_id,
                        job_dir,
                        min(max_gemini_requests, len(question_numbers(output_dir))),
                    ) if emit_progress else None,
                )
                auto_generation = auto_summary
                if auto_generation.get("solutions_payload"):
                    (job_dir / "solutions.json").write_text(
                        json.dumps(auto_generation["solutions_payload"], ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                auto_generation["auto_generated_solutions_url"] = (
                    f"/runs/{job_id}/{GEMINI_GENERATED_CSV}"
                )
                auto_generation["gemini_execution_log_url"] = (
                    f"/runs/{job_id}/{GEMINI_EXECUTION_LOG_FILENAME}"
                )
                auto_generation["predicted_cut_log_url"] = (
                    f"/runs/{job_id}/{GEMINI_CUT_LOG_FILENAME}"
                )
                progress(
                    "GEMINI",
                    f"Gemini 자동 생성 완료: 성공 {auto_generation.get('success', 0)}개 / 실패 {auto_generation.get('failure', 0)}개",
                    96,
                    "success" if not auto_generation.get("failure") else "warning",
                )
            except Exception as exc:
                progress("GEMINI", f"Gemini 자동 처리 실패: {exc}", 96, "error")
                auto_generation = {
                    "enabled": False,
                    "error": str(exc),
                    "error_code": "GEMINI_AUTO_ERROR",
                    "subject": gemini_subject,
                    "model": gemini_model,
                    "requested": max_gemini_requests,
                    "concurrency": gemini_concurrency,
                    "processed": 0,
                    "success": 0,
                    "failure": 0,
                    "warnings": [f"Gemini 자동 처리 실패: {exc}"],
                }

    if auto_generation:
        auto_generation.setdefault("enabled", True)

    progress("OUTPUT", "작업 결과 정리 중", 98)
    metadata = {
        "job_id": job_id,
        "input": str(input_path),
        "output_dir": str(output_dir),
        "count": len(manifest),
        "dpi": dpi,
        "expected_questions": expected,
        "gemini_auto_generation": auto_generation,
    }
    (job_dir / "job.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    response_payload = {
        **metadata,
        "questions": question_payload(job_id, output_dir),
        "contact_sheet_url": f"/runs/{job_id}/questions/{contact_path.name}",
        "manifest_url": f"/runs/{job_id}/questions/manifest.json",
        "download_url": f"/download/{job_id}",
        "zip_path": str(zip_path),
    }
    if auto_generation:
        response_payload["auto_generation"] = auto_generation

    result_file(job_dir).write_text(
        json.dumps(response_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return response_payload


def run_split_job_background(params: dict[str, object]) -> None:
    job_id = str(params["job_id"])
    job_dir = Path(params["job_dir"])
    try:
        execute_split_job(params, emit_progress=True)
        append_job_progress(
            job_id,
            job_dir,
            status="completed",
            stage="COMPLETE",
            message="작업 완료",
            progress=100,
            level="success",
        )
    except ApiRequestError as exc:
        payload = {**exc.payload, "status": exc.status_code}
        error_file(job_dir).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        append_job_progress(
            job_id,
            job_dir,
            status="failed",
            stage=str(payload.get("error_stage") or "FAILED"),
            message=str(payload.get("error") or exc),
            progress=100,
            level="error",
        )
    except Exception as exc:  # pragma: no cover - surfaced to local UI
        payload = {
            "error": f"처리 중 오류가 발생했습니다: {exc}",
            "error_code": "BACKGROUND_EXCEPTION",
            "error_stage": "BACKGROUND_JOB",
            "job_id": job_id,
            "status": 500,
        }
        error_file(job_dir).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        append_job_progress(
            job_id,
            job_dir,
            status="failed",
            stage="BACKGROUND_JOB",
            message=payload["error"],
            progress=100,
            level="error",
        )


@app.post("/api/split/start")
def api_split_start():
    try:
        params = prepare_split_job_request()
    except ApiRequestError as exc:
        return jsonify(exc.payload), exc.status_code

    job_id = str(params["job_id"])
    job_dir = Path(params["job_dir"])
    append_job_progress(
        job_id,
        job_dir,
        status="queued",
        stage="UPLOAD",
        message="PDF 업로드 저장 완료",
        progress=5,
        level="success",
    )
    thread = threading.Thread(target=run_split_job_background, args=(params,), daemon=True)
    thread.start()
    return jsonify(
        {
            "job_id": job_id,
            "status": "queued",
            "status_url": f"/api/jobs/{job_id}/status",
        }
    ), 202


@app.get("/api/jobs/<job_id>/status")
def api_job_status(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    progress_payload = read_json_file(progress_file(job_dir)) or {
        "job_id": job_id,
        "status": "unknown",
        "stage": "UNKNOWN",
        "message": "작업 상태를 찾지 못했습니다.",
        "progress": 0,
        "events": [],
    }
    result_payload = read_json_file(result_file(job_dir))
    if result_payload:
        progress_payload["status"] = "completed"
        progress_payload["progress"] = 100
        progress_payload["result"] = result_payload
    error_payload = read_json_file(error_file(job_dir))
    if error_payload:
        progress_payload["status"] = "failed"
        progress_payload["progress"] = 100
        progress_payload["error"] = error_payload
    return jsonify(progress_payload)


@app.post("/api/split")
def api_split():
    try:
        params = prepare_split_job_request()
        response_payload = execute_split_job(params, emit_progress=False)
    except ApiRequestError as exc:
        return jsonify(exc.payload), exc.status_code
    return jsonify(response_payload)


@app.post("/api/jobs/<job_id>/open")
def open_job_folder(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    target_dir = job_dir / "questions"
    if not target_dir.exists():
        target_dir = job_dir
    if not target_dir.exists():
        return jsonify({"error": "결과 폴더를 찾지 못했습니다."}), 404
    subprocess.Popen(["open", str(target_dir)])
    return jsonify({"ok": True, "output_dir": str(target_dir)})


@app.post("/api/jobs/<job_id>/delete")
def delete_job(job_id: str):
    try:
        job_dir = safe_job_dir(job_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not job_dir.exists():
        return jsonify({"ok": True})
    shutil.rmtree(job_dir)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5057, debug=False)
