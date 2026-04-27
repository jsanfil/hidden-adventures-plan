# Tasks and Templates

Historical snapshot only. This directory preserves older task and thread templates that are no longer part of the active planning surface.

Recommended workflow:

1. create or update an issue in your issue tracker
2. copy the task template into the issue body or linked Markdown note
3. update `master-plan.md` or the relevant workstream when status changes

Execution notes:

- Run parallel Codex work across repos, and allow multiple active threads or git worktrees inside the same repo when scopes are explicit and non-conflicting.
- Use each owning repo's `main` branch unless there is a repo-specific reason to do otherwise.
- Keep `hidden-adventures-plan` as the only repo that declares milestone status and cross-repo truth.

Track the current scheduled feature and repo sequencing in `master-plan.md`.
Historical lane playbooks from the prior execution model now live under `archive/tasks-threads/` and are not authoritative for current decisions.
