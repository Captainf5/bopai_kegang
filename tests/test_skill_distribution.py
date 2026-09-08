import hashlib, importlib.util, json, re, sys, tempfile, unittest, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'delivery-pack/scripts'
sys.path.insert(0,str(SCRIPTS))
import build_mobile_pack, build_skill_package

class DistributionTests(unittest.TestCase):
    def test_mobile_copy_matches_all_sources(self):
        build_mobile_pack.build(check=True)
        text=build_mobile_pack.render()
        for source in build_mobile_pack.source_paths():
            self.assertIn(source.read_text(encoding='utf-8').strip(),text)

    def test_zip_matches_sources_and_excludes_unrelated_files(self):
        paths=[p.relative_to(ROOT).as_posix() for p in build_skill_package.source_files()]
        self.assertEqual(paths,sorted(paths))
        build_skill_package.build(check=True)
        with zipfile.ZipFile(build_skill_package.OUTPUT) as archive:
            names=archive.namelist()
            self.assertTrue(all(p.startswith('bopai-kegang/') and '..' not in Path(p).parts for p in names))
            self.assertEqual(sum(bool(re.search(r'/references/\d{2}-.*\.md$',p)) for p in names),10)
            self.assertFalse(any('/reference-pack/' in p or '/.git/' in p or p.endswith('.pdf') for p in names))
            manifest=json.loads(archive.read('bopai-kegang/PACKAGE-MANIFEST.json'))
            for path,digest in manifest['files'].items():
                self.assertEqual(hashlib.sha256(archive.read('bopai-kegang/'+path)).hexdigest(),digest)

    def test_fresh_unpacked_skill_can_render_without_author_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(build_skill_package.OUTPUT) as archive:
                archive.extractall(tmp)
            package=Path(tmp)/'bopai-kegang'
            spec=importlib.util.spec_from_file_location('portable_layout',package/'delivery-pack/scripts/课纲排版toWord带图版.py')
            renderer=importlib.util.module_from_spec(spec); spec.loader.exec_module(renderer)
            for days in [1,2]:
                source=package/f'outputs/WorkBuddy职场办公实战工作坊-{days}D.md'
                target=Path(tmp)/f'{days}D.docx'
                renderer.convert_md_to_docx(source,target)
                self.assertGreater(target.stat().st_size,10000)
            entry=(package/'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('name: bopai-kegang',entry)
            self.assertNotRegex(entry,r'[CDE]:[/\\]')
