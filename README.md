# codebase-baseline-planner

> **中文**：代码库认知基线、持久化记忆与二次开发规划技能。在修改、DIY、重构、迁移、接手维护或继续实现已有代码库之前，建立并持续维护可追溯的「项目认知基线与交接记忆」。
>
> **English**: An AI skill that builds and continuously maintains a traceable *project cognition baseline & handoff memory* before you modify, refactor, migrate, take over, or keep building on an existing codebase.

---

## 它是什么 / What is this?

在让 AI 动手改代码之前，这个技能会先帮你在项目里建立一份「给 AI 自己看的项目档案」：代码库是什么、关键模块怎么运作、做过什么决定、改到哪一步了。这份档案存放在项目内部（如 `docs/ai-project/`），这样**任何 AI 对话或 Agent 以后都能快速接手**，不用从头再读一遍整个代码库。

Before letting an AI touch your code, this skill establishes a *project memory* inside the repository — what the codebase is, how key modules work, which decisions were made, and how far an implementation has gotten. Because the memory lives **inside the project** (`docs/ai-project/`), any future AI session or agent can pick up where the last one left off without re-reading the whole codebase.

**设计原则 / Design principles**

- 先恢复已有记忆，再扫描代码（restore memory before scanning code）
- 先核对版本，再信任文档（verify the revision before trusting the docs）
- 证据优先，区分事实 / 推断 / 反馈 / 未知（evidence first — separate facts, inferences, feedback, and unknowns）
- 先还原原项目，再讨论你的改造想法（understand the original project before fusing your ideas）
- 未经确认不生成最终方案、不改代码（no final plan or code changes without confirmation）
- 把状态写回项目，不依赖聊天记录（write state back into the project, never rely on chat logs）

## 功能 / Features

| 中文 | English |
|---|---|
| 项目记忆恢复与新鲜度判断 | Restore project memory and judge whether it is still fresh |
| 增量复查，避免重复全量扫描 | Incremental review instead of repeated full rescans |
| 决策记录（DEC-xxx） | Decision log (`DEC-xxx`) |
| 融合方案（FUSION_PLAN） | Fusion plan (`FUSION_PLAN.md`) |
| 实施状态跟踪（IMP-xxx） | Implementation status tracking (`IMP-xxx`) |
| 交接文档，新对话无缝接手 | Handoff docs so a new session can take over seamlessly |
| 防「清单锁死」的开放式复查 | Open-ended review to prevent "checklist lock-in" |

## 安装 / Installation

这是一个 **OpenAI Agent Skills** 格式的技能（`SKILL.md` + `agents/openai.yaml`），兼容 Codex / ChatGPT / Claude Code 等支持 SKILL.md 的环境。

This is an **OpenAI Agent Skills** format skill (`SKILL.md` + `agents/openai.yaml`), compatible with Codex / ChatGPT / Claude Code and any environment that supports `SKILL.md`.

### Codex / ChatGPT（OpenAI）

```bash
git clone https://github.com/sodanyx/codebase-baseline-planner.git \
  ~/.codex/skills/codebase-baseline-planner
```

> 在 Windows 上，`~` 指你的用户目录（如 `C:\Users\你的用户名\`），上面命令可替换为：
> `git clone https://github.com/sodanyx/codebase-baseline-planner.git "C:\Users\你的用户名\.codex\skills\codebase-baseline-planner"`

### Claude Code

```bash
git clone https://github.com/sodanyx/codebase-baseline-planner.git \
  ~/.claude/skills/codebase-baseline-planner
```

安装后，当任务涉及「了解 / 修改 / 重构 / 迁移一个已有代码库」时，技能会自动触发。

Once installed, the skill auto-triggers when a task involves *understanding, modifying, refactoring, or migrating an existing codebase*.

## 使用方法 / Usage

安装后无需手动调用 —— 直接描述你的任务即可。技能会自动执行阶段化工作流：

Once installed there is no manual invocation — just describe your task. The skill runs a phased workflow automatically:

```
阶段 -1  恢复项目记忆并判断新鲜度     Restore memory & check freshness
阶段 0   确认调查对象和证据范围       Confirm scope & evidence sources
阶段 1   生成项目特定覆盖图           Build a project-specific coverage map
阶段 2   调查或增量更新原项目         Investigate or incrementally update
阶段 3   执行盲区发现                 Run blind-spot discovery
阶段 4   保存原项目认知基线并暂停     Save baseline, then pause
阶段 5   讨论用户想法并维护决策记录   Discuss ideas & keep decisions
阶段 6   确认后保存融合方案           Save fusion plan after confirmation
阶段 7   实施并持续更新交接状态       Implement & keep handoff status fresh
```

### 配套脚本 / Helper script

需要一个可选的 Python 3 环境（用于初始化和检查项目记忆结构）：

An optional Python 3 environment is used to initialize and validate the project-memory structure:

```bash
python scripts/project_memory.py status  --project-root <你的项目目录>
python scripts/project_memory.py init    --project-root <你的项目目录>
python scripts/project_memory.py validate --project-root <你的项目目录>
```

> 脚本只负责创建 / 校验记忆文件骨架，**不做分析**，也不会覆盖已有文档。

## 目录结构 / Project structure

```
codebase-baseline-planner/
├── SKILL.md                     # 技能主文档（入口） / Skill main document (entry point)
├── agents/
│   └── openai.yaml              # OpenAI 平台配置（chatgpt/codex/api/atlas）
├── assets/
│   └── icon.svg                 # 技能图标 / Skill icon
├── references/
│   ├── analysis-framework.md    # 深度分析框架 / Deep-analysis framework
│   ├── persistence-protocol.md  # 记忆读写协议 / Memory persistence protocol
│   └── report-templates.md      # 文档模板 / Report templates
├── scripts/
│   └── project_memory.py        # 记忆骨架初始化/校验脚本 / Memory scaffold script
├── LICENSE
└── README.md
```

在目标项目里，它会建立如下记忆结构（可自定义）：

Inside the target project it scaffolds this memory layout (customizable):

```text
AI_PROJECT_CONTEXT.md              # 稳定入口 / Stable entry point
docs/ai-project/
├── state.json
├── BASELINE.md                    # 认知基线 / Baseline
├── DECISIONS.md                   # 决策记录 / Decisions
├── FUSION_PLAN.md                 # 融合方案 / Fusion plan
├── IMPLEMENTATION_STATUS.md       # 实施状态 / Implementation status
└── CHANGELOG.md
```

## 要求 / Requirements

- Python 3.x（仅脚本需要，非必需）/ Python 3.x (only for the helper script, optional)
- Git（仅安装时克隆用）/ Git (only for cloning)

## 开源协议 / License

[MIT](LICENSE) © 2026 sodanyx

## 反馈与支持 / Feedback

如果你发现 Bug、有改进建议，或者想贡献代码，欢迎提交 [Issue](https://github.com/sodanyx/codebase-baseline-planner/issues) 或 Pull Request。

If you find a bug, have a suggestion, or want to contribute, feel free to open an [Issue](https://github.com/sodanyx/codebase-baseline-planner/issues) or a Pull Request.
