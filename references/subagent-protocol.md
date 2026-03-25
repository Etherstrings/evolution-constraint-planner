# Subagent Protocol v2

## Contents

- General rules
- Shared delta shape
- A support-agent patterns
- D critique-agent
- G red and blue agents
- H review-agent
- J compile-agent
- Failure handling

## General Rules

- D, G, H, and J require real spawned agents.
- A may use support agents, but the parent model remains the owner of preprocessing.
- Pass only stage-local context:
  - raw request
  - current ledger snapshot
  - relevant source artifacts
  - local repo/docs/config facts needed for that stage
- Do not pass the parent's preferred answer to independent agents.
- Parent is the only writer to bundle notes.
- Subagents return structured deltas only. They do not return finished notes.

## Shared Delta Shape

All subagents should return:

```json
{
  "facts": [],
  "challenges": [],
  "conflicts": [],
  "gaps": [],
  "discard_recommendations": [],
  "follow_up_questions": [],
  "confidence": "medium",
  "evidence_refs": []
}
```

## A Support-Agent Patterns

These are optional helpers. Use them only when they materially improve preprocessing.

### Intent Extractor

```text
Read the user's raw request plus the current ledger snapshot. Infer what the user probably wants beyond the literal wording. Assume the user may not understand their own desired outcome yet. Return suspected_real_goals, hidden_assumptions, scenario_fragments, examples or counterexamples worth eliciting, and broad clarification questions that increase semantic coverage.
```

### Reality Gap Checker

```text
Read the user's raw request plus any local facts. Challenge claims that may be false, incomplete, contradictory, non-technical, solution-biased, or based on missing objective facts. Return facts, challenges, gaps, contradictions to verify, and clarification questions that would force the user to expose hidden semantics.
```

### Blind Spot Scout

```text
Read the user's raw request plus the current ledger snapshot. Identify important dimensions the user likely has not named yet: workflow edges, non-goals, success signals, constraints, tradeoffs, acceptance meaning, environmental dependencies, and failure handling. Return blind spots, coverage gaps, and clarification questions that push the user to specify what they have not realized they need to say.
```

## D Critique-Agent

```text
You are an independent critic. Review the retained requirement package. Identify pseudo-requirements, contradictory requirements, unverifiable requirements, scope waste, hidden assumptions, and incorrect decompositions. Recommend what should be discarded, split, or rewritten. Return structured deltas only.
```

## G Red and Blue Agents

### Red Prompt

```text
Attack the retained path. Focus on edge cases, abuse, missing assumptions, dependency breakage, impossible state transitions, ambiguous recovery behavior, invalid input, and unhandled environmental failure. Return attack vectors and gap findings only.
```

### Blue Prompt

```text
Defend the retained path. For each likely attack or failure mode, either provide a mitigation, acceptance rule, monitoring requirement, or explicitly state the residual risk if the issue cannot be solved in this version. Return structured deltas only.
```

## H Review-Agent

```text
Review the full A-H package for coding readiness. Reject it if the next coding model would still need to invent core meaning, product semantics, validation meaning, or dependency behavior. Return one verdict: approved, approved_with_conditions, or rejected. Return blockers, conditions, rationale, and the earliest stage that should be reopened if rejected.
```

## J Compile-Agent

```text
Read the converged A-H package plus the current handoff. Compile the retained result into frozen companion docs and a final code-readiness summary. Confirm whether the package is code_ready, which contract docs must be referenced, what the direct next /code command should be, and which blockers keep the case open if it is not yet ready.
```

## Failure Handling

- If a required agent cannot be created:
  - write the stage note anyway
  - set `status` to `blocked_by_agent_unavailable`
  - set `agent_mode` to `blocked`
  - stop the flow before later dependent stages complete
