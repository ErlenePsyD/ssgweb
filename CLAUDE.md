# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is ErlenePsyD.com, a psychology blog and professional website built with Pelican (Python static site generator). The site focuses on gerontology and clinical psychology content by Dr. Erlene Rosowsky.

## Development Commands

```bash
# Setup environment (run from project root)
cd erlenepsyd.com && poetry install && poetry shell

# Local development
poetry run pelican content/                    # Generate site
poetry run pelican --listen --autoreload      # Live server (http://localhost:8000)

# Alternative using Makefile (from erlenepsyd.com/ directory)
make html                                      # Generate site
make devserver                                 # Live server with auto-reload
make clean                                     # Clean output directory
```

## Content Development

**Blog posts:** Create in `erlenepsyd.com/content/blog/` with this format:
```markdown
---
Title: Your Post Title
Date: YYYY-MM-DD HH:MM
Tags: tag1, tag2, tag3
Summary: SEO-friendly description for meta tags
---

Content here with responsive images:
![Alt text]({static}/images/filename.jpg){: .image-process-crisp}
```

**Images:** Place in `erlenepsyd.com/content/images/` and reference with `{static}/images/` syntax. The `{: .image-process-crisp}` class enables automatic responsive image generation.

**Static pages:** Located in `erlenepsyd.com/content/pages/` (about.md, contact.md, cv.md, gallery.md)

## Content Style Guide

Conventions for editing and formatting blog posts. Preserve the author's voice; these rules govern mechanics, not substance.

**Punctuation:**
- **Em-dashes (—):** Avoid em-dashes in body prose. Many readers are sensitive to them, and they can read as AI-generated. Replace with commas where the sentence still flows; otherwise restructure into shorter sentences. The post Summary (frontmatter) is the one place an em-dash pair is acceptable for a tight parenthetical aside.
- Remove unnecessary parentheses and ellipses when formatting drafts for the web.

**Voice & perspective:**
- Posts are written in the first person as an aging psychologist. In Summaries, use first person ("we," "our") or refer to "an aging psychologist." **Never** refer to "Dr. Rosowsky" in the third person.
- Summaries should focus on the post's themes and ideas, not its literary devices, and accurately represent the author's positions.

**Formatting for web readability:**
- Use `##` headings to organize content into logical sections.
- Keep paragraphs short (2–4 sentences); break up run-on sentences.
- Use bullet lists for dense or enumerable information.
- Use `>` blockquotes for pull quotes that highlight key insights.
- Fix grammar while preserving the author's distinctive voice; never summarize or condense original content.

## Architecture

**Pelican Configuration:**
- `pelicanconf.py` - Main configuration with plugins and theme settings
- `publishconf.py` - Production overrides (sets RELATIVE_URLS = False)

**Key Plugins:**
- `pelican-seo` - SEO metadata and structured data
- `pelican-image-process` - Responsive image generation with multiple formats
- `pelican-neighbors` - Post navigation
- `pelican-sitemap` - XML sitemap generation
- `typogrify` - Typography enhancement

**Custom Theme:** `themes/myidea/` contains Jinja2 templates and CSS for the professional psychology theme.

## Deployment

**Staging:** All PRs automatically deploy to Firebase staging with preview URLs posted in PR comments.

**Production:** Merging to `main` branch triggers automatic deployment to production Firebase hosting.

**Branch Strategy:** Create feature branches from GitHub issues, develop with staging previews, merge to main for production.

## Important Technical Details

**Dependencies:** Uses Poetry for local development but pip/requirements.txt for GitHub Actions (Python 3.9 in CI, 3.12 locally).

**Generated Content:** The `output/` directory is gitignored and contains the built static site.

**Firebase Config:** `firebase.json` defines hosting rules and redirects for both staging and production.

**Draft Content:** The `/drafts/` folder contains work-in-progress posts that can be moved to the blog folder when ready.

## Content Workflow

The repository includes comprehensive documentation in README.md and WORKFLOW.md that detail the full content development process, GitHub Actions automation, and emergency procedures for rollbacks.