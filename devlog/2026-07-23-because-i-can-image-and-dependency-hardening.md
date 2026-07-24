# Because I Can Image + Dependency Hardening — 2026-07-23

## Session Summary

Added the client's featured image to the already-published "Because I Can" post, then enabled Dependabot and worked through the 30 alerts it surfaced. Investigation revealed that the repo's `requirements.txt` (which CI installs from) was decoupled from Poetry — Dependabot only updated `poetry.lock`, so security patches never reached production. Fixed the immediate Pillow + soupsieve advisories, then refactored dependency management so Poetry is the single source of truth, eliminating the drift class entirely. Repo went from **30 open Dependabot alerts to 0**, all deployed to production.

## Work Completed

### Featured Image
- Client photo `drafts/IMG_3401.jpeg` (5712×4284, 9 MB, desert lawn at golden hour)
  - `xplat` (per prepare-post skill) is not installed; used `imgpro` directly and renamed manually
  - Resized to 720×540 at quality 80 with `imgpro resize --width 720 --quality 80`
  - Stripped EXIF (removes iPhone GPS) with `imgpro convert --format jpg --quality 80 --strip-exif`
  - Named `desert-lawn-sunset-shadows.jpg`, placed in `content/images/` with `.image-process-crisp`
- Added after the tagline in `because-i-can.md` with descriptive alt text
- Committed to existing branch `post/because-i-can` (PR #111); deleted the 9 MB raw source from `drafts/`
- Client approved staging preview; merged PR #111 to production

### Dependabot Enablement
- No `.github/dependabot.yml` existed; added config for `pip` and `github-actions` ecosystems (PR #112)
- Note: the GitHub token in use (`stratofax`) has push/triage but **not admin**, so the "Dependabot security updates" repo setting could not be toggled via API — left as a hand-off note for an admin

### Security Investigation & Immediate Fix
- 30 open alerts = 15 unique advisories double-counted across `requirements.txt` and `poetry.lock`
  - Pillow < 12.3.0 (10 high + 3 medium), soupsieve <= 2.8.3 (2 high)
- **Root-cause finding:** CI runs `pip install -r requirements.txt`, but Dependabot's version PRs only updated `poetry.lock`. Confirmed in a Dependabot PR build log that CI still installed `pillow-12.2.0`. `requirements.txt` was a hand-maintained `poetry export` that drifted.
- Patched the production manifest directly: `requirements.txt` → pillow 12.3.0, soupsieve 2.8.4 (PR #123). Cleared all 15 `requirements.txt` alerts.

### Dependabot PR Triage
- Dependabot opened 10 PRs. Closed the 8 pip PRs (#115–#122) — each only touched `poetry.lock` (dev-only) and would have created dev/prod drift; superseded by #123 and the refactor below.
- Merged the 2 GitHub Actions bumps: checkout 6→7 (#113). setup-python 6→7 (#114) still open pending a rebase (see Open Items).

### Refactor: Poetry as Single Source of Truth (PR #124)
- CI now installs via `poetry install --only main` against `pyproject.toml` + `poetry.lock`, with pip-cached Poetry, in both Firebase workflows
- Deleted `requirements.txt`; `poetry.lock` is the only pinned manifest
- Relocked security packages with a targeted `poetry update pillow soupsieve`: pillow 12.2.0 → 12.3.0, soupsieve 2.6 → 2.9.1 (no collateral upgrades)
- Updated README and CLAUDE.md to document the Poetry-only flow
- Verified: local build clean (54 articles, 4 pages); PR staging preview green; production deploy green on the new pipeline
- **Result: Dependabot alerts 30 → 0**

## Commits Made

| Hash | Message |
|---|---|
| fab3987 | feat: add featured image to "Because I Can" post |
| 33499cd | Merge pull request #111 (because-i-can) |
| 13dbf92 | chore: add Dependabot config for pip and github-actions |
| 162e2ba | Merge pull request #112 (enable-dependabot) |
| 41f878b | fix: bump pillow and soupsieve to patch security advisories |
| 89aaf3a | Merge pull request #123 (security-bump-pillow-soupsieve) |
| 62ce14f | chore(deps): Bump actions/checkout from 6 to 7 |
| e815f5d | Merge pull request #113 (checkout v7) |
| 13803ed | refactor: make Poetry the single source of truth for dependencies |
| 1def334 | Merge pull request #124 (poetry-source-of-truth) |

## Key Files

**Created/Modified:**
- `erlenepsyd.com/content/blog/because-i-can.md` — added featured image
- `erlenepsyd.com/content/images/desert-lawn-sunset-shadows.jpg` — featured image (720×540)
- `.github/dependabot.yml` — new Dependabot config (pip + github-actions)
- `.github/workflows/firebase-hosting-merge.yml` / `firebase-hosting-pull-request.yml` — Poetry-based install/build
- `poetry.lock` — pillow 12.3.0, soupsieve 2.9.1
- `README.md`, `CLAUDE.md` — documented Poetry-only dependency flow

**Deleted:**
- `requirements.txt` — removed; Poetry is now the single source of truth
- `drafts/IMG_3401.jpeg` — raw client source (client retains original)

## Open Items

- **PR #114** (actions/setup-python 6→7) — conflicted with #124's setup-python block; triggered `@dependabot rebase`. Merge once it repushes. CI hygiene only, not security.
- **Admin hand-off:** enable "Dependabot security updates" (Settings → Code security) with an admin account for targeted security-only auto-PRs going forward. Not required now — the Poetry refactor means routine version PRs already reach production.

## Notes

- **Local Poetry is broken** in this env: the pyenv Python 3.12.3 throws `unsupported hash type blake2b/blake2s` (compiled without proper OpenSSL). Worked around it with `pipx run poetry` (uses Homebrew Python 3.14) to run `poetry update` and `poetry lock` successfully. Worth fixing the pyenv build for future sessions.
- `poetry lock` in Poetry 2.x only refreshes; it does **not** upgrade already-locked deps that still satisfy constraints. Use `poetry update <pkg>` for targeted bumps.
- Image tooling this session: `imgpro` is installed; `xplat` (referenced by the prepare-post skill) is not. A prior devlog noted renames to `ipro`/`iname`, but neither those nor `xplat` resolved here — only `imgpro`. The skill's image steps may need updating to match what's actually installed.
- The `requirements.txt` ↔ Poetry decoupling was the underlying cause of repeated manual security-sync work seen in earlier devlogs; it is now structurally resolved.
