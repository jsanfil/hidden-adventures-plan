---
name: create-github-bug
description: Use when a user gives a short natural-language bug report, optionally with a screenshot, and wants it turned into a minimal GitHub issue in the correct Hidden Adventures repo.
---

# Create GitHub Bug

Turn a short Codex prompt into a lightweight bug issue without forcing the user through a long template.

## When To Use

Use this skill for prompts like:

- "Let's fix the avatar placement on the ProfileView."
- "Server feed filter is ignoring radius."
- "This screen is clipped on iPhone SE. See screenshot."

Do not use this skill when the user wants the bug fixed immediately without creating a tracking issue.

## Repo Selection

Infer the owning repo before creating the issue.

- Choose `jsanfil/hidden-adventures-ios` for iOS, SwiftUI, Xcode, simulator, screen, layout, navigation, accessibility, or native app bugs.
- Choose `jsanfil/hidden-adventures-server` for API, schema, auth backend, endpoint, migration, fixture pack, or Vitest-related bugs.
- If the prompt clearly spans both repos, create:
  - one coordination issue in `jsanfil/hidden-adventures-plan`
  - one child bug in each owning repo
- If ownership is genuinely unclear, ask one short question instead of guessing.

## Default Labels

Apply these labels to every created bug:

- `type:bug`
- `status:ready`
- `prio:p2` unless the user signals higher urgency

Add one `area:*` label only when it is obvious from the prompt. Skip it when confidence is low.

For cross-repo work, also add:

- `needs:cross-repo`
- `needs:ios` and/or `needs:server` on the coordination issue as appropriate

## Minimal Issue Body

Create a concise title, then use this body shape:

```md
## Summary

<2-4 sentence summary in plain language>

## Acceptance Criteria

- [ ] <user-visible fix outcome>
- [ ] <layout / behavior / contract looks correct in the affected area>
- [ ] <relevant repo validation passes>

## Evidence

<optional screenshot note or link>

## Related Issues

<optional parent or child issue links>

## Notes / Unknowns

<optional ambiguity, repo handoff, or follow-up note>
```

Remove empty optional sections instead of leaving placeholders behind.

## Screenshot Handling

If a screenshot is provided:

- If it already has a durable URL, include it directly in `Evidence`.
- If it is only attached in the Codex thread or available as a local file, summarize the visual issue in words and note where the screenshot lives.
- Do not block issue creation on image upload support.

The written description should stand on its own even if the screenshot is not accessible in GitHub later.

## Title Style

Keep titles short and concrete.

- Good: `ProfileView avatar is misaligned to the right`
- Good: `Feed radius filter is ignored on server reads`
- Avoid: `Fix bug`
- Avoid: `UI issue from screenshot`

## Example

Input:

> Lets fix the avatar placement on the ProfileView. See how it is too far to the right. See screenshot. Make it line up better with the rest of the view.

Output shape:

- Repo: `jsanfil/hidden-adventures-ios`
- Title: `ProfileView avatar is misaligned to the right`
- Labels: `type:bug`, `status:ready`, `prio:p2`, `area:profile`

Issue body:

```md
## Summary

The avatar in `ProfileView` sits too far to the right relative to the rest of the profile content. Adjust the layout so the avatar lines up cleanly with the surrounding view structure.

## Acceptance Criteria

- [ ] Avatar aligns visually with the rest of the profile layout
- [ ] The affected profile screen looks correct after the adjustment
- [ ] Relevant iOS validation passes

## Evidence

- Screenshot referenced from the Codex thread for this bug report
```

## Creation Flow

1. Infer the repo.
2. Draft the title and minimal issue body.
3. Create the issue with `gh issue create` in the owning repo.
4. If labels already exist, apply the default labels during creation.
5. If the shared project `Hidden Adventures Bug Workflow` is available, add the issue to it and mirror the labels into project fields when practical:
   - `status:ready` -> `Status: Todo`
   - `prio:p0` -> `Priority: P0`
   - `prio:p1` -> `Priority: P1`
   - `prio:p2` -> `Priority: P2`
   Labels remain the source of truth if the project is not updated.
6. Return the repo, issue number, and title to the user.

If project mirroring is skipped, still create the minimal issue and mention that the issue labels are authoritative.
