# Content Development Workflow - Quick Reference

This document provides a step-by-step guide for the collaborative content development process.

## Quick Start Checklist

This repo's `main` branch is protected. To update the Firebase production server at https://erlenepsyd.com/, you must merge a PR onto `main`.

Pushing updates to a branch besides `main` will regenerate the site on the Firebase staging server, when a PR is open.

### Environment Setup (One-time)

- [ ] Poetry installed (`poetry --version`)
- [ ] GitHub CLI installed and authenticated (`gh auth status`)
- [ ] Repository cloned locally
- [ ] Dependencies installed (`poetry install`)

### Receive Drafts

When a new draft is created:

1. Check out the branch `feature/update-content`
2. Add the draft document to the `drafts` folder
3. Commit and push the updates.

### For Each New Post

#### 1. Create Issue and Branch


```bash
# Create issue on GitHub, then:
git fetch origin
git checkout <branch-name-from-issue>
```

Create the new branch from `feature/update-content` with a descriptive name, like:

- `feature/post-37`
- `feature/couples-podcast`

#### 2. Add Content

Create the new markdown file with the following prompt:

> You are a skilled and nuanced editor with a light touch, who focuses on formatting writing for online readability instead of changing the original text. Please fix the grammar in the following article. Add headings, bullet lists and pull quotes as appropriate. Break long, run-on sentences into shorter sentences. Do not summarize. Preserve the details of the stories, especially descriptive details and quotes. Break long paragraphs into shorter ones. Remove parenthesis and ellipsis. Format and save the file in Markdown with a short, 1 - 3 word filename, in the `drafts` directory, using the following format: `drafts/post-title.md`.

- Add markdown file to `erlenepsyd.com/content/blog/`
- Add images to `erlenepsyd.com/content/images/`
- Follow naming conventions: `post-title.md`, `descriptive-image-name.jpg`

#### 3. Test Locally

```bash
cd erlenepsyd.com
poetry shell
poetry run pelican content/
poetry run pelican --listen --autoreload
```

- Visit `http://127.0.0.1:8000/`
- Verify post appears on homepage
- Check images load correctly
- Test all links

#### 4. Create PR

```bash
git add .
git commit -m "Add new post: [Post Title]"
git push origin <branch-name>
gh pr create --title "Add new post: [Post Title]" --body "Ready for client review"
```

#### 5. Client Review Process

1. GitHub Actions creates staging URL automatically
2. Email staging URL to client
3. For changes:

   ```bash
   # Make edits, test locally, then:
   git add .
   git commit -m "Update based on client feedback"
   git push origin <branch-name>
   ```

4. Repeat until approved

#### 6. Publish

```bash
gh pr merge <pr-number> --merge --delete-branch
```

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

Your content here...

![Alt text]({static}/images/your-image.jpg){: .image-process-crisp}
```

### Image Guidelines

- Use descriptive filenames
- Optimize for web (reasonable file sizes)
- Include alt text for accessibility
- Use `{: .image-process-crisp}` for styling

## Automation Features

### GitHub Actions

- **PR Creation**: Automatically builds staging site
- **PR Updates**: Rebuilds staging on each push
- **Main Merge**: Automatically deploys to production
- **Comments**: Posts staging URLs in PR comments

### Local Development Features

- **Auto-reload**: Changes trigger automatic rebuilds
- **Live server**: Instant preview at localhost:8000
- **Dependency management**: Poetry handles all Python packages

## Emergency Procedures

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
