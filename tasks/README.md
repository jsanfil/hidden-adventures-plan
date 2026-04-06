# Tasks and Templates

This directory holds durable templates for task creation and repo-based execution tracking.

Recommended workflow:

1. create or update an issue in your issue tracker
2. copy the task template into the issue body or linked Markdown note
3. update `master-plan.md` or the relevant workstream when status changes

Execution notes:

- Run parallel Codex work across repos, not as multiple active implementation threads in the same repo.
- Use each owning repo's `main` branch unless there is a repo-specific reason to do otherwise.
- Keep `hidden-adventures-plan` as the only repo that declares milestone status and cross-repo truth.

The active repo-lane matrix lives in `tasks/parallel-tracks.md`.
Historical lane playbooks from the prior execution model now live under `archive/tasks-threads/`.
