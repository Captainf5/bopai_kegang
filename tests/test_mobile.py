import importlib.util, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cloud",ROOT/"delivery-pack/scripts/cloud_render.py")
cloud = importlib.util.module_from_spec(spec); spec.loader.exec_module(cloud)
class MobileInputTests(unittest.TestCase):
    def event(self):
        md = (ROOT/"outputs/WorkBuddy职场办公实战工作坊-2D.md").read_text(encoding="utf-8")
        return {"repository":{"owner":{"login":"owner"}},"sender":{"login":"owner"},
                "issue":{"number":123,"user":{"login":"owner"},"title":"[课纲排版] test",
                         "body":"### 课纲 Markdown\n\n"+md+"\n\n### 发布确认\n\n- [X] "+cloud.ACK}}
    def test_preserves_complete_markdown(self):
        text,n=cloud.issue_markdown(self.event())
        self.assertIn("第二天",text); self.assertIn("培训准备",text); self.assertEqual(n,123)
    def test_rejects_other_user(self):
        event=self.event(); event["sender"]["login"]="stranger"
        with self.assertRaises(ValueError): cloud.issue_markdown(event)
    def test_requires_public_ack(self):
        event=self.event(); event["issue"]["body"]=event["issue"]["body"].replace("[X]","[ ]")
        with self.assertRaises(ValueError): cloud.issue_markdown(event)
    def test_markdown_is_not_executed(self):
        event=self.event(); event["issue"]["body"]=event["issue"]["body"].replace("## 八、", "$(touch SHOULD_NOT_EXIST)\n\n## 八、")
        text,n=cloud.issue_markdown(event)
        self.assertIn("$(touch SHOULD_NOT_EXIST)",text)
        self.assertFalse((ROOT/"SHOULD_NOT_EXIST").exists())
    def test_rejects_one_line_request(self):
        event=self.event(); event["issue"]["body"]="### 课纲 Markdown\n\n# 帮我做课纲\n\n### 发布确认\n\n- [X] "+cloud.ACK
        with self.assertRaises(ValueError): cloud.issue_markdown(event)
if __name__ == "__main__": unittest.main()
