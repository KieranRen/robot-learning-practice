# 我的机器人学习实践

这个仓库保存个人练习、笔记、进度与可复现证据。默认教材参考副本放在相邻的 `knowledge/`，公共贡献使用单独的 `contribution/`。需要同时使用不同教材版本时，分别保留固定版本的参考副本，在 `progress.md` 中记录每项任务的实际来源和相对副本目录。

## 教材来源

首次复制后核对以下默认来源和标签，填写实际完整 commit，作为初始复制记录。若使用其他版本，按实际来源修改，不能沿用未经核对的默认值。教材更新时保留旧记录，在 `progress.md` 追加新版本；同时学习多个目标时，各任务记录自己的教材版本与运行条件。

| 项目 | 记录 |
| --- | --- |
| 上游仓库或共享来源 | [noBug01/Robot_knowledge_study](https://github.com/noBug01/Robot_knowledge_study)，私有教材来源，复制后核对 |
| 教材 tag | 首版默认 v0.1.0，使用 git -C ../knowledge describe --tags --exact-match 核对；明确使用未打标签的修订时写无 tag |
| 教材完整 commit | 待填写，可用 git -C ../knowledge rev-parse HEAD 查询 |
| 复制内容 | examples/hello_robot.py、tests/test_hello_robot.py、environment.yml、实验报告模板和工作区模板 |
| 许可证 | 从教材保留的 LICENSE |

## 开始工作

命令在本仓库根目录运行。环境不存在时先创建，已有环境按学习流程确认用途和版本。

```bash
conda env create -f environment.yml
conda activate robot_manipulation_learning
python examples/hello_robot.py
python -m pytest
```

上述命令对应初始 M0 工作区。其他任务按其实际说明使用环境和运行入口。如果使用不同的环境名，在 `progress.md` 和环境报告中记录实际名称。不得通过更新同名环境意外改变另一项正在进行的任务，顶部环境摘要也不能替代逐任务记录。

## 个人记录

- `progress.md` 保存可并行的目标，以及逐任务 ID、教材来源与参考副本、版本、运行条件、状态、证据、评审和下一步
- `experiments/environment_reports/` 保存环境报告和复现说明
- `examples/` 与 `tests/` 保存个人实现及对应测试
- `AGENTS.md` 规定 AI 在这个个人仓库中的工作范围

从教材复制文件后保留来源、原有版权声明和适用许可证。个人结果经过整理与 Review，具有公共复用价值时，可从当前上游 `main` 建立贡献分支并提议 PR。

本工作区含从私有教材复制的内容。需要个人 GitHub 远程时创建私有仓库，保持教材授权的访问范围；独立仓库不会自动继承上游权限。对外分享前确认相关内容可以公开。向知识库贡献时，按实际权限选择已授权协作分支或允许的私有 Fork。

旧版模板中已经填写的内容和验收继续保留，需要新字段时追加表格或说明。不要用新模板覆盖个人记录，也不要把当前环境补写成未经核实的历史环境。同一参考副本在一个时点只对应一个当前提交，切换前确认仍在进行的任务是否依赖它。
