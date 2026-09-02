from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "legislative" / "2026" / "affiliations"
URL = "https://www.servel.cl/wp-content/uploads/2025/11/PRELIMINARES_DIPUTADOS.zip"


def decode_preview(data: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "latin-1", "cp1252"):
        try:
            return encoding, data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return "binary", ""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 conoce-a-tu-parlamentario/2.0"})
    response = session.get(URL, timeout=90)
    response.raise_for_status()
    archive = zipfile.ZipFile(io.BytesIO(response.content))

    files = []
    for info in archive.infolist():
        if info.is_dir():
            continue
        raw = archive.read(info.filename)
        encoding, decoded = decode_preview(raw[:12000])
        lines = [line for line in decoded.splitlines() if line.strip()][:8]
        files.append({
            "name": info.filename,
            "size": info.file_size,
            "encoding_guess": encoding,
            "preview": lines,
        })

    diagnostics = {
        "source_url": URL,
        "download_bytes": len(response.content),
        "files": files,
    }
    (OUT / "servel_2025_zip_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
