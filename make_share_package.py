#!/usr/bin/env python3
"""Build a clean team-sharing ZIP for Auto Analysis."""

from __future__ import annotations

import json
import re
import shutil
import stat
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
PACKAGE_NAME = "Auto Analysis 공유용"
PACKAGE_DIR = DIST_DIR / PACKAGE_NAME
ZIP_PATH = DIST_DIR / "Auto_Analysis_공유용.zip"
SAMPLE_ARCHIVE_TITLE = "4월 NEW"
SECRET_PATTERN = re.compile(r"AIza[0-9A-Za-z_-]{20,}")

RUNTIME_FILES = [
    "app.py",
    "split_exam_questions.py",
    "geo_cut_predictor.py",
    "geo_cut_model.json",
    "ebsi_geo_data.json",
    "classification_units.json",
    "requirements.txt",
    "start_gui.command",
    "start_gui_windows.bat",
    "prepare_windows_venv.ps1",
    "처음_읽어주세요.txt",
]

RUNTIME_DIRS = [
    "templates",
    "static",
    "design-system",
]


def copytree_clean(src: Path, dest: Path) -> None:
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def copy_text_crlf(src: Path, dest: Path) -> None:
    text = src.read_text(encoding="utf-8").replace("\r\n", "\n")
    dest.write_text(text.replace("\n", "\r\n"), encoding="utf-8")


def scrub_local_paths(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: scrub_local_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub_local_paths(item) for item in value]
    if isinstance(value, str) and ("/Users/" in value or "\\Users\\" in value):
        name = Path(value).name
        return name or "local_path_removed"
    return value


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def copy_runtime_files() -> None:
    for filename in RUNTIME_FILES:
        src = ROOT / filename
        dest = PACKAGE_DIR / filename
        if filename == "geo_cut_model.json":
            payload = read_json(src)
            payload["source_dir"] = "shared_package"
            payload["ebsi_path"] = "ebsi_geo_data.json"
            write_json(dest, payload)
        elif filename.endswith(".bat"):
            copy_text_crlf(src, dest)
        else:
            shutil.copy2(src, dest)

    shutil.copy2(ROOT / "README_공유용.md", PACKAGE_DIR / "README.md")

    for dirname in RUNTIME_DIRS:
        copytree_clean(ROOT / dirname, PACKAGE_DIR / dirname)

    copy_text_crlf(ROOT / "start_gui_windows.bat", PACKAGE_DIR / "Auto Analysis 실행 - Windows.bat")
    mac_launcher = PACKAGE_DIR / "Auto Analysis 실행 - macOS.command"
    shutil.copy2(ROOT / "start_gui.command", mac_launcher)
    mac_launcher.chmod(mac_launcher.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def sample_archive_item() -> dict[str, Any]:
    index_path = ROOT / "archives" / "index.json"
    if not index_path.exists():
        raise FileNotFoundError("archives/index.json 파일이 없어 샘플을 포함할 수 없습니다.")

    for item in read_json(index_path):
        if isinstance(item, dict) and item.get("title") == SAMPLE_ARCHIVE_TITLE:
            return item
    raise ValueError(f"'{SAMPLE_ARCHIVE_TITLE}' 샘플 아카이브를 찾지 못했습니다.")


def sanitize_archive_payload(payload: dict[str, Any], archive_id: str) -> dict[str, Any]:
    sanitized = scrub_local_paths(payload)
    sanitized["archive_dir"] = f"archives/{archive_id}"
    sanitized["snapshot_dir"] = f"archives/{archive_id}/job"
    return sanitized


def copy_sample_archive() -> None:
    item = sample_archive_item()
    archive_id = str(item["archive_id"])
    src_dir = ROOT / "archives" / archive_id
    if not src_dir.exists():
        raise FileNotFoundError(f"샘플 아카이브 폴더를 찾지 못했습니다: {src_dir}")

    package_archives = PACKAGE_DIR / "archives"
    package_archives.mkdir(parents=True, exist_ok=True)
    dest_dir = package_archives / archive_id
    copytree_clean(src_dir, dest_dir)

    archive_payload = sanitize_archive_payload(read_json(dest_dir / "archive.json"), archive_id)
    write_json(dest_dir / "archive.json", archive_payload)

    job_path = dest_dir / "job" / "job.json"
    if job_path.exists():
        job_payload = scrub_local_paths(read_json(job_path))
        job_payload["output_dir"] = f"archives/{archive_id}/job/questions"
        write_json(job_path, job_payload)

    index_payload = sanitize_archive_payload(dict(item), archive_id)
    write_json(package_archives / "index.json", [index_payload])


def assert_no_api_key() -> None:
    for path in PACKAGE_DIR.rglob("*"):
        if not path.is_file():
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if SECRET_PATTERN.search(data.decode("utf-8", errors="ignore")):
            raise ValueError(f"API 키로 보이는 문자열이 공유본에 남아 있습니다: {path}")


def zip_package() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            arcname = Path(PACKAGE_NAME) / path.relative_to(PACKAGE_DIR)
            archive.write(path, arcname)


def main() -> None:
    DIST_DIR.mkdir(exist_ok=True)
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)

    PACKAGE_DIR.mkdir(parents=True)
    copy_runtime_files()
    copy_sample_archive()
    assert_no_api_key()
    zip_package()

    print(f"공유 폴더: {PACKAGE_DIR}")
    print(f"공유 ZIP: {ZIP_PATH}")


if __name__ == "__main__":
    main()
