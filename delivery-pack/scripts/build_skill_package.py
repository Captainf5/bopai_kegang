"""Build deterministic full and authoring-only Skill ZIPs."""

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "releases/bopai-kegang.zip"
AUTHORING_OUTPUT = ROOT / "releases/bopai-kegang-authoring.zip"

CORE = [
    "SKILL.md",
    "WORKFLOW.md",
    "OUTPUT-FORMAT.md",
    "CHECKLIST.md",
    "EXAMPLES.md",
    "大展宏图方法论.md",
    "CROSS-PLATFORM.md",
    "MOBILE-WORKFLOW.md",
    "MOBILE-PARITY-TEST.md",
    "VERSION",
    "agents/openai.yaml",
    "outputs/博AI增效-课程销售矩阵.md",
    "outputs/博AI增效-课程销售客服Q&A.md",
    "delivery-pack/DELIVERY-WORKFLOW.md",
    "delivery-pack/STYLE-GUIDE-WORD.md",
]

AUTHORING_PATTERNS = [
    "references/*.md",
    "references/*.json",
    "outputs/catalog/*.md",
    "feishu-pack/*.md",
]

FULL_PATTERNS = AUTHORING_PATTERNS + [
    "delivery-pack/*.md",
    "delivery-pack/requirements*.txt",
    "delivery-pack/课纲模板.docx",
    "delivery-pack/scripts/*.py",
    "delivery-pack/images/*.png",
    "delivery-pack/images/README.md",
]

TEXT = {".md", ".py", ".txt", ".yaml", ".json"}


def source_files(flavor="full"):
    if flavor not in {"full", "authoring"}:
        raise ValueError(f"未知Skill包类型: {flavor}")
    paths = {ROOT / relative for relative in CORE}
    patterns = FULL_PATTERNS if flavor == "full" else AUTHORING_PATTERNS
    for pattern in patterns:
        paths.update(ROOT.glob(pattern))
    for path in paths:
        if (
            not path.is_file()
            or path.is_symlink()
            or not path.resolve().is_relative_to(ROOT.resolve())
        ):
            raise ValueError(f"缺失或不安全的包资源: {path}")
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def payload(flavor="full"):
    import build_mobile_pack

    files = {}
    for path in source_files(flavor):
        if path.suffix in TEXT or path.name == "VERSION":
            data = path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        else:
            data = path.read_bytes()
        files[path.relative_to(ROOT).as_posix()] = data
    manifest = {
        "name": "bopai-kegang",
        "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "flavor": flavor,
        "source": "https://github.com/Captainf5/bopai_kegang",
        "reference_basis": "outputs/catalog",
        "basis_sha256": build_mobile_pack.course_basis_sha256(),
        "files": {
            relative: hashlib.sha256(data).hexdigest()
            for relative, data in files.items()
        },
    }
    files["PACKAGE-MANIFEST.json"] = json.dumps(
        manifest, ensure_ascii=False, indent=2
    ).encode("utf-8")
    return files


def _write(output, files):
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, data in files.items():
            info = zipfile.ZipInfo(
                "bopai-kegang/" + relative, date_time=(1980, 1, 1, 0, 0, 0)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def _check(output, files):
    with zipfile.ZipFile(output) as archive:
        expected = {"bopai-kegang/" + relative for relative in files}
        if set(archive.namelist()) != expected:
            raise AssertionError(f"包文件列表已过期: {output.name}")
        for relative, data in files.items():
            if archive.read("bopai-kegang/" + relative) != data:
                raise AssertionError(f"包内容已过期: {output.name}: {relative}")


def build(check=False):
    import build_mobile_pack

    build_mobile_pack.build(check=check)
    packages = [
        ("full", OUTPUT),
        ("authoring", AUTHORING_OUTPUT),
    ]
    summary = {}
    for flavor, output in packages:
        files = payload(flavor)
        if check:
            _check(output, files)
        else:
            _write(output, files)
        summary[flavor] = {
            "files": len(files),
            "bytes": output.stat().st_size,
            "check": check,
        }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return OUTPUT


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    build(parser.parse_args().check)
