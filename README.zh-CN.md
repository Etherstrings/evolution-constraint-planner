# Evolution Constraint Planner

[English](README.md) | 简体中文

<div align="center">

**先冻结产品含义，再把交付压进一个有约束的 plan-code-achieve 闭环。**

![Codex First](https://img.shields.io/badge/Codex-First-412991?style=flat-square)
![Constraint Planning](https://img.shields.io/badge/Planning-Constraint_Driven-0F766E?style=flat-square)
![CLI Toolkit](https://img.shields.io/badge/CLI-Toolkit-1D4ED8?style=flat-square)
![Plan Code Achieve](https://img.shields.io/badge/Workflow-Plan_Code_Achieve-7C3AED?style=flat-square)

原始需求 -> 冻结含义 -> code-ready handoff -> run evidence -> achieve verdict

[赞助支持](#support)

</div>

`evolution-constraint-planner` 是一套以 Codex 为核心的 Skill 与工具链，用来把一条原始需求压成一个有约束的交付闭环：

1. `pre` 负责追问和整理，直到需求语义足够冻结，可以进入审批门。
2. `plan` 负责让保留下来的路径收敛成一个 code-ready bundle。
3. `code` 只能从冻结后的 handoff 执行，不允许重新发明产品含义。
4. `achieve` 负责判断结果是否真的满足验收，以及这个 case 是否可以归档关闭。

它的核心原则很简单：规划负责冻结含义，编码负责忠实执行，闭环负责证明结果是否可接受。只要编码阶段还需要补产品语义，说明规划失败了。

## <a id="support"></a>赞助支持

如果 ECL 对你的 Codex 工作流有帮助，欢迎通过 GitHub Sponsors 支持后续维护：

- GitHub Sponsors: https://github.com/sponsors/Etherstrings

## 这个仓库包含什么

- `SKILL.md`：生产可用的 Codex Skill 本体。
- `scripts/`：用于 scaffold、render、validate、run 记录、achieve note 的 CLI 辅助脚本。
- `templates/`：bundle 各类产物的 markdown 模板。
- `schemas/`：normalized case 的结构说明。
- `references/`：playbook、质量门槛、子代理协议。
- `docs/`：理论、阶段、子代理、实现细节文档。
- `examples/`：一套可通过校验的 Stage A 示例工作区。
- `tests/`：公开仓库 smoke tests。

## 为什么要做 ECL

大多数 agent 工作流会在两个地方失真：

- 前面问得太少，后面编码阶段开始偷偷补行为
- 规划一直不肯冻结，导致每个阶段都在重新解释产品

ECL 的做法是把交付过程当成一个带约束的编译链：

- raw request -> normalized case
- normalized case -> staged bundle
- staged bundle -> code handoff
- code handoff -> run evidence
- run evidence -> achieve verdict

这个 bundle 不是一堆随手笔记，而是控制下一阶段能否继续的真值面。

## Codex 安装方式

先 clone 仓库，再把它安装进 Codex skills 目录：

```bash
git clone https://github.com/Etherstrings/evolution-constraint-planner.git
cd evolution-constraint-planner
./scripts/install_skill.sh
```

默认会安装到：

```text
${CODEX_HOME:-$HOME/.codex}/skills/evolution-constraint-planner
```

也可以手动覆盖安装根目录：

```bash
CODEX_HOME=/tmp/codex-home ./scripts/install_skill.sh
```

## CLI 快速开始

CLI 本身是薄工具层，负责渲染、校验和记录。真正的推理行为仍由遵循这个 Skill 的模型承担。

从原始需求初始化 Stage A：

```bash
python3 scripts/ecl.py pre \
  --request "Build a minimal app with a dashboard, an empty state, and one write flow." \
  --output /abs/path/to/bundle \
  --repo-path /abs/path/to/repo \
  --project-path /abs/path/to/repo
```

在 approval gate 完成之后，渲染 post-approval bundle：

```bash
python3 scripts/ecl.py plan \
  --input-json /abs/path/to/case.json \
  --output /abs/path/to/bundle \
  --force
```

记录一次 `/code` 执行：

```bash
python3 scripts/ecl.py code \
  --case /abs/path/to/bundle \
  --run-json /abs/path/to/run.json
```

渲染最终 achieve 判定：

```bash
python3 scripts/ecl.py achieve --case /abs/path/to/bundle
```

## Codex 侧的必要能力

这个仓库是明确按 Codex-first 来设计的，所以默认假设：

- 环境可以把一个目录里的 `SKILL.md` 作为 Codex skill 加载
- 模型可以读本地文件、执行本地脚本
- 环境支持真实 spawned subagents

如果你的运行环境不能拉起真实子代理，那么 ECL 仍然可以被阅读和参考，但 D、G、H、J 这几个阶段就不能被诚实地标记为 complete。

## 仓库导览

- [docs/zh-CN/theory.md](docs/zh-CN/theory.md)：ECL 的理论源头、定位和要解决的问题
- [docs/zh-CN/stages.md](docs/zh-CN/stages.md)：每个阶段的职责、输入输出、exit gate 和失败方式
- [docs/zh-CN/subagents.md](docs/zh-CN/subagents.md)：哪些阶段必须启用真实子代理、返回协议是什么
- [docs/zh-CN/implementation.md](docs/zh-CN/implementation.md)：CLI 流程、bundle 编译、模板、schema 与 OpenSpec 输出
- [examples/README.zh-CN.md](examples/README.zh-CN.md)：如何阅读示例工作区

## 示例工作区

仓库附带一套可通过 validator 的 Stage A 示例：

- [examples/stage-a-sample/case.json](examples/stage-a-sample/case.json)
- [examples/stage-a-sample/bundle/00-overview.md](examples/stage-a-sample/bundle/00-overview.md)
- [examples/stage-a-sample/bundle/98-j-compile-for-code.md](examples/stage-a-sample/bundle/98-j-compile-for-code.md)
- [examples/stage-a-sample/bundle/99-code-handoff.md](examples/stage-a-sample/bundle/99-code-handoff.md)

示例中的路径已经统一替换为占位式绝对路径，方便公开展示而不泄露本地环境信息。

## 验证方式

运行公开仓库的 smoke tests：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

直接校验仓库内附带的示例 bundle：

```bash
python3 scripts/validate_ecl_bundle.py examples/stage-a-sample/bundle
```

## 许可证

[MIT](LICENSE)
