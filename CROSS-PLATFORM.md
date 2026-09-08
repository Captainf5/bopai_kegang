# Codex与WorkBuddy共用一个课纲Skill

Skill名称：`bopai-kegang`，显示名：博AI课纲。唯一维护源是[原仓库](https://github.com/Captainf5/bopai_kegang)，各端安装包、手机附件均由同一源文件生成。

## 电脑调用

### Codex

只写课纲可下载[轻量写作Skill包](releases/bopai-kegang-authoring.zip?raw=true)；需要本地Word排版时使用[完整Skill包](releases/bopai-kegang.zip?raw=true)。解压后保留完整的 `bopai-kegang/` 文件夹，放入用户级 `.agents/skills/`。不要只复制SKILL.md，也不要在多个发现目录重复安装同名Skill。

下一轮输入：

> 使用 $bopai-kegang，为【对象】设计【天数】的【主题】课程，主工具【】，核心场景【】，学员最后带走【成果】。每章先列关键词，完整写出讲解、演示、练习与产出；按已认可样式排版。

如技能列表尚未出现，刷新或重启客户端，再选择“博AI课纲”。无需配置新的MCP、密钥或插件。

### WorkBuddy

写稿优先导入轻量写作ZIP；需要WorkBuddy本地调用Word模板与排版脚本时再导入完整ZIP。确认技能包包含SKILL.md、references和13份`outputs/catalog`当前课纲；完整包另含delivery-pack。导入后在已安装技能中启用并选择“博AI课纲”；界面名称以当前版本为准。

> 请调用博AI课纲（bopai-kegang），为【对象】制作【天数】的【主题】课程。按技能中的写法、参考和模板完成，先列关键词，保留完整实操内容，最后交付Markdown与带图Word；不能本地导出PDF时使用仓库云端排版入口。

不要求WorkBuddy理解Codex的 `$` 选择语法，也不要求Codex调用WorkBuddy的专属接口。两者使用同一个标准SKILL.md和相对路径资源，Codex的agents/openai.yaml仅作可选界面信息。

## 手机调用与接力

先判断当前手机入口的实际能力，不把桌面端安装等同于手机端同步安装：

1. **能看到技能或访问已配置项目**：在Codex/WorkBuddy当前可用入口选择“博AI课纲”，或明确要求读取仓库中的完整Skill和所需参考。使用同一套规则。
2. **不能调用本地Skill，但能读附件**：上传[手机核心规则包](mobile/博AI课纲-手机核心规则包.md?raw=true)和一个方向包，按[MOBILE-WORKFLOW.md](MOBILE-WORKFLOW.md)写稿。附件中以“文件：路径”划分的内容就是对应资源，不要求手机打开不存在的本地路径。
3. **既不能读技能也不能读附件**：说明入口缺失，切换到支持的会话或浏览器；不要宣称已加载。仅发一句“按我的Skill”不能把规则自动传过去。

跨设备继续修改时，提供最新完整Markdown及新要求；Word/截图只作参考，不依赖另一个会话的隐含历史。手机语音只需讲清对象、时长、主题、场景和成果，缺关键方向才追问。

手机写稿后，通过[排版表单](https://github.com/Captainf5/bopai_kegang/issues/new?template=course-render.yml)提交完整Markdown，在[云端记录](https://github.com/Captainf5/bopai_kegang/actions/workflows/render-course.yml)下载Word和PDF。它不要求办公室电脑开机；若选择手机遥控桌面WorkBuddy的路线，则电脑需要保持在线。

## 维护与验收

- 仓库更新规则→重建手机核心包、方向包、全量兼容包和两档ZIP→运行测试→经授权推送。发行文件不手改，不让手机附件或安装副本反向覆盖新源文件。
- 使用新包更新已有安装前，核对是否存在本地自定义修改；有则保留并合并，不能直接覆盖。安装副本不是自动同步订阅，更新后需重新导入/同步。
- 写稿不依赖Python、Word或特定连接器；本地排版按delivery-pack的依赖运行。没有本地渲染能力时用现有云端入口，不擅自替换模板。
- Word可编辑；跨端固定分页以同一PDF为准，不能保证所有Word阅读模式不重排。
- 公开仓库与表单仅放通用、脱敏内容；发布和发送客户消息不是同一动作，均须遵守相应授权。
- 包结构校验、安装文件存在、客户端能发现、附件完整读取和实际任务成功是不同层证据，不能互相冒充。“同水准”按同一质量门槛判断，不要求不同模型逐字一致。

## 官方依据

2026-09-08核对：[Codex技能结构与加载位置](https://learn.chatgpt.com/docs/build-skills)、[WorkBuddy技能导入](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)、[WorkBuddy小程序附件与技能](https://www.codebuddy.cn/docs/workbuddymini/features/Attachments-and-Skills)。客户端版本与账号能力变化时重新核对。
