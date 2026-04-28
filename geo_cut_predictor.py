"""Runtime predictor for Korean/World Geography first-cut estimates."""

from __future__ import annotations

import json
import math
import hashlib
import re
import unicodedata
from bisect import bisect_left, bisect_right
from functools import lru_cache
from pathlib import Path
from statistics import NormalDist
from typing import Iterable


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "geo_cut_model.json"
EBSI_PATH = ROOT / "ebsi_geo_data.json"
QUESTION_IMAGE_ROOTS = (
    {
        "subject": "세계지리",
        "path": Path.home() / "Downloads" / "세계지리 3",
        "priority": 20,
        "label": "26학년도 사진",
    },
    {
        "subject": "한국지리",
        "path": Path.home() / "Downloads" / "한국지리 2",
        "priority": 20,
        "label": "26학년도 사진",
    },
    {
        "subject": "세계지리",
        "path": Path.home() / "Downloads" / "세계지리 2",
        "priority": 10,
        "label": "기존 사진",
    },
    {
        "subject": "한국지리",
        "path": Path.home() / "Downloads" / "한국지리",
        "priority": 10,
        "label": "기존 사진",
    },
)
QUESTION_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
LOGIT_EPS = 0.005
GRADE_PERCENTILES = {"1": 0.96, "2": 0.89, "3": 0.77}
NORMAL_DIST = NormalDist()


class PredictionError(ValueError):
    """Raised when predictor inputs are not usable."""


@lru_cache(maxsize=1)
def load_model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_ebsi_payload() -> dict:
    if not EBSI_PATH.exists():
        return {"records": []}
    return json.loads(EBSI_PATH.read_text(encoding="utf-8"))


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def historical_exam_id(record: dict) -> str:
    return f"{record.get('exam_year')}-{str(record.get('month')).zfill(2)}-{record.get('subject')}"


def possible_raw_scores(points: list[float]) -> list[int] | None:
    int_points = []
    for point in points:
        rounded = round(point)
        if abs(point - rounded) > 0.001:
            return None
        int_points.append(int(rounded))

    scores = {0}
    for point in int_points:
        scores |= {score + point for score in scores}
    return sorted(scores)


def nearest_possible_score(value: float, possible_scores: list[int], total_points: float) -> int:
    clamped = clamp(value, 0, total_points)
    return min(possible_scores, key=lambda score: (abs(score - clamped), -score))


def lower_possible_score(value: float, possible_scores: list[int], total_points: float) -> int:
    clamped = clamp(value, 0, total_points)
    candidates = [score for score in possible_scores if score <= clamped + 0.001]
    return candidates[-1] if candidates else possible_scores[0]


def upper_possible_score(value: float, possible_scores: list[int], total_points: float) -> int:
    clamped = clamp(value, 0, total_points)
    candidates = [score for score in possible_scores if score >= clamped - 0.001]
    return candidates[0] if candidates else possible_scores[-1]


def round_half_up(value: float) -> int:
    return int(math.floor(value + 0.5))


def sigmoid(value: float) -> float:
    return 1 / (1 + math.exp(-value))


def chance_floor_logit(rate: float, floor: float) -> float:
    scaled = (rate - floor) / (100 - floor)
    scaled = clamp(scaled, LOGIT_EPS, 1 - LOGIT_EPS)
    return math.log(scaled / (1 - scaled))


def chance_floor_rate(value: float, floor: float) -> float:
    return floor + (100 - floor) * sigmoid(value)


def percentile(sorted_values: list[float], value: float) -> float:
    if len(sorted_values) <= 1:
        return 0.0
    left = bisect_left(sorted_values, value)
    right = bisect_right(sorted_values, value)
    rank = (left + right - 1) / 2
    return clamp(rank / (len(sorted_values) - 1), 0.0, 1.0)


def quantile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    if q <= 0:
        return sorted_values[0]
    if q >= 1:
        return sorted_values[-1]
    position = q * (len(sorted_values) - 1)
    low = int(position)
    high = min(low + 1, len(sorted_values) - 1)
    fraction = position - low
    return sorted_values[low] * (1 - fraction) + sorted_values[high] * fraction


def quantile_map(info: dict, rate: float, source: str, target: str) -> float | None:
    source_rates = info.get(f"{source}_rates", [])
    target_rates = info.get(f"{target}_rates", [])
    if not source_rates or not target_rates:
        return None
    return quantile(target_rates, percentile(source_rates, rate))


def map_item_rates(subject: str, rates: list[float], model: dict, source: str, target: str) -> list[float] | None:
    mappings = model.get("item_rate_mapping", {})
    mapping = mappings.get(subject)
    if not mapping:
        return None
    if not mapping.get(f"usable_for_runtime_{source}_conversion", False):
        return None

    if mapping.get("method") == "empirical_quantile":
        mapped = [quantile_map(mapping, rate, source, target) for rate in rates]
        if any(value is None for value in mapped):
            return None
        return [float(value) for value in mapped]

    if mapping.get("method") == "pooled_empirical_quantile_with_subject_shrinkage":
        pooled_mapping = mappings.get("_pooled", {})
        subject_weight = clamp(float(mapping.get("subject_weight", 0.25)), 0.0, 1.0)
        mapped = []
        for rate in rates:
            pooled_value = quantile_map(pooled_mapping, rate, source, target)
            subject_value = quantile_map(mapping, rate, source, target)
            if pooled_value is None and subject_value is None:
                return None
            if pooled_value is None:
                mapped.append(float(subject_value))
            elif subject_value is None:
                mapped.append(float(pooled_value))
            else:
                mapped.append((1 - subject_weight) * pooled_value + subject_weight * subject_value)
        return mapped

    return None


def normalize_numbers(values: Iterable[object], count: int, label: str) -> list[float]:
    numbers = []
    for value in values:
        try:
            numbers.append(float(value))
        except (TypeError, ValueError):
            raise PredictionError(f"{label} 값은 숫자여야 합니다.") from None
    if len(numbers) != count:
        raise PredictionError(f"{label}은 {count}개가 필요합니다.")
    return numbers


def convert_academy_to_national(subject: str, rates: list[float], model: dict) -> list[float]:
    mapped = map_item_rates(subject, rates, model, "academy", "national")
    if mapped:
        return [min(mapped_rate, academy_rate) for mapped_rate, academy_rate in zip(mapped, rates)]

    relation = model["academy_to_national_rate"][subject]
    intercept = relation["intercept"]
    slope = relation["slope"]
    if relation.get("method") == "chance_floor_logit":
        floor = relation["chance_floor"]
        return [
            chance_floor_rate(intercept + slope * chance_floor_logit(rate, floor), floor)
            for rate in rates
        ]
    if relation.get("method") == "linear_with_chance_floor":
        floor = relation["chance_floor"]
        return [clamp(intercept + slope * rate, floor, 99.5) for rate in rates]
    return [clamp(intercept + slope * rate, 0.5, 99.5) for rate in rates]


def convert_national_to_academy(subject: str, rates: list[float], model: dict) -> list[dict[str, object]]:
    mapped = map_item_rates(subject, rates, model, "national", "academy")
    if mapped:
        return [
            {
                "value": clamp(max(value, rate), 0, 100),
                "label": f"{clamp(max(value, rate), 0, 100):.1f}%",
                "is_upper_bound": False,
            }
            for value, rate in zip(mapped, rates)
        ]

    relation = model["academy_to_national_rate"][subject]
    intercept = relation["intercept"]
    slope = relation["slope"]
    converted = []
    if relation.get("method") == "linear_with_chance_floor":
        floor = relation["chance_floor"]
        threshold = clamp((floor - intercept) / slope, 0, 100)
        upper_reachable = intercept + slope * 100
        for rate in rates:
            if rate <= floor + 0.001:
                converted.append(
                    {
                        "value": threshold,
                        "label": f"≤{threshold:.1f}%",
                        "is_upper_bound": True,
                    }
                )
            elif rate >= upper_reachable - 0.001:
                converted.append(
                    {
                        "value": 100.0,
                        "label": "≥100.0%",
                        "is_upper_bound": False,
                    }
                )
            else:
                value = clamp((rate - intercept) / slope, 0, 100)
                converted.append(
                    {
                        "value": value,
                        "label": f"{value:.1f}%",
                        "is_upper_bound": False,
                    }
                )
        return converted

    if relation.get("method") == "chance_floor_logit":
        floor = relation["chance_floor"]
        for rate in rates:
            value = chance_floor_rate(
                (chance_floor_logit(rate, floor) - intercept) / slope,
                floor,
            )
            converted.append(
                {
                    "value": clamp(value, 0, 100),
                    "label": f"{clamp(value, 0, 100):.1f}%",
                    "is_upper_bound": False,
                }
            )
        return converted

    for rate in rates:
        value = clamp((rate - intercept) / slope, 0, 100)
        converted.append({"value": value, "label": f"{value:.1f}%", "is_upper_bound": False})
    return converted


def hard_item_features(rates: list[float], points: list[float], count: int = 15) -> dict[str, float]:
    ranked_items = sorted(zip(rates, points), key=lambda pair: pair[0])
    hard_items = ranked_items[:count]
    easy_items = ranked_items[count:]
    hard_points = sum(point for _, point in hard_items)
    hard_rate = sum(point * rate for rate, point in hard_items) / hard_points
    hard_variance = sum(
        point * (rate - hard_rate) ** 2 for rate, point in hard_items
    ) / hard_points
    easy_points = sum(point for _, point in easy_items)
    easy_rate = (
        sum(point * rate for rate, point in easy_items) / easy_points
        if easy_points
        else max(rates)
    )
    return {
        "hard15_rate": hard_rate,
        "hard15_sd": math.sqrt(hard_variance),
        "under40_points": sum(point for rate, point in hard_items if rate < 40),
        "under50_points": sum(point for rate, point in hard_items if rate < 50),
        "easy5_rate": easy_rate,
    }


def feature_values(rates: list[float], points: list[float]) -> dict[str, float]:
    total_points = sum(points)
    probabilities = [rate / 100 for rate in rates]
    mean = sum(point * probability for point, probability in zip(points, probabilities))
    independent_sd = math.sqrt(
        sum(point * point * probability * (1 - probability) for point, probability in zip(points, probabilities))
    )
    weighted_rate = mean / total_points * 100
    rate_variance = sum(
        point * (rate - weighted_rate) ** 2 for point, rate in zip(points, rates)
    ) / total_points
    features = {
        "mean": mean,
        "ind_sd": independent_sd,
        "rate_sd": math.sqrt(rate_variance),
        "weighted_rate": weighted_rate,
    }
    features.update(hard_item_features(rates, points))
    return features


def apply_linear_model(coefficients: dict, subject: str, features: dict) -> float:
    value = coefficients["intercept"]
    if subject == "세계지리":
        value += coefficients["world_geography_offset"]
    for name, coefficient in coefficients.items():
        if name in {"intercept", "world_geography_offset"}:
            continue
        value += coefficient * features[name]
    return value


def score_scale_rows(
    possible_scores: list[int] | None,
    total_points: float,
    mean: float,
    sd: float,
    predictions: dict[str, dict] | None = None,
) -> list[dict[str, float | int]]:
    if possible_scores:
        scores = sorted(possible_scores, reverse=True)
    else:
        scores = list(range(int(math.floor(total_points)), -1, -1))

    safe_sd = max(0.1, sd)
    grade_anchors = []
    cut_labels: dict[int, list[str]] = {}
    if predictions:
        for cut, percentile_value in GRADE_PERCENTILES.items():
            prediction = predictions.get(cut)
            if not prediction:
                continue
            grade_anchors.append(
                (
                    float(prediction["predicted_cut"]),
                    NORMAL_DIST.inv_cdf(percentile_value),
                )
            )
            cut_labels.setdefault(int(prediction["suggested_cut"]), []).append(f"{cut}컷")

    grade_anchors = sorted(grade_anchors, key=lambda anchor: anchor[0], reverse=True)
    unique_anchors = []
    for raw_score, z_score in grade_anchors:
        if not unique_anchors or abs(raw_score - unique_anchors[-1][0]) > 0.001:
            unique_anchors.append((raw_score, z_score))

    def calibrated_z_score(score: float) -> float:
        if len(unique_anchors) < 2:
            return (score - mean) / safe_sd

        if score >= unique_anchors[0][0]:
            high_anchor, low_anchor = unique_anchors[0], unique_anchors[1]
        elif score <= unique_anchors[-1][0]:
            high_anchor, low_anchor = unique_anchors[-2], unique_anchors[-1]
        else:
            high_anchor, low_anchor = unique_anchors[0], unique_anchors[1]
            for index in range(len(unique_anchors) - 1):
                candidate_high = unique_anchors[index]
                candidate_low = unique_anchors[index + 1]
                if candidate_high[0] >= score >= candidate_low[0]:
                    high_anchor, low_anchor = candidate_high, candidate_low
                    break

        raw_span = high_anchor[0] - low_anchor[0]
        if abs(raw_span) <= 0.001:
            return (score - mean) / safe_sd
        fraction = (score - low_anchor[0]) / raw_span
        return low_anchor[1] + fraction * (high_anchor[1] - low_anchor[1])

    rows = []
    for score in scores:
        standard_z_score = (score - mean) / safe_sd
        percentile_z_score = calibrated_z_score(score)
        standard_score_value = 50 + 10 * standard_z_score
        percentile_value = 100 * (0.5 * (1 + math.erf(percentile_z_score / math.sqrt(2))))
        rows.append(
            {
                "raw_score": score,
                "standard_score": round_half_up(standard_score_value),
                "standard_score_exact": standard_score_value,
                "percentile": clamp(round_half_up(percentile_value), 0, 100),
                "percentile_exact": clamp(percentile_value, 0, 100),
                "cut_label": " · ".join(cut_labels.get(score, [])),
            }
        )
    return rows


def runtime_bias_correction(model: dict, mode: str, subject: str, cut: str) -> float:
    correction = model.get("runtime_corrections", {}).get(mode)
    if not correction or correction.get("method") != "subject_cut_bias_subtraction":
        return 0.0
    subject_corrections = correction.get("by_subject", {}).get(subject, {})
    if cut in subject_corrections:
        return max(0.0, float(subject_corrections[cut]))
    return max(0.0, float(correction.get("by_cut", {}).get(cut, 0.0)))


def historical_cut_caps(subject: str, features: dict, model: dict) -> tuple[dict[str, float], list[dict]]:
    caps: dict[str, float] = {}
    latest_november_anchor: dict | None = None
    matched = []
    for anchor in model.get("historical_anchors", []):
        if anchor.get("subject") != subject:
            continue
        if (
            anchor.get("mean") is None
            or anchor.get("nat_sd") is None
            or anchor.get("hard15_rate") is None
        ):
            continue
        anchor_mean = float(anchor["mean"])
        anchor_rate_mean = float(anchor.get("rate_mean", anchor_mean))
        anchor_sd = max(0.1, float(anchor["nat_sd"]))
        anchor_easy5_rate = float(anchor.get("easy5_rate", anchor["easiest_top15_rate"]))
        no_easier_than_anchor = (
            features["mean"] <= anchor_rate_mean + 0.5
            and features["hard15_rate"] <= float(anchor["hard15_rate"]) + 1.0
            and features["easy5_rate"] <= anchor_easy5_rate + 1.0
        )
        if not no_easier_than_anchor:
            continue

        if str(anchor.get("month")).zfill(2) == "11" and (
            latest_november_anchor is None
            or int(anchor.get("exam_year") or 0) > int(latest_november_anchor.get("exam_year") or 0)
        ):
            latest_november_anchor = anchor

        matched.append(
            {
                "exam_year": anchor.get("exam_year"),
                "month": anchor.get("month"),
                "raw1": anchor.get("raw1"),
                "raw2": anchor.get("raw2"),
                "raw3": anchor.get("raw3"),
            }
        )
        for cut in ("1", "2", "3"):
            raw_cut = anchor.get(f"raw{cut}")
            if raw_cut is None:
                continue
            raw_cut = float(raw_cut)
            caps[cut] = min(caps.get(cut, raw_cut), raw_cut)

    if latest_november_anchor:
        anchor_mean = float(latest_november_anchor["mean"])
        anchor_sd = max(0.1, float(latest_november_anchor["nat_sd"]))
        for cut in ("1", "2", "3"):
            raw_cut = latest_november_anchor.get(f"raw{cut}")
            if raw_cut is None:
                continue
            raw_cut = float(raw_cut)
            anchor_z = (raw_cut - anchor_mean) / anchor_sd
            scaled_cap = raw_cut + (features["mean"] - anchor_mean)
            scaled_cap += anchor_z * (features["nat_sd"] - anchor_sd)
            caps[cut] = min(caps.get(cut, raw_cut), raw_cut, scaled_cap)

    return caps, matched


def historical_matches(subject: str, features: dict, predictions: dict, model: dict) -> list[dict]:
    matches = []
    for record in load_ebsi_payload().get("records", []):
        if record.get("subject") != subject:
            continue
        items = record.get("items") or []
        if len(items) != 20:
            continue
        if record.get("national_mean") is None or record.get("national_sd") is None:
            continue
        try:
            rates = [float(item["national_rate"]) for item in items]
            points = [float(item["points"]) for item in items]
        except (KeyError, TypeError, ValueError):
            continue

        anchor_features = feature_values(rates, points)
        anchor_features["nat_sd"] = clamp(
            apply_linear_model(model["sd_model"]["coefficients"], subject, anchor_features),
            0.1,
            25.0,
        )

        mean_delta = features["mean"] - anchor_features["mean"]
        sd_delta = features["nat_sd"] - anchor_features["nat_sd"]
        hard_delta = features["hard15_rate"] - anchor_features["hard15_rate"]
        easy_delta = features["easy5_rate"] - anchor_features["easy5_rate"]
        under40_delta = features["under40_points"] - anchor_features["under40_points"]
        distance = math.sqrt(
            (mean_delta / 3.0) ** 2
            + (sd_delta / 1.6) ** 2
            + (hard_delta / 8.0) ** 2
            + (easy_delta / 12.0) ** 2
            + (under40_delta / 8.0) ** 2
        )

        cuts = {
            cut: int(float(record[f"raw{cut}"]))
            for cut in ("1", "2", "3")
            if record.get(f"raw{cut}") is not None
        }
        cut_diffs = {
            cut: int(predictions[cut]["suggested_cut"]) - cuts[cut]
            for cut in cuts
            if cut in predictions
        }
        matches.append(
            {
                "id": historical_exam_id(record),
                "subject": record.get("subject"),
                "exam_year": record.get("exam_year"),
                "month": str(record.get("month")).zfill(2),
                "mean": record.get("national_mean"),
                "nat_sd": record.get("national_sd"),
                "hard15_rate": anchor_features["hard15_rate"],
                "easy5_rate": anchor_features["easy5_rate"],
                "under40_points": anchor_features["under40_points"],
                "cuts": cuts,
                "cut_diffs": cut_diffs,
                "distance": distance,
            }
        )
    return sorted(matches, key=lambda match: match["distance"])[:8]


def historical_exam_payload() -> dict:
    exams = []
    for record in load_ebsi_payload().get("records", []):
        if record.get("subject") not in {"한국지리", "세계지리"}:
            continue
        items = record.get("items") or []
        if len(items) != 20:
            continue
        if any(item.get("national_rate") is None or item.get("points") is None for item in items):
            continue

        inferred_items = [
            item
            for item in items
            if "inferred" in str(item.get("source", ""))
            or str(item.get("source", "")).startswith("easy_floor")
        ]
        exams.append(
            {
                "id": historical_exam_id(record),
                "subject": record.get("subject"),
                "exam_year": record.get("exam_year"),
                "school_year": record.get("school_year"),
                "month": str(record.get("month")).zfill(2),
                "label": f"{record.get('exam_year')}년 {str(record.get('month')).zfill(2)}월 {record.get('subject')}",
                "mean": record.get("national_mean"),
                "nat_sd": record.get("national_sd"),
                "cuts": {
                    cut: int(float(record[f"raw{cut}"]))
                    for cut in ("1", "2", "3")
                    if record.get(f"raw{cut}") is not None
                },
                "points": [float(item["points"]) for item in items],
                "rates": [float(item["national_rate"]) for item in items],
                "inferred_count": len(inferred_items),
                "inferred_rate": (
                    sum(float(item["national_rate"]) for item in inferred_items) / len(inferred_items)
                    if inferred_items
                    else None
                ),
            }
        )
    exams.sort(
        key=lambda exam: (
            int(exam.get("exam_year") or 0),
            int(exam.get("month") or 0),
            exam.get("subject") or "",
        ),
        reverse=True,
    )
    return {"exams": exams, "count": len(exams)}


def normalize_text(value: object) -> str:
    return unicodedata.normalize("NFC", str(value or ""))


def question_subject_code(subject: str) -> str:
    return "world" if subject == "세계지리" else "korea"


def parse_question_image_metadata(path: Path, fallback_subject: str) -> dict | None:
    text = normalize_text(" ".join(path.parts))
    if "세계지리" in text:
        subject = "세계지리"
    elif "한국지리" in text:
        subject = "한국지리"
    else:
        subject = fallback_subject

    exam_year = None
    school_year = None
    month = None
    for part in path.parts:
        shorthand = re.fullmatch(r"(\d{2})(0[369]|11)", normalize_text(part))
        if shorthand:
            exam_year = 2000 + int(shorthand.group(1))
            month = shorthand.group(2)
            school_year = exam_year + 1
            break

    if exam_year is None:
        school_year_match = re.search(r"(\d{2}|\d{4})\s*학년도", text)
        if not school_year_match:
            return None
        school_year_text = school_year_match.group(1)
        school_year = int(school_year_text)
        if school_year < 100:
            school_year += 2000
        exam_year = school_year - 1
        month_match = re.search(r"(\d{1,2})\s*월", text)
        if month_match:
            month = f"{int(month_match.group(1)):02d}"
        else:
            month_match = re.search(r"(\d{1,2})\s*평", text)
            if month_match:
                month = f"{int(month_match.group(1)):02d}"
        if month is None and ("대학수학능력시험" in text or "수능" in text):
            month = "11"

    if month is None:
        return None

    name = normalize_text(path.name)
    question = None
    for pattern in (
        r"_(\d{1,2})-(?:일반|투명)",
        r"Problem_object_\d+_(\d{4})",
        r"\[문제0*(\d{1,2})\]",
        r"_(\d{4})\.",
    ):
        question_match = re.search(pattern, name)
        if question_match:
            question = int(question_match.group(1))
            break

    if question is None or question < 1 or question > 20:
        return None

    return {
        "subject": subject,
        "exam_year": exam_year,
        "school_year": school_year,
        "month": month,
        "question": question,
    }


def question_image_priority(path: Path) -> tuple[int, str]:
    name = normalize_text(path.name)
    if "일반" in name:
        return 4, "일반"
    if "[문제" in name:
        return 4, "문항"
    if "Problem_object" in name:
        return 3, "문항"
    if "투명" in name:
        return 2, "투명배경"
    return 1, "이미지"


def question_rate_source_label(source: object) -> str:
    text = str(source or "")
    if "inferred" in text or text.startswith("easy_floor"):
        return "보충 데이터"
    if text:
        return "EBSi"
    return ""


def question_match_status(source: object, record: dict | None) -> tuple[str, str]:
    if not record:
        return "unmatched", "정보 없음"
    text = str(source or "")
    if "inferred" in text or text.startswith("easy_floor"):
        return "inferred", "보충 데이터"
    if text:
        return "exact", "EBSi"
    return "unmatched", "정보 없음"


def question_choice_rates(record: dict | None, question: int) -> list[dict[str, object]]:
    if not record:
        return []
    for row in record.get("wrong_top15", []):
        if int(row.get("question") or 0) != question:
            continue
        choices = row.get("choices") or []
        answer = int(row.get("answer") or 0)
        rates = []
        for index, rate in enumerate(choices, start=1):
            if rate is None:
                continue
            rates.append(
                {
                    "choice": index,
                    "rate": round(float(rate), 1),
                    "is_answer": index == answer,
                }
            )
        return rates
    return []


def difficulty_band(wrong_rate: float | None) -> tuple[str, str]:
    if wrong_rate is None:
        return "unknown", "난이도 정보 없음"
    if wrong_rate >= 60:
        return "very_hard", "최고난도"
    if wrong_rate >= 45:
        return "hard", "고난도"
    if wrong_rate >= 25:
        return "normal", "보통"
    return "easy", "쉬움"


def question_exam_label(subject: str, exam_year: int, school_year: int | None, month: str) -> str:
    display_school_year = school_year or exam_year + 1
    if month == "11":
        return f"{display_school_year}학년도 수능 {subject}"
    return f"{display_school_year}학년도 {int(month)}월 모의평가 {subject}"


def question_exam_short_label(exam_year: int, school_year: int | None, month: str) -> str:
    display_school_year = school_year or exam_year + 1
    if month == "11":
        return f"{display_school_year} 수능"
    return f"{display_school_year} {int(month)}월"


def historical_record_lookup() -> dict:
    lookup = {}
    for record in load_ebsi_payload().get("records", []):
        subject = record.get("subject")
        exam_year = record.get("exam_year")
        month = record.get("month")
        if subject not in {"한국지리", "세계지리"} or exam_year is None or month is None:
            continue
        lookup[(subject, int(exam_year), str(month).zfill(2))] = record
    return lookup


def record_cuts(record: dict | None) -> dict:
    if not record:
        return {}
    return {
        cut: int(float(record[f"raw{cut}"]))
        for cut in ("1", "2", "3")
        if record.get(f"raw{cut}") is not None
    }


@lru_cache(maxsize=1)
def question_bank_index() -> dict:
    records = historical_record_lookup()
    grouped: dict[tuple[str, int, str, int], dict] = {}
    for root_info in QUESTION_IMAGE_ROOTS:
        fallback_subject = root_info["subject"]
        root = root_info["path"]
        source_priority = int(root_info["priority"])
        source_label = str(root_info["label"])
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() not in QUESTION_IMAGE_EXTENSIONS:
                continue
            metadata = parse_question_image_metadata(path, fallback_subject)
            if not metadata:
                continue
            key = (
                metadata["subject"],
                int(metadata["exam_year"]),
                str(metadata["month"]).zfill(2),
                int(metadata["question"]),
            )
            priority, variant = question_image_priority(path)
            current = grouped.get(key)
            if current is None:
                grouped[key] = {
                    **metadata,
                    "path": path,
                    "priority": priority,
                    "source_priority": source_priority,
                    "source_label": source_label,
                    "variant": variant,
                    "image_count": 1,
                }
            else:
                current["image_count"] += 1
                if (source_priority, priority) > (
                    current["source_priority"],
                    current["priority"],
                ):
                    current["path"] = path
                    current["priority"] = priority
                    current["source_priority"] = source_priority
                    current["source_label"] = source_label
                    current["variant"] = variant

    items = []
    paths = {}
    for (subject, exam_year, month, question), image in grouped.items():
        record = records.get((subject, exam_year, month))
        item = None
        if record:
            item = next(
                (
                    row
                    for row in record.get("items", [])
                    if int(row.get("question") or 0) == question
                ),
                None,
            )

        correct_rate = (
            round(float(item["national_rate"]), 1)
            if item and item.get("national_rate") is not None
            else None
        )
        wrong_rate = round(100 - correct_rate, 1) if correct_rate is not None else None
        points = (
            float(item["points"])
            if item and item.get("points") is not None
            else None
        )
        image_id = f"{question_subject_code(subject)}-{exam_year}-{month}-{question:02d}"
        path = image["path"]
        paths[image_id] = path
        cuts = record_cuts(record)
        source = item.get("source") if item else None
        match_status, match_label = question_match_status(source, record)
        difficulty, difficulty_label = difficulty_band(wrong_rate)
        choice_rates = question_choice_rates(record, question)
        school_year = record.get("school_year") if record else image.get("school_year")
        exam_key = f"{subject}|{exam_year}|{month}"
        exam_label = question_exam_label(subject, exam_year, school_year, month)
        exam_short_label = question_exam_short_label(exam_year, school_year, month)
        label = f"{exam_short_label} {subject} {question}번"
        items.append(
            {
                "id": image_id,
                "label": label,
                "exam_key": exam_key,
                "exam_label": exam_label,
                "exam_short_label": exam_short_label,
                "subject": subject,
                "exam_year": exam_year,
                "school_year": school_year,
                "month": month,
                "question": question,
                "points": points,
                "correct_rate": correct_rate,
                "wrong_rate": wrong_rate,
                "choice_rates": choice_rates,
                "rate_source": question_rate_source_label(source),
                "match_status": match_status,
                "match_label": match_label,
                "difficulty": difficulty,
                "difficulty_label": difficulty_label,
                "raw_source": source,
                "image_url": f"/api/question-image/{image_id}",
                "image_count": image["image_count"],
                "image_variant": image["variant"],
                "image_set": image["source_label"],
                "mean": record.get("national_mean") if record else None,
                "nat_sd": record.get("national_sd") if record else None,
                "cuts": cuts,
                "exam_id": historical_exam_id(record) if record else None,
                "search_text": normalize_text(
                    f"{label} {exam_label} {path.name} {path.parent.name} "
                    f"{source or ''} {match_label} {difficulty_label} {image['source_label']}"
                ),
            }
        )

    items.sort(
        key=lambda row: (
            -int(row["exam_year"]),
            -int(row["month"]),
            row["subject"],
            int(row["question"]),
        )
    )
    exam_groups = {}
    for item in items:
        exam = exam_groups.setdefault(
            item["exam_key"],
            {
                "key": item["exam_key"],
                "label": item["exam_label"],
                "short_label": item["exam_short_label"],
                "subject": item["subject"],
                "exam_year": item["exam_year"],
                "school_year": item["school_year"],
                "month": item["month"],
                "count": 0,
                "exact_count": 0,
                "inferred_count": 0,
                "unmatched_count": 0,
            },
        )
        exam["count"] += 1
        if item["match_status"] == "exact":
            exam["exact_count"] += 1
        elif item["match_status"] == "inferred":
            exam["inferred_count"] += 1
        else:
            exam["unmatched_count"] += 1

    exams = sorted(
        exam_groups.values(),
        key=lambda exam: (
            -int(exam["exam_year"]),
            -int(exam["month"]),
            exam["subject"],
        ),
    )
    return {
        "items": items,
        "paths": paths,
        "available": {
            "subjects": sorted({item["subject"] for item in items}),
            "years": sorted({item["exam_year"] for item in items}),
            "months": sorted({item["month"] for item in items}),
            "exams": exams,
        },
    }


def refresh_question_bank() -> None:
    question_bank_index.cache_clear()


def question_image_path(image_id: str) -> Path | None:
    path = question_bank_index()["paths"].get(image_id)
    if path and path.exists():
        return path
    return None


def filter_number(value: object, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def search_question_bank(params: object) -> dict:
    index = question_bank_index()
    items = index["items"]
    subject = str(params.get("subject", "") or "")
    exam_key = str(params.get("exam_key", "") or "")
    month = str(params.get("month", "") or "")
    difficulty = str(params.get("difficulty", "") or "")
    match_status = str(params.get("match", "") or "")
    sort_key = str(params.get("sort", "latest") or "latest")
    text_query = normalize_text(params.get("q", "")).strip().lower()
    question = filter_number(params.get("question"))
    year_from = filter_number(params.get("year_from"))
    year_to = filter_number(params.get("year_to"))
    wrong_min = filter_number(params.get("wrong_min"))
    wrong_max = filter_number(params.get("wrong_max"))
    correct_min = filter_number(params.get("correct_min"))
    correct_max = filter_number(params.get("correct_max"))
    limit = int(clamp(filter_number(params.get("limit"), 24) or 24, 1, 120))

    filtered = []
    for item in items:
        if exam_key:
            if item["exam_key"] != exam_key:
                continue
        elif subject and item["subject"] != subject:
            continue
        if not exam_key:
            if month and item["month"] != month.zfill(2):
                continue
            if year_from is not None and item["exam_year"] < int(year_from):
                continue
            if year_to is not None and item["exam_year"] > int(year_to):
                continue
        if question is not None and item["question"] != int(question):
            continue
        if difficulty and item["difficulty"] != difficulty:
            continue
        if match_status and item["match_status"] != match_status:
            continue
        wrong_rate = item.get("wrong_rate")
        correct_rate = item.get("correct_rate")
        if wrong_min is not None and (wrong_rate is None or wrong_rate < wrong_min):
            continue
        if wrong_max is not None and (wrong_rate is None or wrong_rate > wrong_max):
            continue
        if correct_min is not None and (correct_rate is None or correct_rate < correct_min):
            continue
        if correct_max is not None and (correct_rate is None or correct_rate > correct_max):
            continue
        if text_query and text_query not in item["search_text"].lower():
            continue
        filtered.append(item)

    def rate_sort_value(item: dict, field: str, fallback: float) -> float:
        value = item.get(field)
        return float(value) if value is not None else fallback

    if sort_key == "wrong_desc":
        filtered.sort(
            key=lambda item: (
                -rate_sort_value(item, "wrong_rate", -1),
                -item["exam_year"],
                -int(item["month"]),
                item["question"],
            )
        )
    elif sort_key == "correct_asc":
        filtered.sort(
            key=lambda item: (
                rate_sort_value(item, "correct_rate", 101),
                -item["exam_year"],
                -int(item["month"]),
                item["question"],
            )
        )
    elif sort_key == "question":
        filtered.sort(
            key=lambda item: (
                item["subject"],
                item["question"],
                -item["exam_year"],
                -int(item["month"]),
            )
        )
    else:
        filtered.sort(
            key=lambda item: (
                -item["exam_year"],
                -int(item["month"]),
                item["subject"],
                item["question"],
            )
        )

    public_items = []
    for item in filtered[:limit]:
        public = {key: value for key, value in item.items() if key != "search_text"}
        public_items.append(public)

    summary = {
        "match": {},
        "difficulty": {},
    }
    for item in filtered:
        summary["match"][item["match_status"]] = summary["match"].get(item["match_status"], 0) + 1
        summary["difficulty"][item["difficulty"]] = summary["difficulty"].get(item["difficulty"], 0) + 1

    return {
        "items": public_items,
        "count": len(filtered),
        "total": len(items),
        "limit": limit,
        "available": index["available"],
        "summary": summary,
    }


def model_public_payload() -> dict:
    model = load_model()
    pooled_mapping = model.get("item_rate_mapping", {}).get("_pooled", {})
    return {
        "version": model["version"],
        "subjects": model["subjects"],
        "cuts": model["cuts"],
        "default_points": model["default_points"],
        "academy_to_national_rate": model["academy_to_national_rate"],
        "item_rate_mapping": {
            subject: {
                "method": info["method"],
                "subject_weight": info.get("subject_weight"),
                "academy_source": info["academy_source"],
                "national_source": info["national_source"],
                "coverage": info.get("coverage"),
                "usable_for_runtime_academy_conversion": info.get(
                    "usable_for_runtime_academy_conversion",
                    False,
                ),
                "counts": info["counts"],
                "pooled_counts": pooled_mapping.get("counts"),
            }
            for subject, info in model.get("item_rate_mapping", {}).items()
            if subject in model["subjects"]
        },
        "sd_model": {"cross_validation": model["sd_model"]["cross_validation"]},
        "cut_models": {
            cut: {"cross_validation": info["cross_validation"]}
            for cut, info in model["cut_models"].items()
        },
        "training_records": model["training_records"],
        "historical_anchor_count": len(model.get("historical_anchors", [])),
        "historical_exam_count": len(historical_exam_payload()["exams"]),
    }


def predict_cut(subject: str, rates: Iterable[object], points: Iterable[object], mode: str) -> dict:
    model = load_model()
    if subject not in model["subjects"]:
        raise PredictionError("지원 과목은 한국지리와 세계지리입니다.")

    raw_rates = normalize_numbers(rates, 20, "정답률")
    raw_points = normalize_numbers(points, 20, "배점")
    if any(rate < 0 or rate > 100 for rate in raw_rates):
        raise PredictionError("정답률은 0부터 100 사이여야 합니다.")
    if any(point <= 0 for point in raw_points):
        raise PredictionError("배점은 양수여야 합니다.")

    total_points = sum(raw_points)
    warnings = []
    if abs(total_points - 50) > 0.001:
        warnings.append(f"배점 합이 {total_points:g}점입니다. 탐구 표준인 50점과 다릅니다.")
    possible_scores = possible_raw_scores(raw_points)

    if mode == "academy":
        academy_rates = [
            {"value": rate, "label": f"{rate:.1f}%", "is_upper_bound": False}
            for rate in raw_rates
        ]
        national_rates = convert_academy_to_national(subject, raw_rates, model)
    elif mode == "national":
        national_rates = raw_rates
        academy_rates = convert_national_to_academy(subject, raw_rates, model)
    else:
        raise PredictionError("정답률 입력 모드를 확인해주세요.")

    features = feature_values(national_rates, raw_points)
    estimated_sd = apply_linear_model(model["sd_model"]["coefficients"], subject, features)
    features["nat_sd"] = clamp(estimated_sd, 0.1, 25.0)
    cut_caps, matched_anchors = historical_cut_caps(subject, features, model)
    predictions = {}
    for cut, cut_model in model["cut_models"].items():
        coefficients = cut_model["coefficients"]
        prediction = apply_linear_model(coefficients, subject, features)
        prediction = clamp(prediction, 0, total_points)
        historical_cap = cut_caps.get(cut)
        if historical_cap is not None:
            prediction = min(prediction, historical_cap)
        correction = runtime_bias_correction(model, mode, subject, cut)
        if correction:
            prediction = clamp(prediction - correction, 0, total_points)
        subject_cv = cut_model["cross_validation"]["by_subject"].get(
            subject,
            cut_model["cross_validation"],
        )
        rmse = subject_cv["rmse"]
        predictions[cut] = {
            "predicted_cut": prediction,
            "suggested_cut": (
                nearest_possible_score(prediction, possible_scores, total_points)
                if possible_scores
                else int(clamp(round(prediction), 0, total_points))
            ),
            "range_low": (
                lower_possible_score(math.floor(prediction - rmse), possible_scores, total_points)
                if possible_scores
                else int(clamp(math.floor(prediction - rmse), 0, total_points))
            ),
            "range_high": (
                upper_possible_score(math.ceil(prediction + rmse), possible_scores, total_points)
                if possible_scores
                else int(clamp(math.ceil(prediction + rmse), 0, total_points))
            ),
            "rmse": rmse,
            "mae": subject_cv["mae"],
            "historical_cap": historical_cap,
            "runtime_correction": correction,
        }

    conversion_rows = []
    for index, (point, national_rate, academy_rate) in enumerate(
        zip(raw_points, national_rates, academy_rates),
        start=1,
    ):
        conversion_rows.append(
            {
                "question": index,
                "points": point,
                "national_rate": national_rate,
                "academy_rate": academy_rate["value"],
                "academy_rate_label": academy_rate["label"],
                "academy_rate_is_upper_bound": academy_rate["is_upper_bound"],
            }
        )

    first_cut = predictions["1"]
    score_table = score_scale_rows(
        possible_scores,
        total_points,
        features["mean"],
        features["nat_sd"],
        predictions,
    )
    historical_comparisons = historical_matches(subject, features, predictions, model)
    return {
        "subject": subject,
        "mode": mode,
        "predictions": predictions,
        "predicted_cut": first_cut["predicted_cut"],
        "suggested_cut": first_cut["suggested_cut"],
        "range_low": first_cut["range_low"],
        "range_high": first_cut["range_high"],
        "estimated_national_rates": national_rates,
        "estimated_academy_rates": academy_rates,
        "conversion_rows": conversion_rows,
        "score_table": score_table,
        "historical_matches": historical_comparisons,
        "features": features,
        "rmse": first_cut["rmse"],
        "mae": first_cut["mae"],
        "warnings": warnings,
        "matched_historical_anchors": matched_anchors[:5],
    }
