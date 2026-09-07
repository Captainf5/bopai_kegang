# 课纲交付流程

## 手机

按根目录[MOBILE-WORKFLOW.md](../MOBILE-WORKFLOW.md)操作：手机AI读取同源加载包并写稿，GitHub表单接收完整Markdown，Actions生成Word和PDF下载包。无需本地Word或电脑开机。

## 电脑

安装依赖 `pip install -r delivery-pack/requirements.txt`。

生成Word：

```bash
python delivery-pack/scripts/课纲排版toWord带图版.py --input "课纲.md"
```

模板为同目录的“课纲模板.docx”，由用户认可样稿去除客户正文、缩略图与个人元数据派生；保留样式、主题和编号。图片均与仓库已有公开素材逐字节核对。

本地PDF助手仍支持已安装Word的环境：

```bash
python delivery-pack/scripts/docx_to_pdf.py --input "课纲_带图.docx"
```

若Word启动失败，不把本地导出能力当作移动流程依赖；直接使用云端排版。云端Linux使用requirements-cloud.txt、LibreOffice和Noto中文字体，不依赖Windows COM。

## 一致性与检查

同一份MD＋Skill＋模板生成Word，再统一导出PDF。手机和电脑都看此PDF，不能分别导出再比较。Word可编辑，手机阅读模式可能重排。

正式交付前检查全部页面；修改内容或版式后重新渲染。清单与规则见根目录CHECKLIST.md。下载包内render-result.json记录PDF页数和SHA256，仅用于内部校验，不写进客户正文。
