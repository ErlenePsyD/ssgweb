---
name: prepare-post
description: Prepare a draft blog post for publication by formatting content, generating frontmatter, and moving to the blog directory
arguments:
  - name: draft_file
    description: Path to the draft file (e.g., drafts/post-44.txt)
    required: true
---

You are preparing a blog post for publication on ErlenePsyD.com, a psychology blog by Dr. Erlene Rosowsky focused on gerontology and aging.

## Your Task

Read the draft file at `$ARGUMENTS.draft_file` and prepare it for publication by:

### 1. Generate Frontmatter

Create proper Pelican frontmatter with:
- **Title**: Extract from the draft content (usually near the beginning)
- **Date**: Use today's date in format `YYYY-MM-DD HH:MM` (use 08:00 as default time)
- **Tags**: Generate 3-5 relevant tags based on content (common tags: aging, psychology, gerontology, wisdom, mental health, relationships, family)
- **Summary**: Write a 1-2 sentence SEO-friendly description

### 2. Format Content for Web Readability

Apply full restructuring:
- **Fix grammar** while preserving the author's distinctive voice
- **Add clear headings** (use ## for main sections) to organize content logically
- **Create bullet lists** where appropriate for dense information
- **Add pull quotes** (use > blockquote syntax) to highlight key insights
- **Break long paragraphs** into shorter ones (2-4 sentences each)
- **Break run-on sentences** into shorter, clearer sentences
- **Remove unnecessary parentheses and ellipses**

### 3. Apply Standard Post Structure

Use this structure:
```markdown
---
Title: [extracted title]
Date: [today's date] 08:00
Tags: [generated tags]
Summary: [SEO summary]
---

_Thoughts and Suggestions from an Aging Psychologist._

[Formatted content with headings, short paragraphs, pull quotes...]

[Contact me]({filename}/pages/contact.md). I'd love to hear back from you, especially about any creative ways you've put this to use.

![Dr. R written by hand]({static}/images/dr_r_sm.png)
```

### 4. Content Preservation Rules

- **Never summarize** or condense the original content
- **Preserve all stories**, anecdotes, and descriptive details
- **Maintain direct quotes** exactly as written
- **Keep the author's personal voice** and perspective

### 5. Save the File

- Create a short, descriptive filename (1-3 words, kebab-case)
- Save to `erlenepsyd.com/content/blog/[filename].md`
- Delete or note the original draft file location

### 6. Final Output

After completing the edits:
1. Show the user the generated frontmatter for review
2. Confirm the new file location
3. Summarize the structural changes made (headings added, paragraphs split, etc.)
