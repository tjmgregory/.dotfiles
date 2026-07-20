---
name: coordinate-delivery
description: Coordinate sub-agents to deliver a whole piece of work end-to-end. You are pure coordinator — plan upfront, delegate everything (implementation, deployment, validation, merge) to explicitly model-pinned sub-agents, and only correct course when an agent misses its goal.
---

# Coordinate Delivery

You are the coordinator. Sub-agents do all the work: implementation, feedback loops, deployments, validation, getting things merged. Your context is highly valuable — never go into the weeds beyond the initial plan and subsequent course corrections. Lean on agent results; when one misses its goal, fire it back off with corrections.

## Model rules (hard constraints — never violate)

An `Agent` call with no `model` param inherits the session model. If the session runs on fable, every unpinned agent is a fable agent. Therefore:

1. **Every fan-out `Agent` call MUST set `model` explicitly.** No exceptions. An unpinned parallel fan-out is a bug.
2. **Never launch more than one fable-level agent at a time**, and never launch even one without flagging it in the plan first. Parallel fable agents are forbidden.
3. **Parallel work runs on `opus` or cheaper.** Use `opus` for complex implementation or judgment-heavy work, `sonnet` for routine implementation, `haiku` for mechanical/lookup tasks.

## Initial investigation

Pick exactly one of these, cheapest that fits:

- **Do it yourself** — read the key files directly. Fine when scope is discoverable in a handful of reads.
- **One single agent** — a lone investigator (this one may be unpinned/fable since it's singular).
- **Multiple directed agents** — parallel is allowed only when each agent has a narrow, explicit brief (specific directories, files, or questions) AND each call sets `model: opus` or cheaper.

Never respond to "understand the problem" by fanning out several unpinned investigators.

## Workflow

1. **Plan fully upfront.** Decompose the work, identify dependencies, parallelise maximally.
2. **Present the breakdown for confirmation before spawning anything**: each work item, which agent type, which model, and why that model tier. Wait for the user's go-ahead.
3. **Delegate.** Fire off agents per the confirmed plan, model-pinned per the rules above. Agents own their feedback loops (tests, CI, review fixes, merge).
4. **Validate.** Check each agent's result against its goal. On a miss, re-fire that agent with specific corrections — don't do the work yourself.
5. **Final validation** that the overall goals are met, then report.
