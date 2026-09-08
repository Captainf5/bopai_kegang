"""Cloud rendering only: no model calls and no execution of submitted Markdown."""
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "outputs/catalog/博AI增效-2D-10倍职场办公_6X畅销版.md"
ACK = "我确认课纲不含客户机密或个人敏感信息，并同意公开课纲与生成文件。"

def issue_markdown(event):
    owner = event["repository"]["owner"]["login"]
    issue = event["issue"]
    if event["sender"]["login"] != owner or issue["user"]["login"] != owner:
        raise ValueError("仅仓库所有者可以使用公开排版入口")
    if not issue["title"].startswith("[课纲排版]"):
        raise ValueError("不是课纲排版请求")
    body = issue.get("body") or ""
    if "- [x] " + ACK not in body.lower():
        raise ValueError("未确认公开范围")
    marker = "### 课纲 Markdown\n\n"
    if marker not in body or "\n### 发布确认" not in body:
        raise ValueError("请使用仓库课纲排版表单")
    content = body.split(marker, 1)[1].rsplit("\n### 发布确认", 1)[0].strip()
    fence = chr(96)*3
    if content.startswith(fence) and content.endswith(fence):
        content = content.split("\n", 1)[1].rsplit(fence, 1)[0].strip()
    if not content.startswith("# ") or len(content) < 300 or len(content) > 60000:
        raise ValueError("请提交完整课纲Markdown（300—60000字符），而非一句需求")
    return content, int(issue["number"])

def convert_pdf(docx, pdf, soffice):
    binary = shutil.which(soffice) if not Path(soffice).is_absolute() else soffice
    if not binary:
        raise RuntimeError("缺少云端LibreOffice；请使用GitHub Actions排版入口")
    with tempfile.TemporaryDirectory(prefix="bopai-render-") as tmp:
        tmp = Path(tmp)
        result = subprocess.run([str(binary), "-env:UserInstallation="+(tmp/"profile").as_uri(),
            "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(docx.resolve())],
            capture_output=True, text=True, timeout=180)
        generated = tmp / (docx.stem + ".pdf")
        if result.returncode != 0 or not generated.exists() or generated.stat().st_size < 1000:
            raise RuntimeError("PDF转换失败: "+result.stderr[-500:])
        shutil.copyfile(generated, pdf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path)
    parser.add_argument("--soffice", default="soffice")
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    if args.event:
        content, number = issue_markdown(json.loads(args.event.read_text(encoding="utf-8")))
        dest = ROOT / "outputs/requests" / ("issue-"+str(number))
        dest.mkdir(parents=True, exist_ok=True)
        md = dest / "course.md"
        md.write_text(content+"\n", encoding="utf-8")
    else:
        md = (args.input or SAMPLE).resolve()
    docx = md.with_name(md.stem+"_带图.docx")
    pdf = docx.with_suffix(".pdf")
    spec = importlib.util.spec_from_file_location("layout", Path(__file__).with_name("课纲排版toWord带图版.py"))
    layout = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(layout)
    layout.convert_md_to_docx(md, docx)
    convert_pdf(docx, pdf, args.soffice)
    import pypdfium2
    document = pypdfium2.PdfDocument(pdf)
    pages = len(document)
    text = "\n".join(page.get_textpage().get_text_range() for page in document)
    if pages == 0 or "课程" not in text:
        raise ValueError("PDF正文检查失败")
    manifest = {"files":[str(p.relative_to(ROOT)).replace("\\","/") for p in [md,docx,pdf]],
                "pages":pages, "pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest()}
    Path("render-result.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False))

if __name__ == "__main__":
    main()
