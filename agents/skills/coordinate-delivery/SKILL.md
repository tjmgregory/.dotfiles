---
name: coordinate-delivery
description: Coordinates end-to-end delivery of a whole piece of work through model-pinned sub-agents — plans upfront, delegates everything (implementation, deployment, validation, merge), and corrects course only when an agent misses its goal. Use when the user invokes /coordinate-delivery or asks to coordinate, orchestrate, or delegate an entire delivery to sub-agents.
---

# Coordinate Delivery

Act as pure coordinator. Sub-agents do all the work: implementation, feedback loops, deployments, validation, getting things merged. Coordinator context is highly valuable — never go into the weeds beyond the initial plan and subsequent course corrections. Lean on agent results; when one misses its goal, fire it back off with corrections.

## Model rules (hard constraints — never violate)

An `Agent` call with no `model` param inherits the session model. If the session runs on fable, every unpinned agent is a fable agent. Therefore:

1. **Every fan-out `Agent` call MUST set `model` explicitly.** No exceptions. An unpinned parallel fan-out is a bug.
2. **Never launch more than one fable-level agent at a time**, and never launch even one without flagging it in the plan first. Parallel fable agents are forbidden.
3. **Parallel work runs on `opus` or cheaper.** Use `opus` for complex implementation or judgment-heavy work, `sonnet` for routine implementation, `haiku` for mechanical/lookup tasks.
4. **A fable sub-agent MUST run `/coordinate-delivery` itself** and push all implementation to its own pinned sub-team. This is mandatory, not conditional on the work looking big enough. A fable agent that writes the code itself is a bug.
5. **Reserve fable for the meaty and critical work**, including serial critical-path pieces. Rule 2 (one fable at a time) constrains *concurrency*, not which work deserves fable. When a critical piece runs alone, it gets fable.

## API and load errors are never a reason to change the plan

`500`, `529 Overloaded`, and "server error mid-response" are transient infrastructure faults. They say nothing about whether the plan or the agent was right.

- **Resume the same agent** (`SendMessage` to its id) so it keeps its context and its worktree. Do not relaunch it fresh, do not hand its job to a different agent, and do not absorb its role yourself.
- **Never restructure the delegation** because an agent died. If a lead keeps dying, resume the lead; do not promote yourself into its position or spawn its children on its behalf.
- **Waiting is the correct response.** Let the load pass and carry on as planned.
- Tell the resumed agent plainly that it died to a server-side error, not to a mistake of its own, and where it had got to.

Course corrections are for agents that **miss their goal**, not for agents the infrastructure interrupted.

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

## Verify agent reports against real state

An agent's self-report is a claim, not evidence. Before accepting "done", check the artefact: the PR is merged, the commit is **pushed** (agents commit locally and forget to push), CI is green **against the current head SHA** (a duplicate workflow run pending is not a failure), the file on `origin/main` actually says what the agent said it says.

Two recurring agent failure modes to watch for:

- **Parking on a phantom signal.** An agent stops mid-task saying it is "waiting on the background watcher / CI / a monitor" when nothing will ever notify it. Resume it and tell it to poll to a terminal state itself and act.
- **Unit-green, wiring-absent.** Components pass their own tests while nothing on the live path calls them. Requirement coverage and green CI both look fine. Make every builder prove the wiring with a test that **fails if the wiring is removed**, and make reviewers ask "is this actually invoked on the live request path", not "does the code exist".
