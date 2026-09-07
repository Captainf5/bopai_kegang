"""Generate the phone attachment from authoritative repo files; do not hand-edit it."""
import hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def build():
    paths = [ROOT/p for p in ["SKILL.md","WORKFLOW.md","OUTPUT-FORMAT.md","CHECKLIST.md","references/README.md","references/STYLE-BENCHMARK.md","大展宏图方法论.md"]]
    paths += sorted((ROOT/"references").glob("[0-9][0-9]-*.md"))
    text = "# 博AI课纲·手机加载包\n\n这是由同一仓库自动汇集的读取副本，不要手工编辑。主规则优先于参考课纲。先读SKILL及输出规则，再按任务选读01与1—2份相关参考。仓库正文为唯一维护源。\n\n"
    for path in paths:
        content=path.read_text(encoding="utf-8").strip()
        text += "\n\n---\n\n## 文件："+path.relative_to(ROOT).as_posix()+"\n\n"+content+"\n"
    output=ROOT/"mobile/博AI课纲-手机加载包.md"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(text,encoding="utf-8")
    print("Mobile pack:",len(paths),"source files;",len(text),"characters; SHA256",hashlib.sha256(text.encode()).hexdigest())
    return output
if __name__ == "__main__": build()
