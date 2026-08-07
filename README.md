# codebase-baseline-planner

> **中文**：原项目分析、盲区发现与二次开发协作技能。在修改、DIY、重构、迁移、接手维护或继续实现已有代码库之前，先独立还原原项目、系统发现盲区与未知，经确认后形成融合的二次开发方案；同时把关键认知与决策写回项目内，方便后续交接。
>
> **English**: An AI skill for *independent codebase analysis, blind-spot discovery, and collaborative secondary-development planning*. Before modifying, refactoring, migrating, taking over, or building on an existing codebase, it first restores the original project, surfaces blind spots and unknowns, and — after your confirmation — produces a fused secondary-development plan. Key knowledge and decisions are written back into the project for handoff.

---

## 它是什么 / What is this?

在让 AI 动手改代码之前，这个技能会先**独立还原原项目**：把代码库是什么、关键模块怎么运作、有哪些隐含约定和限制风险，整理成一份可交给任何 AI Agent 或开发者阅读的**原项目认知基线**。然后系统性**发现盲区与未知**——哪些地方证据不足、哪些假设有风险、历史上踩过什么坑。之后再与你**讨论并确认二次开发方向**，最后才生成融合的改造方案。关键认知与决策会写回项目内，方便任何 AI 对话或 Agent 后续接手。

Before letting an AI touch your code, this skill first *independently restores the original project* — turning what the codebase does, how its key modules work, its implicit conventions, constraints, and risks into a **cognition baseline** any AI agent or developer can pick up. It then systematically *surfaces blind spots and unknowns*: where evidence is thin, which assumptions are risky, and what historical pitfalls exist. Only after discussing and confirming the *secondary-development direction* with you does it produce a fused plan. Key knowledge and decisions are written back into the project so any future AI session or agent can take over.

**设计原则 / Design principles**

- 先独立还原原项目，再讨论你的改造想法（restore the original project before discussing your ideas）
- 清单只保证最低覆盖，不是思考边界（checklists set the floor, never the ceiling）
- 证据优先，区分事实 / 推断 / 反馈 / 未知（evidence first — separate facts, inferences, feedback, and unknowns）
- 主动发现盲区与未知，不放过关键缺口（actively surface blind spots and unknowns）
- 保持独立判断，必要时纠正你的认知（keep independent judgment; correct misconceptions when needed）
- 未经确认不生成最终方案、不改代码（no final plan or code changes without confirmation）
- 关键认知与决策写回项目，便于交接（write key knowledge and decisions back into the project for handoff）

## 功能 / Features

| 中文 | English |
|---|---|
| 独立还原原项目，形成认知基线 | Independently restore the original project into a cognition baseline |
| 盲区发现：证据扫描 / 盲区检查 / 反向失败推演 / 范围外检查 | Blind-spot discovery: evidence scan, blind-spot check, reverse-failure reasoning, out-of-scope check |
| 保持独立判断，必要时纠正你的认知 | Keep independent judgment and correct misconceptions |
| 提交基线，讨论并确认二次开发方向 | Submit the baseline, discuss and confirm the direction |
| 融合的二次开发方案 | Fused secondary-development plan (`FUSION_PLAN.md`) |
| 决策记录（DEC-xxx） | Decision log (`DEC-xxx`) |
| 防「清单锁死」的开放式复查 | Open-ended review to prevent "checklist lock-in" |
| 辅助：关键状态写回项目，新会话可接手 | Auxiliary: write key state back into the project for handoff |

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

> 注：恢复项目记忆（阶段 -1）与写回状态（阶段 7）属于**辅助交接能力**，用于跨会话复用；技能主体是分析、盲区发现与协作规划。
>
> Note: restoring project memory (Phase −1) and writing state back (Phase 7) are *auxiliary handoff capabilities*; the core of the skill is analysis, blind-spot discovery, and collaborative planning.

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

在目标项目里，它还会建立如下**辅助交接**结构（可自定义）：

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
