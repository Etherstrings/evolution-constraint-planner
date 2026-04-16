# Evolution Constraint Planner

English | [简体中文](README.zh-CN.md)

<div align="center">

**Freeze product meaning before coding starts, then drive delivery through a constrained plan-code-achieve loop.**

![Codex First](https://img.shields.io/badge/Codex-First-412991?style=flat-square)
![Constraint Planning](https://img.shields.io/badge/Planning-Constraint_Driven-0F766E?style=flat-square)
![CLI Toolkit](https://img.shields.io/badge/CLI-Toolkit-1D4ED8?style=flat-square)
![Plan Code Achieve](https://img.shields.io/badge/Workflow-Plan_Code_Achieve-7C3AED?style=flat-square)

Raw request -> frozen meaning -> code-ready handoff -> run evidence -> achieve verdict

[Codex Installation](#codex-installation) · [CLI Quick Start](#cli-quick-start) · [Support](#support)

</div>

`evolution-constraint-planner` is a Codex-first skill and toolkit for turning a raw request into a constrained delivery loop:

1. `pre` interrogates the request until meaning is frozen enough to approve.
2. `plan` converges the retained path into a code-ready bundle.
3. `code` executes only from the frozen handoff.
4. `achieve` decides whether the result actually met acceptance and whether the case can be archived.

The core idea is simple: planning owns meaning, coding owns execution, and closure owns acceptance. If the coding model still has to invent product semantics, planning failed.

## <a id="support"></a>Support

If ECL helps your Codex workflow, you can support ongoing maintenance via GitHub Sponsors:

- GitHub Sponsors: https://github.com/sponsors/Etherstrings

## What This Repository Contains

- `SKILL.md`: the production Codex skill.
- `scripts/`: CLI helpers for scaffold, render, validate, run recording, and achieve notes.
- `templates/`: markdown templates for bundle artifacts and stage notes.
- `schemas/`: structured schema guidance for the normalized case format.
- `references/`: playbooks, quality bars, and subagent protocol.
- `docs/`: technical documentation for the theory, stages, subagents, and implementation.
- `examples/`: a validator-passing Stage A sample workspace.
- `tests/`: smoke tests for the public repo.

## Why ECL Exists

Most agentic workflows fail in one of two ways:

- they ask too few questions up front, so coding silently invents behavior later
- they keep product interpretation open for too long, so every later stage drifts

ECL solves that by treating delivery like a constrained compilation pipeline:

- raw request -> normalized case
- normalized case -> staged bundle
- staged bundle -> code handoff
- code handoff -> run evidence
- run evidence -> achieve verdict

The bundle is not just notes. It is the truth surface that decides whether the next stage is allowed to proceed.

## Codex Installation

Clone the repository and install it into your Codex skills directory:

```bash
git clone https://github.com/Etherstrings/evolution-constraint-planner.git
cd evolution-constraint-planner
./scripts/install_skill.sh
```

By default the installer copies the repository to:

```text
${CODEX_HOME:-$HOME/.codex}/skills/evolution-constraint-planner
```

You can override the destination root:

```bash
CODEX_HOME=/tmp/codex-home ./scripts/install_skill.sh
```

## CLI Quick Start

The CLI is intentionally thin. It does rendering, validation, and run recording. The reasoning work still belongs to the model following the skill.

Initialize Stage A from a raw request:

```bash
python3 scripts/ecl.py pre \
  --request "Build a minimal app with a dashboard, an empty state, and one write flow." \
  --output /abs/path/to/bundle \
  --repo-path /abs/path/to/repo \
  --project-path /abs/path/to/repo
```

After the approval gate is complete, render the post-approval bundle:

```bash
python3 scripts/ecl.py plan \
  --input-json /abs/path/to/case.json \
  --output /abs/path/to/bundle \
  --force
```

Record a `/code` run:

```bash
python3 scripts/ecl.py code \
  --case /abs/path/to/bundle \
  --run-json /abs/path/to/run.json
```

Render the final achieve verdict:

```bash
python3 scripts/ecl.py achieve --case /abs/path/to/bundle
```

## Required Codex Behavior

This repository is explicitly Codex-first. The public skill assumes:

- the environment can load a `SKILL.md` directory as a Codex skill
- the model can read local files and run the helper scripts
- real spawned subagents are available for the mandatory independent stages

If your environment cannot launch real subagents, ECL can still be studied, but D, G, H, and J cannot be truthfully marked complete.

## Repository Map

- [docs/theory.md](docs/theory.md): what ECL is, where its theory comes from, and what problem it is designed to solve
- [docs/stages.md](docs/stages.md): every stage, owner, input, output, exit gate, and failure mode
- [docs/subagents.md](docs/subagents.md): exactly where real subagents are required and what they return
- [docs/implementation.md](docs/implementation.md): CLI flow, bundle compilation, templates, schema, and OpenSpec output
- [examples/README.md](examples/README.md): how to read the sample workspace
- [README.zh-CN.md](README.zh-CN.md): Chinese repository guide

## Example Workspace

The repository ships with a validator-passing Stage A sample:

- [examples/stage-a-sample/case.json](examples/stage-a-sample/case.json)
- [examples/stage-a-sample/bundle/00-overview.md](examples/stage-a-sample/bundle/00-overview.md)
- [examples/stage-a-sample/bundle/98-j-compile-for-code.md](examples/stage-a-sample/bundle/98-j-compile-for-code.md)
- [examples/stage-a-sample/bundle/99-code-handoff.md](examples/stage-a-sample/bundle/99-code-handoff.md)

Paths inside the sample are intentionally sanitized to placeholder absolute paths so the example can be published safely.

## Verification

Run the public smoke tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Validate the shipped sample bundle directly:

```bash
python3 scripts/validate_ecl_bundle.py examples/stage-a-sample/bundle
```

## License

[MIT](LICENSE)
