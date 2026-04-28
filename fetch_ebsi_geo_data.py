#!/usr/bin/env python3
"""Fetch EBSi historical geography grade cuts and wrong-answer rates."""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


BASE_URL = "https://www.ebsi.co.kr"
SOURCE_URL = (
    "https://www.ebsi.co.kr/ebs/xip/xipa/"
    "retrievePastGrdCutWrongAnswerRate.ebs?tab=1"
)
SUBJECTS = ("한국지리", "세계지리")
SOCIAL_AREA_CODE = "5"
SOCIAL_GRADE_TAB_CODE = "4210,4209,4208,4207,4201,4202,4204,4205,4206"


def post(path: str, data: dict[str, object] | None = None, text: bool = False):
    payload = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(
        BASE_URL + path,
        data=payload,
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": SOURCE_URL,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="replace")
    return body if text else json.loads(body)


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def to_float(value: str) -> float | None:
    match = re.search(r"-?\d+(?:\.\d+)?", value or "")
    return float(match.group()) if match else None


def parse_grade_cut_html(markup: str) -> dict[str, dict]:
    records: dict[str, dict] = {}
    sections = re.split(r'<div class="col_6">', markup)
    for section in sections:
        title_match = re.search(r"<h3>(.*?)</h3>", section, flags=re.S)
        if not title_match:
            continue
        subject = clean_text(title_match.group(1)).replace(" ", "")
        if subject not in SUBJECTS:
            continue

        mean = to_float(re.search(r"평균:\s*([0-9.]+)", section).group(1)) if re.search(r"평균:\s*([0-9.]+)", section) else None
        sd = to_float(re.search(r"표준편차:\s*([0-9.]+)", section).group(1)) if re.search(r"표준편차:\s*([0-9.]+)", section) else None
        record = {"subject": subject, "national_mean": mean, "national_sd": sd, "cuts": {}}

        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", section, flags=re.S):
            cells = [clean_text(cell) for cell in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]
            if len(cells) < 4:
                continue
            grade = cells[0].strip()
            if grade not in {"1", "2", "3"}:
                continue
            record["cuts"][grade] = {
                "raw": to_float(cells[1]),
                "standard": to_float(cells[2]),
                "percentile": to_float(cells[3]),
            }

        if (
            mean is not None
            and sd is not None
            and 0 <= mean <= 50
            and 0 < sd <= 20
            and all(str(cut) in record["cuts"] for cut in (1, 3))
            and record["cuts"]["1"].get("raw") is not None
            and record["cuts"]["1"].get("standard") is not None
            and record["cuts"]["3"].get("raw") is not None
            and record["cuts"]["3"].get("standard") is not None
        ):
            records[subject] = record
    return records


def parse_wrong_answer_html(markup: str) -> list[dict]:
    if "서비스 준비중" in markup or "nodata" in markup and "<tbody>" not in markup:
        return []

    rows = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", markup, flags=re.S):
        cells = [clean_text(cell) for cell in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]
        if len(cells) < 10:
            continue
        try:
            rank = int(cells[0])
            question = int(cells[1])
            wrong_rate = float(cells[2])
            points = int(float(cells[3]))
            answer = int(float(cells[4]))
            choices = [float(cells[index]) for index in range(5, 10)]
        except ValueError:
            continue
        rows.append(
            {
                "rank": rank,
                "question": question,
                "wrong_rate": wrong_rate,
                "correct_rate": 100 - wrong_rate,
                "points": points,
                "answer": answer,
                "choices": choices,
            }
        )
    return rows


def infer_easy_missing_rate(wrong_rows: list[dict]) -> float:
    easiest_top15_rate = max(row["correct_rate"] for row in wrong_rows)
    return (100.0 + easiest_top15_rate) / 2


def infer_items(grade_record: dict, wrong_rows: list[dict]) -> list[dict] | None:
    if not wrong_rows or grade_record.get("national_mean") is None:
        return None

    by_question = {row["question"]: row for row in wrong_rows}
    known_points = sum(row["points"] for row in wrong_rows)
    missing_questions = [question for question in range(1, 21) if question not in by_question]
    missing_total = 50 - known_points
    if missing_total < 0 or missing_total > 3 * len(missing_questions):
        return None

    missing_points = {question: 2 for question in missing_questions}
    extra_three_point_count = int(round(missing_total - 2 * len(missing_questions)))
    for question in sorted(missing_questions, reverse=True)[: max(0, extra_three_point_count)]:
        missing_points[question] = 3

    if missing_total > 0:
        missing_rate = infer_easy_missing_rate(wrong_rows)
    else:
        missing_rate = 100.0
    missing_rate = max(0.0, min(100.0, missing_rate))

    items = []
    for question in range(1, 21):
        if question in by_question:
            row = by_question[question]
            items.append(
                {
                    "question": question,
                    "points": row["points"],
                    "national_rate": row["correct_rate"],
                    "source": "ebsi_wrong_top15",
                }
            )
        else:
            items.append(
                {
                    "question": question,
                    "points": missing_points[question],
                    "national_rate": missing_rate,
                    "source": "easy_midpoint_inferred_missing",
                }
            )
    return items


def result_list(payload: dict) -> list[dict]:
    return payload.get("result") or []


def fetch_records(delay: float) -> list[dict]:
    records: list[dict] = []
    grade_years = result_list(post("/ebs/xip/xipa/retrievePastGrdCutYearList.ajax"))
    wrong_years = {item["code"] for item in result_list(post("/ebs/xip/xipa/retrieveWrongAnswerRateYearList.ajax"))}

    for grade_year in grade_years:
        school_year = int(grade_year["code"])
        exam_year = str(school_year - 1)
        if exam_year not in wrong_years:
            continue

        grade_months = result_list(
            post(
                "/ebs/xip/xipa/retrievePastGrdCutMonthList.ajax",
                {"year": grade_year["code"], "stdntGrd": "3"},
            )
        )
        wrong_months = result_list(
            post(
                "/ebs/xip/xipa/retrieveWrongAnswerRateMonthList.ajax",
                {"year": exam_year, "targetCd": "D300"},
            )
        )
        wrong_month_by_value = {item["value"]: item["code"] for item in wrong_months}

        for grade_month in grade_months:
            month_value = grade_month["value"]
            wrong_record_id = wrong_month_by_value.get(month_value)
            if not wrong_record_id:
                continue

            grade_html = post(
                "/ebs/xip/xipa/retrievePastGrdCutList.ajax",
                {
                    "year": grade_year["code"],
                    "stdntGrd": "3",
                    "month": grade_month["code"],
                    "subjCd": SOCIAL_GRADE_TAB_CODE,
                },
                text=True,
            )
            grade_records = parse_grade_cut_html(grade_html)
            if not grade_records:
                continue

            subject_options = result_list(
                post(
                    "/ebs/xip/xipa/retrieveWrongAnswerRateSubjList.ajax",
                    {
                        "year": exam_year,
                        "targetCd": "D300",
                        "irecord": wrong_record_id,
                        "arOrd": SOCIAL_AREA_CODE,
                    },
                )
            )
            subject_codes = {item["value"].replace(" ", "").replace("·", ""): item["code"] for item in subject_options}

            for subject in SUBJECTS:
                if subject not in grade_records or subject not in subject_codes:
                    continue
                wrong_html = post(
                    "/ebs/xip/xipa/retrieveWrongAnswerRateList.ajax",
                    {"paperId": subject_codes[subject]},
                    text=True,
                )
                wrong_rows = parse_wrong_answer_html(wrong_html)
                items = infer_items(grade_records[subject], wrong_rows)
                if not items:
                    continue

                grade_record = grade_records[subject]
                records.append(
                    {
                        "source": "EBSi",
                        "school_year": school_year,
                        "exam_year": int(exam_year),
                        "month": month_value,
                        "subject": subject,
                        "national_mean": grade_record["national_mean"],
                        "national_sd": grade_record["national_sd"],
                        "raw1": grade_record["cuts"]["1"]["raw"],
                        "raw2": grade_record["cuts"]["2"]["raw"],
                        "raw3": grade_record["cuts"]["3"]["raw"],
                        "std1": grade_record["cuts"]["1"]["standard"],
                        "std2": grade_record["cuts"]["2"]["standard"],
                        "std3": grade_record["cuts"]["3"]["standard"],
                        "items": items,
                        "wrong_top15": wrong_rows,
                    }
                )
                time.sleep(delay)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().with_name("ebsi_geo_data.json"),
    )
    parser.add_argument("--delay", type=float, default=0.05)
    args = parser.parse_args()

    records = fetch_records(args.delay)
    payload = {
        "source": "EBSi 역대 등급컷/오답률",
        "source_url": SOURCE_URL,
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "records": records,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    by_subject = {subject: sum(record["subject"] == subject for record in records) for subject in SUBJECTS}
    print(f"wrote {args.output}")
    print(json.dumps({"total": len(records), "by_subject": by_subject}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
