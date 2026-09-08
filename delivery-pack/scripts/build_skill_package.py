"""Build one portable Skill ZIP from an explicit public-resource allowlist."""
import argparse, hashlib, json, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT/'releases/bopai-kegang.zip'
CORE = ['SKILL.md','WORKFLOW.md','OUTPUT-FORMAT.md','CHECKLIST.md','EXAMPLES.md',
        '大展宏图方法论.md','CROSS-PLATFORM.md','MOBILE-WORKFLOW.md','VERSION',
        'agents/openai.yaml','mobile/博AI课纲-手机加载包.md',
        'outputs/WorkBuddy职场办公实战工作坊-1D.md',
        'outputs/WorkBuddy职场办公实战工作坊-2D.md']
PATTERNS = ['references/*.md','feishu-pack/*.md','delivery-pack/*.md',
            'delivery-pack/requirements*.txt','delivery-pack/课纲模板.docx',
            'delivery-pack/scripts/*.py','delivery-pack/images/*.png','delivery-pack/images/README.md']
TEXT = {'.md','.py','.txt','.yaml'}

def source_files():
    paths = {ROOT/p for p in CORE}
    for pattern in PATTERNS:
        paths.update(ROOT.glob(pattern))
    for path in paths:
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f'缺失或不安全的包资源: {path.name}')
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())

def payload():
    files = {}
    for path in source_files():
        # Normalize text so Windows and cloud checkout produce equivalent bundles.
        data = path.read_text(encoding='utf-8').encode('utf-8') if path.suffix in TEXT or path.name=='VERSION' else path.read_bytes()
        files[path.relative_to(ROOT).as_posix()] = data
    manifest = {'name':'bopai-kegang','version':(ROOT/'VERSION').read_text().strip(),
                'source':'https://github.com/Captainf5/bopai_kegang',
                'files':{p:hashlib.sha256(data).hexdigest() for p,data in files.items()}}
    files['PACKAGE-MANIFEST.json'] = json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8')
    return files

def build(check=False, output=OUTPUT):
    import build_mobile_pack
    build_mobile_pack.build(check=True)
    files=payload()
    if check:
        with zipfile.ZipFile(output) as archive:
            assert set(archive.namelist())=={'bopai-kegang/'+p for p in files}, '包文件列表已过期'
            for path,data in files.items():
                assert archive.read('bopai-kegang/'+path)==data, f'包内容已过期: {path}'
    else:
        output.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for path,data in files.items():
                info=zipfile.ZipInfo('bopai-kegang/'+path, date_time=(1980,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644 << 16
                archive.writestr(info,data)
    print(f'Portable Skill: {len(files)} files; {output.stat().st_size} bytes; check={check}')
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
