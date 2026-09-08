import hashlib, re, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'outputs/catalog'
BASELINE={1:'93ff0e8040767e206456a71138bfeedc860f825f290f3aa487d8bb0b573aa4c2',
          2:'835c10c831ae5925831d7e21c9c33bc75697b3d860d597115e4f1b5a78b1ea03'}

class CatalogTests(unittest.TestCase):
    def test_workbuddy_body_unchanged(self):
        for days,digest in BASELINE.items():
            p=CAT/f'博AI增效-{days}D-10倍职场办公_6X畅销版.md'
            body=p.read_text(encoding='utf-8').split('\n',1)[1]
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(),digest)

    def test_catalog_names_and_complete_modules(self):
        files=list(CAT.glob('*.md')); self.assertEqual(len(files),10)
        for path in files:
            text=path.read_text(encoding='utf-8')
            self.assertEqual(text.splitlines()[0],'# '+path.stem)
            self.assertTrue(path.name=='博AI增效-OPC实战工作坊.md' or re.fullmatch(r'博AI增效-[12]D-.+_6X(畅销|数据|高管|极速|进阶|飞书|垂直)版.md',path.name))
            for section in ['一、主讲人介绍','二、本课程说明','三、课程大纲','四、课程产出','五、课件展示','六、课程现场','七、课后准备','八、培训准备']:
                self.assertIn('## '+section,text)
            modules=re.split(r'\*\*(?:模块\d+|加餐)：',text)[1:]
            for block in modules:
                keys=['关键词：','讲解要点：','演示：','学员练习：','产出物：']
                positions=[block.index(k) for k in keys]
                self.assertEqual(positions,sorted(positions),path.name)

    def test_schedules_have_breaks_and_match_modules(self):
        for path in CAT.glob('*.md'):
            text=path.read_text(encoding='utf-8')
            rows=re.findall(r'^\| (\d{2}:\d{2})—(\d{2}:\d{2}) \|',text,re.M)
            slots=re.findall(r'\*\*(?:模块\d+|加餐)：[^\n]*｜(\d{2}:\d{2})—(\d{2}:\d{2})\*\*',text)
            self.assertEqual(rows,slots,path.name)
            number=lambda t:int(t[:2])*60+int(t[3:])
            ends=[];last=None
            for a,b in rows:
                a,b=number(a),number(b); self.assertGreater(b,a)
                if last is not None:
                    if a<last:
                        self.assertEqual(last,1050); self.assertEqual(a,540); ends.append(last)
                    else: self.assertIn(a-last,[15,120])
                last=b
            self.assertEqual(last,1050)
            self.assertEqual(len(ends)+1,2 if '-2D-' in path.name else 1)

    def test_matrix_links_resolve(self):
        matrix=ROOT/'outputs/博AI增效-课程销售矩阵.md'
        links=re.findall(r'\]\((catalog/[^)]+\.md)\)',matrix.read_text(encoding='utf-8'))
        self.assertEqual(len(links),10)
        for link in links: self.assertTrue((matrix.parent/link).is_file())
