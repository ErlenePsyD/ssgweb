# Content Development Workflow

This document provides a complete step-by-step guide for the content development process.

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

## Add New Post

Here are the steps to add a new post to the site.

### Clean up the local repo

- Use the custom command alias `git cleanup` to remove stale branches
- Ensure the `main` branch is up to date: `git switch main && git pull`

### Receive Drafts

When a new draft is created:

1. Add the draft document to the `drafts` folder
2. Create a new branch with a descriptive name that includes the `posts/` prefix  and the post number. For example, `git checkout -b posts/42-contagion`
3. Commit and push the updates

### Create the new post

When it's time to prepare the post for the staging server, Move the draft file from the `drafts` folder to the `posts` folder:

```bash
cd ~/Repos/erlenepsyd/ssgweb/
mv drafts/post-title.md erlenepsyd.com/content/blog/
```

### Format Post

Use the agent-blog-post-editor:

> Use @agent-blog-post-editor to prepare @erlenepsyd.com/content/blog/contagion.md for publication

Or execute this prompt, to prepare the new post:

> You are a skilled and nuanced editor with a light touch, who focuses on formatting writing for online readability instead of changing the original text. Please fix the grammar in the following article. Add headings, bullet lists and pull quotes as appropriate. Break long, run-on sentences into shorter sentences. Do not summarize. Preserve the details of the stories, especially descriptive details and quotes. Break long paragraphs into shorter ones. Remove parenthesis and ellipsis. Format and save the file in Markdown with a short, 1 - 3 word filename, in the `drafts` directory, using the following format: `drafts/post-title.md`.

### Post creation file conventions

- Add markdown file to `erlenepsyd.com/content/blog/`
- Add images to `erlenepsyd.com/content/images/`
- Follow naming conventions: `post-title.md`, `descriptive-image-name.jpg`

### Push Changes to Remote

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "Add new post: [Post Title]"

# Push to remote branch
git push origin <branch-name>
```

### Create Pull Request

When the post is ready for review and testing, create a pull request to deploy the updates to the staging server.

Create PR using GitHub CLI:

```bash
gh pr create --title "Add new post: [Post Title]" --body "Adds new blog post and supporting images. Ready for client review."
```

Additional pushes will automatically trigger a GitHub Action to create a Firebase staging deployment with a preview URL.

The GitHub Actions will post a comment with the staging URL for review.

### (Optional) Generate Site Locally and Test

Pushing changes to an open PR will generate a new staging deployment. If there are problems with the staging deployment, you can generate a new one locally and test it.

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

### Client Review Cycle

After reviewing the staging site, follow these steps to reach signoff:

1. Email the staging URL to the client for review
2. Client provides feedback via email
3. Make requested changes locally
4. Test changes with local development server
5. Push updates to the same branch
6. Repeat until client approves

Each push automatically updates the staging deployment.

### Publish to Live Site

Once client approves all changes, merge the PR:

```bash
gh pr merge <pr-number> --merge --delete-branch
```

Or merge via GitHub web interface.

Merging to `main` automatically deploys to the production site via GitHub Actions.

### Create LinkedIn summaries

Using an AI tool, like Windsurf or Perplexity, that allows you to select multiple AI models, summarize the new post with the following prompt:

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

- Use descriptive filenames
- Optimize for web (reasonable file sizes)
- Include alt text for accessibility
- Use `{: .image-process-crisp}` for styling

Content column width: 760px maximum

This is defined in main.css:427:

```css
#content {
    background: #fff;
    margin-bottom: 2em;
    overflow: hidden;
    padding: 20px 20px;
    max-width: 760px;
    /* ... */
}
```

However, since there's 20px padding on each side (left and right), the actual usable content area is 720px (760px - 40px).

Key measurements:

- `#content max-width: 760px`
- Padding: 20px on each side (40px total)
- **Actual content area: 720px**
- Body container: 800px max-width (main.css:243)

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
