# Content Development Workflow

This document provides a complete step-by-step guide for the collaborative content development process, designed for collaboration between developers and content creators.

## Overview

This repo's `main` branch is protected. To update the Firebase production server at [https://erlenepsyd.com/](https://erlenepsyd.com/), you must merge a PR onto `main`.

Pushing updates to a branch besides `main` will regenerate the site on the Firebase staging server when a PR is open.

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
```

**Checklist:**

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

- `post/37-couples-podcast`

#### 2. Add Content

Use the agent-blog-post-editor to execute this prompt:

> You are a skilled and nuanced editor with a light touch, who focuses on formatting writing for online readability instead of changing the original text. Please fix the grammar in the following article. Add headings, bullet lists and pull quotes as appropriate. Break long, run-on sentences into shorter sentences. Do not summarize. Preserve the details of the stories, especially descriptive details and quotes. Break long paragraphs into shorter ones. Remove parenthesis and ellipsis. Format and save the file in Markdown with a short, 1 - 3 word filename, in the `drafts` directory, using the following format: `drafts/post-title.md`.

- Add markdown file to `erlenepsyd.com/content/blog/`
- Add images to `erlenepsyd.com/content/images/`
- Follow naming conventions: `post-title.md`, `descriptive-image-name.jpg`

#### 3. Generate Site Locally and Test

```bash
# Navigate to the website directory
cd erlenepsyd.com

# Activate Poetry shell
poetry shell

# Generate the site
poetry run pelican content/

# Start local development server
poetry run pelican --listen --autoreload
```

The site will be available at `http://127.0.0.1:8000/`. Test that:

- New post appears on the front page
- Images load correctly
- All links work properly
- Content displays as expected

Press `CTRL-C` to stop the server.

#### 4. Push Changes to Remote

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "Add new post: [Post Title]"

# Push to remote branch
git push origin <branch-name>
```

Pushing changes automatically triggers GitHub Actions to create a Firebase staging deployment with a preview URL.

#### 5. Create Pull Request

```bash
# Create PR using GitHub CLI
gh pr create --title "Add new post: [Post Title]" --body "Adds new blog post and supporting images. Ready for client review."

# Or create PR via GitHub web interface
```

The GitHub Actions will post a comment with the staging URL for review.

#### 6. Client Review Cycle

1. Email the staging URL to the client for review
2. Client provides feedback via email
3. Make requested changes locally
4. Test changes with local development server
5. Push updates to the same branch
6. Repeat until client approves

**Making Updates During Review:**

```bash
# Make changes to content files
# Test locally as described in step 3
# Commit and push updates
git add .
git commit -m "Update post based on client feedback"
git push origin <branch-name>
```

Each push automatically updates the staging deployment.

#### 7. Publish to Live Site

Once client approves all changes:

```bash
# Merge the PR (requires approval)
gh pr merge <pr-number> --merge --delete-branch

# Or merge via GitHub web interface
```

Merging to `main` automatically deploys to the production site via GitHub Actions.

#### 8. Sync Development Branch

After publishing to `main`, synchronize `feature/update-content` with the latest changes:

```bash
# Create PR to merge main into feature/update-content
gh pr create --base feature/update-content --head main \
  --title "Sync feature/update-content with latest main changes" \
  --body "Brings feature/update-content up to date with main branch"

# After approving and merging the sync PR:
git checkout feature/update-content
git pull origin feature/update-content

# Clean up any stale remote tracking references
git remote prune origin
```

This ensures `feature/update-content` stays current with the protected `main` branch for future development work.

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

### Current GitHub Actions

- **PR Creation**: Automatically builds staging site
- **PR Updates**: Rebuilds staging on each push
- **Main Merge**: Automatically deploys to production
- **Comments**: Posts staging URLs in PR comments
- Automatic staging deployments on PR creation
- Automatic production deployments on merge to main
- Preview URL generation and commenting

### Local Development Features

- **Auto-reload**: Changes trigger automatic rebuilds
- **Live server**: Instant preview at localhost:8000
- **Dependency management**: Poetry handles all Python packages

### Potential Enhancements

Consider adding these automation improvements:

**Automated Testing with Playwright:**

```bash
# Add Playwright to dependencies
poetry add playwright pytest-playwright

# Install browser dependencies
poetry run playwright install
```

Create test files to verify:

- New posts appear on homepage
- Images load correctly
- Navigation links work
- SEO metadata is present

**Future GitHub Actions Enhancements:**

- Automated accessibility testing
- Link checking
- Image optimization
- Performance testing

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
