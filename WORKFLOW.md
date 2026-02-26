# Content Development Workflow

This document provides a complete step-by-step guide for the content development process.

## Overview

This repo's `main` branch is protected. To update the Firebase production server at [https://erlenepsyd.com/](https://erlenepsyd.com/), you must merge a PR onto `main`.

Pushing updates to a branch besides `main` will regenerate the site on the Firebase staging server when a PR is open.

Most of the workflow is automated via Claude Code skills (`/prepare-post` and `/git-sync --pr`). The manual steps are: receiving the draft, reviewing the formatted post, client review of staging, and merging the PR.

### Environment Setup (One-time)

Before starting, ensure your local environment is properly configured:

#### Prerequisites Check

```bash
# Verify Poetry is installed
poetry --version

# Verify Python dependencies are installed
poetry install

# Verify GitHub CLI is set up (for PR management)
gh auth status

# Verify content tools are available
xplat --version
imgpro --version
```

**Checklist:**

- [ ] Poetry installed (`poetry --version`)
- [ ] GitHub CLI installed and authenticated (`gh auth status`)
- [ ] Repository cloned locally
- [ ] Dependencies installed (`poetry install`)
- [ ] `xplat` installed via pipx (`xplat --version`)
- [ ] `imgpro` installed via pipx (`imgpro --version`)
- [ ] Claude Code installed with `/prepare-post` and `/git-sync` skills

## Add New Post

Here are the steps to add a new post to the site.

### 1. Clean up the local repo

- Use the custom command alias `git cleanup` to remove stale branches
- Ensure the `main` branch is up to date: `git switch main && git pull`

### 2. Receive the draft

Add the draft document to the `drafts/` folder.

### 3. Prepare the post with `/prepare-post`

Run the Claude Code skill:

```
/prepare-post drafts/post-title.md
```

This automatically:

- Extracts the title, generates tags and SEO summary
- Formats content for web readability (headings, short paragraphs, pull quotes)
- Fixes grammar while preserving the author's voice
- Saves to `erlenepsyd.com/content/blog/` with a descriptive filename
- Shows you the result for review

### 4. Deploy to staging with `/git-sync --pr`

After reviewing and approving the formatted post, run:

```
/git-sync --pr
```

This automatically:

- Creates a feature branch (e.g., `post/magical-thinking`)
- Commits the post, draft, and any other changes
- Opens a pull request, which triggers a staging deployment

### 5. Add a featured image

After the PR is open, `/prepare-post` walks you through the image workflow:

1. **Rename** with `xplat rename --style web` for a web-compatible filename
2. **Convert** iPhone photos (MPO) to plain JPEG with `imgpro convert`
3. **Resize** to 720px wide (content column width) with `imgpro resize --width 720 --quality 80`
4. **Add to the post** with descriptive alt text and `.image-process-crisp` class

Commit and push to the same branch — staging rebuilds automatically.

### File conventions

- Blog posts: `erlenepsyd.com/content/blog/post-title.md`
- Images: `erlenepsyd.com/content/images/descriptive-name.jpg`
- Drafts: `drafts/post-title.md`

### (Optional) Test locally

If there are problems with the staging deployment, you can test locally:

```bash
cd erlenepsyd.com && poetry run pelican --listen --autoreload
```

The site will be available at `http://127.0.0.1:8000/`. Press `CTRL-C` to stop.

### 6. Client review cycle

1. Send the staging URL to the client for review
2. Client provides feedback
3. Make requested changes and push to the same branch
4. Staging rebuilds automatically — repeat until approved

### 7. Publish to production

Once the client approves, merge the PR:

```bash
gh pr merge <pr-number> --merge --delete-branch
```

Or merge via the GitHub web interface. Merging to `main` automatically deploys to production via GitHub Actions.

### 8. Create LinkedIn summary

Summarize the new post for social media:

> Please summarize the article, as if you were the original author, using a helpful and professional tone. Keep the summary to 120 words or less.

## Common Commands

### Local Development

```bash
# Start development server
cd erlenepsyd.com && poetry run pelican --listen --autoreload

# Generate site only
cd erlenepsyd.com && poetry run pelican content/

# Check Poetry environment
poetry env info
```

### GitHub Operations

```bash
# List open PRs
gh pr list

# View PR details
gh pr view <pr-number>

# Check PR status and staging URL
gh pr view <pr-number> --json comments

# Merge PR
gh pr merge <pr-number> --merge --delete-branch
```

### Troubleshooting

```bash
# Reset Poetry environment
poetry env remove python
poetry install

# Check GitHub CLI auth
gh auth status
gh auth refresh

# View recent GitHub Actions
gh run list
gh run view <run-id> --log
```

## File Structure

```text
erlenepsyd.com/
├── content/
│   ├── blog/           # Markdown blog posts
│   ├── images/         # Supporting images
│   └── pages/          # Static pages
├── themes/
│   └── myidea/         # Custom theme
├── pelicanconf.py      # Pelican configuration
└── Makefile           # Build commands
```

## Content Guidelines

### Blog Post Format

```markdown
---
Title: Your Post Title
Date: YYYY-MM-DD HH:MM
Tags: tag1, tag2, tag3
Summary: Brief description for SEO and previews
---

_Thoughts and Suggestions from an Aging Psychologist._

![Alt text]({static}/images/your-image.jpg){: .image-process-crisp}

Post content here...

[Contact me]({filename}/pages/contact.md). I’d love to hear back from you, especially about any creative ways you’ve put this to use.

![Dr. R written by hand]({static}/images/dr_r_sm.png)

_Photo by the author's family._
```

### Image Guidelines

- Use descriptive filenames (e.g., `picking-lemons-sunny-backyard.jpg`)
- Resize to 720px wide (the actual content area width) with `imgpro resize --width 720 --quality 80`
- Convert iPhone photos (MPO format) to plain JPEG first with `imgpro convert --format jpg --strip-exif`
- Use `xplat rename --style web` to ensure web-compatible filenames
- Include descriptive alt text for accessibility
- Use `{: .image-process-crisp}` class for responsive image generation

#### Content area dimensions

- `#content max-width: 760px` (defined in main.css:427)
- Padding: 20px on each side (40px total)
- **Actual content area: 720px** — target width for images
- Body container: 800px max-width (main.css:243)

## Automation Features

### Claude Code Skills

- **`/prepare-post`** — End-to-end post preparation: formatting, frontmatter, image optimization, staging deployment
- **`/git-sync --pr`** — Branch creation, commit, PR, and staging trigger
- **`/git-sync`** — Follow-up commits pushed to the existing branch

### GitHub Actions

- **PR Creation/Updates**: Automatically builds and deploys staging site
- **Main Merge**: Automatically deploys to production
- **Comments**: Posts staging URLs in PR comments

### Local Development

- **Auto-reload**: `poetry run pelican --listen --autoreload` for instant preview
- **Dependency management**: Poetry handles all Python packages

## Emergency Procedures

### Prune Stale Local Branches

Use these steps to remove local branches that no longer exist on the remote.

```bash
# Confirm current branch and upstream status
git status -sb

# Prune stale remote-tracking refs (removes origin/* entries that were deleted on GitHub)
git fetch --prune

# List local branches and show which ones have an upstream that is gone
git branch -vv

# Delete local branches whose upstream is shown as ": gone"
# (example from this repo cleanup)
git branch -D feature/84-post-39-you-earned-it-podcast feature/update-content post/40-npr-interview post/41-fountain-pen

# Verify the result
git branch -vv
```

### Rollback Production

```bash
# Find last good commit
git log --oneline -10

# Create hotfix branch
git checkout -b hotfix-rollback
git reset --hard <good-commit-hash>
git push origin hotfix-rollback

# Create emergency PR
gh pr create --title "Emergency rollback" --body "Rolling back to last known good state"
```

### Fix Broken Staging

```bash
# Check GitHub Actions status
gh run list --limit 5

# View logs for failed run
gh run view <run-id> --log

# Common fixes:
# 1. Check markdown syntax
# 2. Verify image paths
# 3. Ensure all files are committed
```
