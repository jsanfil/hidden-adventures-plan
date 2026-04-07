# Tasks and Templates

This directory holds durable templates for task creation, repo backlog rules, and parallel execution tracking.

Recommended workflow:

1. create or update an issue in your issue tracker
2. copy the task template into the issue body or linked Markdown note
3. update `master-plan.md` or the relevant workstream when status changes

Execution notes:

- Run parallel Codex work across repos, and allow multiple active threads or git worktrees inside the same repo when scopes are explicit and non-conflicting.
- Use each owning repo's `main` branch unless there is a repo-specific reason to do otherwise.
- Keep `hidden-adventures-plan` as the only repo that declares milestone status and cross-repo truth.
- Treat `tasks/parallel-tracks.md` as the source of truth for repo-autonomous next-work rules.

The active repo-lane matrix lives in `tasks/parallel-tracks.md`.
Use `tasks/thread-template.md` when you want to record a scoped thread or worktree.
Historical lane playbooks from the prior execution model now live under `archive/tasks-threads/` and are not authoritative for current decisions.
