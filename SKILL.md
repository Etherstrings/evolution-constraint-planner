---
name: evolution-constraint-planner
description: Run ECL v2 as a strict plan/code/achieve workflow for product and engineering requests that must move from raw ideas to code without semantic drift. Use when Codex needs to take an idea, aggressively audit and clarify it, freeze implementation meaning, produce a code-ready handoff, execute only from that handoff, and verify the shipped result. Especially useful for web products or internal tools where plan must interrogate hidden user intent before freezing meaning, code must not reopen product meaning, and final delivery must survive tests plus first-open product checks.
---

# Evolution Constraint Planner v2

Use this skill when the user wants ECL to behave like a real delivery system, not a loose planning ritual. The non-negotiable rule is simple:

- `plan` is responsible for understanding and freezing meaning
- `code` is responsible only for faithful execution
- `achieve` is responsible for proving the result is actually acceptable and turning that judgment into the archived closure record

If `code` still needs to ask what the product means, `plan` failed.

## Command Surface

Use these command names in the conversation and in helper scripts:

- `ecl pre`
- `ecl plan`
- `ecl code`
- `ecl achieve`

Bundled CLI helpers are available for structured artifacts:

- `scripts/ecl.py scaffold --request "..." --output-json /abs/path/case.json`
- `scripts/ecl.py plan --input-json /abs/path/to/case.json --output /abs/path/to/bundle --force`
- `scripts/ecl.py code --handoff /abs/path/to/90-code-handoff.md --run-json /abs/path/to/run.json`
- `scripts/ecl.py achieve --case /abs/path/to/bundle`

Use the CLI as a rendering, validation, and run-recording helper. The reasoning work still belongs to the model following this skill.

## Workflow Contract

### 1. `pre`

`pre` owns Stage A and the approval gate.

Use `ecl pre` to initialize the Stage A workspace from the raw request, then do the high-interaction clarification work there before any later planning stages begin.

- Treat the raw request as unreliable input.
- Search the local repo, docs, configs, tests, and existing product artifacts before asking the user anything.
- Treat the user's self-report as incomplete, unstable, and frequently under-specified; assume they may not know what they actually want until questioned from multiple angles.
- Do not optimize for fewer questions in A. Optimize for semantic coverage before approval.
- Ask broad, concrete clarification questions that pressure-test goals, non-goals, examples, counterexamples, priorities, edge cases, failure handling, state behavior, data meaning, and UX expectations.
- Prefer question batches that expose hidden contradictions or missing semantics over a single minimal follow-up.
- Present a compact approval pack before moving on:
  - reframed goal
  - retained scope
  - discarded scope
  - critical assumptions
  - the specific decisions that will be frozen for `code`
- Do not enter `ecl plan` until the user explicitly approves the reframed direction and Stage A is complete.

### 2. `plan`

`plan` starts only after `pre` is complete and approved.

- After approval, preserve A as frozen input and run B-H plus J to convergence.
- After approval, most user interaction should stop; B-H and J should converge mainly in the background unless a new high-impact ambiguity appears.
- D, G, and H must use real subagents.
- Treat `30-c-requirements.md` as the place to freeze requirement units and their future coding cut lines, so task decomposition is traced from requirements instead of invented later.
- Treat `50-e-closure.md` as the place to resolve hidden prerequisites and turn requirement dependencies into a dependency-aware execution chain.
- Treat `05-constraint-ledger.md` as the shared truth source.
- Treat `90-code-handoff.md` as the only truthful implementation entrypoint.
- Compile the retained result into companion docs `91-canonical-contracts.md`, `92-constraint-crosswalk.md`, `95-execution-manifest.md`, `96-code-batches.md`, `97-code-preflight.md`, `98-j-compile-for-code.md`, and `99-code-handoff.md`.
- Treat `95-execution-manifest.md` and `96-code-batches.md` as the task-planning surface: dependency-aware phases, grouped batches, verification order, and done signals that can be exported cleanly into `tasks.md`.
- Treat `97-code-preflight.md` as the shared execution workboard used with the user before `/code`: it should summarize the active context bundle, progress snapshot, current focus, remaining work, and pause conditions without changing frozen product meaning.
- Keep `code_ready=false` unless the next coding model can implement without inventing product meaning, validation meaning, state semantics, or dependency behavior.

Read these references while planning:

- [plan-approval-gate.md](references/plan-approval-gate.md)
- [stage-playbook.md](references/stage-playbook.md)
- [subagent-protocol.md](references/subagent-protocol.md)
- [handoff-quality-bar.md](references/handoff-quality-bar.md)
- [ecl-schema.md](references/ecl-schema.md)

### 3. `code`

`code` consumes only `90-code-handoff.md` plus the files it explicitly references.

The companion docs are support surfaces for the handoff:

- `91-canonical-contracts.md`
- `92-constraint-crosswalk.md`
- `95-execution-manifest.md`
- `96-code-batches.md`
- `97-code-preflight.md`
- `98-j-compile-for-code.md`
- `99-code-handoff.md`

`/code` still treats `90-code-handoff.md` as the sole truthful execution entrypoint.

`97-code-preflight.md` is the collaborative execution surface, not an alternate truth source. It may track progress, current unit, remaining work, mirrored task checkboxes, and pause reasons, but it must not rewrite frozen semantics.

`code` must:

- ground itself in repo reality first
- execute the implementation units in order
- verify after each implementation unit
- fail closed on semantic ambiguity
- write a run record every time

`code` must not:

- reopen product direction
- invent missing user semantics
- silently reorder the handoff
- decide acceptance criteria on its own

If a high-impact ambiguity appears during `code`, treat it as a planning defect. Stop, write reentry evidence, and point back to the earliest broken stage.

Read [code-playbook.md](references/code-playbook.md) before running `code`.

### 4. `achieve`

Use `achieve` after coding when the user wants closure rather than a partial implementation report.

`achieve` must verify all of the following:

- the bundle still validates
- required tests/build checks pass
- the product satisfies the handoff acceptance checks
- the first-open experience does not have obvious broken states
- any UI work survives a quick browser pass, not just typecheck

`achieve` must also:

- record whether the run is archived as closed evidence or left open
- keep failed acceptance runs open instead of pretending they closed cleanly

If the implementation fails obvious first-impression quality, `achieve` must not claim success.

Read [achieve-playbook.md](references/achieve-playbook.md) before closing the loop.

## Handoff Truth Rules

When `ecl.code_handoff.code_ready=true`, the handoff must freeze all high-impact meaning needed by the coder.

At minimum the handoff must make explicit:

- what the product is and is not
- the repo targets and repo facts the plan depends on
- the user-visible workflows and empty/error/loading states
- the domain objects and state transitions
- the data shape and persistence behavior
- the file-by-file change plan
- the function-level contracts
- the exact implementation units and their order
- the verification commands and browser checks
- the conditions that would force reentry

Read [handoff-quality-bar.md](references/handoff-quality-bar.md) before declaring `code_ready=true`.

## Extended Companion Bundle

In the extended bundle layout, planning should also emit:

- `91-canonical-contracts.md`: concise frozen contracts
- `92-constraint-crosswalk.md`: contracts mapped to code and verification
- `95-execution-manifest.md`: dependency-aware execution phases or scaffold blueprint
- `96-code-batches.md`: grouped code batches that can become `tasks.md`
- `97-code-preflight.md`: shared execution workboard and coding-time "do not reinterpret" rules
- `98-j-compile-for-code.md`: J-stage compile summary and code-readiness reasoning
- `99-code-handoff.md`: user-facing final handoff summary and next command

These notes do not replace `90-code-handoff.md`; they make the code-ready package easier to inspect without reopening product meaning.

## Web App Quality Bar

This version of the skill is optimized first for web products and internal tools, especially React, Next.js, and Vite projects.

For web app work:

- freeze routes, panels, and entry flows before `code`
- freeze component responsibilities and state ownership before `code`
- spell out loading, empty, stale, retry, and write-failure behavior
- include at least one browser-level validation path in the handoff
- do not claim success if opening the app reveals obvious layout or interaction breakage

Use the user's likely experience as the final bar, not just green terminal output.

## OpenSpec Mapping

When the user wants OpenSpec-style artifacts, map the converged ECL package into:

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/...`

Treat the OpenSpec pack as a compiled view of frozen ECL truth:

- `proposal.md`: what changed and why
- `design.md`: how the retained path works and which dependencies make it viable
- `tasks.md`: dependency-aware implementation steps, grouped batches, verification checkpoints, and done signals

Do this after A-H and J have converged so the OpenSpec pack reflects frozen meaning rather than draft thinking. Use [openspec-mapping.md](references/openspec-mapping.md) for the mapping rules.

## Working Pattern

1. Start from the raw request.
2. Run `ecl pre` to initialize the Stage A approval workspace.
3. Do the high-interaction approval-gate work and freeze the approval pack with the user.
4. Build or update normalized case data until Stage A is complete.
5. Run `ecl plan --input-json ...` after approval to converge B-H and J.
6. Render with `scripts/render_obsidian_bundle.py`.
7. Validate with `scripts/validate_ecl_bundle.py`.
8. Compile the extended companion bundle, including J and 91/92/95/96/97/98/99 when that mode is in use.
9. Execute `/code` only from `90-code-handoff.md`.
10. Record the run with `scripts/render_code_run.py`.
11. Close with `scripts/ecl.py achieve` or the equivalent manual `achieve` workflow so the bundle contains the final acceptance-and-archive record.

## Resource Index

- [plan-approval-gate.md](references/plan-approval-gate.md): how to ask follow-up questions and freeze approval
- [stage-playbook.md](references/stage-playbook.md): A-H execution rules
- [subagent-protocol.md](references/subagent-protocol.md): mandatory agent stages and deltas
- [handoff-quality-bar.md](references/handoff-quality-bar.md): what must be frozen before `code`
- [code-playbook.md](references/code-playbook.md): strict coding behavior
- [achieve-playbook.md](references/achieve-playbook.md): closure, acceptance, and archive verification
- [openspec-mapping.md](references/openspec-mapping.md): optional OpenSpec export rules
- [ecl-schema.md](references/ecl-schema.md): bundle and structured block schema
