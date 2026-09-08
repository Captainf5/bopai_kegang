"""Generate the phone attachment from authoritative repo files; do not hand-edit it."""
import argparse, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def source_paths():
    paths = [ROOT/p for p in ["SKILL.md","WORKFLOW.md","OUTPUT-FORMAT.md","CHECKLIST.md","references/README.md","references/STYLE-BENCHMARK.md","大展宏图方法论.md"]]
    paths += sorted((ROOT/"references").glob("[0-9][0-9]-*.md"))
    paths += [ROOT/p for p in ["references/LECTURER.md","references/WORKBUDDY-COURSE.md","references/COURSE-CATALOG.md","references/COMMUNICATIONS-SERIES.md","CROSS-PLATFORM.md","MOBILE-WORKFLOW.md","delivery-pack/DELIVERY-WORKFLOW.md","delivery-pack/STYLE-GUIDE-WORD.md","outputs/博AI增效-课程销售矩阵.md"]]
    paths += sorted((ROOT/'outputs/catalog').glob('*.md'), key=lambda p:p.name)
    return paths

def render():
    paths = source_paths()
    text = "# 博AI课纲·手机加载包\n\n这是由同一仓库自动汇集的读取副本，不要手工编辑。主规则优先于参考课纲。先读SKILL及输出规则，再按任务选读01与1—2份相关参考。仓库正文为唯一维护源。\n\n"
    for path in paths:
        content=path.read_text(encoding="utf-8").strip()
        text += "\n\n---\n\n## 文件："+path.relative_to(ROOT).as_posix()+"\n\n"+content+"\n"
    return text

def build(check=False):
    text=render()
    output=ROOT/"mobile/博AI课纲-手机加载包.md"
    if check:
        if not output.exists() or output.read_text(encoding="utf-8") != text:
            raise ValueError("手机包与源文件不一致，请重新生成")
        return output
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(text,encoding="utf-8")
    print("Mobile pack:",len(source_paths()),"source files;",len(text),"characters; SHA256",hashlib.sha256(text.encode()).hexdigest())
    return output
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
