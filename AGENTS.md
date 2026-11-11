# Agent instructions

## Scope and checkout

- Follow the user's task and inspect the actual path, remotes, branch, worktrees and working-tree changes before editing. Read applicable nested instructions.
- Use explicit working directories, preserve unrelated edits and isolate concurrent writers in separate branches/worktrees. Start Plugins tasks from verified `main` on a `codex/` branch unless instructed otherwise.
- Locate related checkouts by their remotes rather than assuming sibling paths. Inspect their own instructions before changing them.
- Keep documentation, UI text, comments and diagnostics in English. Retain existing Chinese/English document pairs; translate Chinese-only documents rather than deleting their content.

## Engineering principles

- Keep backend, Engine and frontend build outputs out of the client package. Route solver changes to Engine and service/UI/authentication changes to Platform; consult [README.md](README.md) and [HARNESS_DEVELOPMENT.md](HARNESS_DEVELOPMENT.md) for the interfaces.
- Never publish credentials, private experiments or internal deployment configuration. Use host-managed OAuth; do not hardcode secrets, tokens, client identities or callback ports to bypass discovery or authorization.
- Preserve each client's manifest and installation contracts. Share assets only where the actual client formats are compatible.
- Avoid duplicate instruction/design sources and new execution frameworks without a demonstrated current consumer and benefit.

## Version authorization

- Do not advance this project to version `1.0` without an explicit user request. Do not infer that authorization from compatibility rules, release preparation or deployment readiness.

## Verification and delivery

- For package or manifest changes, run `python -m pytest tests` and `node --test tests/test_plugin_listing.mjs`. The loader check requires a working Codex CLI; report unavailable checks.
- For documentation-only changes, check accuracy, paths and the diff. Do not add placeholder prose tests.
- Verify changed MCP or authentication interfaces against the target service where authorized. Report package checks, online MCP calls and native-panel acceptance separately.
- Do not run Invar Guard or adopt its check-in workflow, contract rules or generic file/function size gates, including in worktrees.
- Commit repositories separately and record paired interface/version dependencies. Verify Engine, Platform, then Plugins when a dependency changes; retain immutable release pins.
- Do not deploy, push, publish or remove other tasks' resources without the corresponding authorization. Preserve reviewable results and report remaining verification gaps.
- Execute directly unless the user or active planning/orchestration role requests Vectl. Existing assigned steps retain their owner; use Vectl tools for managed plan changes and never edit `plan.yaml` directly.
