# 博AI课纲 Skill

在原有仓库里维护同一套课纲规则、十份核心参考与排版模板。手机写稿不降级成简版；电脑和手机查看同一份PDF，分页一致。

[手机使用流程](MOBILE-WORKFLOW.md) · [手机排版入口](https://github.com/Captainf5/bopai_kegang/issues/new?template=course-render.yml) · [云端排版记录与下载](https://github.com/Captainf5/bopai_kegang/actions/workflows/render-course.yml)

## 本次成果

- [WorkBuddy职场办公两天课纲](outputs/WorkBuddy职场办公实战工作坊-2D.md)
- [下载带图Word](outputs/WorkBuddy职场办公实战工作坊-2D_带图.docx?raw=true) · [查看或下载PDF](outputs/WorkBuddy职场办公实战工作坊-2D_带图.pdf?raw=true)
- [Skill入口](SKILL.md)、[十份核心课纲](references/README.md)、[表达与排版标杆](references/STYLE-BENCHMARK.md)
- [课程研发方法](大展宏图方法论.md)、[交付检查表](CHECKLIST.md)
- [本次实测与验收范围](VERIFICATION.md)：最终8页PDF已逐页检查，手机与电脑使用同一个文件。

## 手机怎么用

1. 下载[手机加载包](mobile/博AI课纲-手机加载包.md)，上传到支持文件阅读的手机AI对话，说明对象、天数、主工具、场景和希望学员带走的成果。
2. 让AI按包内规则生成完整Markdown，继续语音或文字修改；确认后复制全文到“手机排版入口”。
3. 在GitHub登录仓库所有者账号提交；打开“云端排版记录与下载”，进入本次运行，在Artifacts下载文件包并解压。固定版式PDF用于查看，Word用于修改。下载包保留7天，及时保存到手机文件。

这是一条不依赖办公室电脑开机的两步AI写稿＋云端排版流程，不是“只填一句需求，GitHub自动调用模型写稿”。没有新增模型API或付费订阅。首次手机AI读取附件和手机浏览器下载体验需在所选客户端确认。

## 电脑怎么用

将整个仓库目录作为一个Skill安装到支持本地Skill的工具中；不要只复制SKILL.md。排版命令见[交付流程](delivery-pack/DELIVERY-WORKFLOW.md)。手机包由脚本生成，不手工维护另一份规则。

## 公开范围

仓库与Issue公开，只放通用课程与脱敏资料。十份核心课纲为基于已有课程的通用重编版，不公开客户原稿；旧reference-pack是历史资料，当前规则优先。排版机器人仅有代码读取权限，不自动提交文件或发布消息。人工commit记录修改，push将已授权修改同步到本仓库，不等于给客户发送消息。
