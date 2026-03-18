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
- **Summary**: Write a 1-2 sentence SEO-friendly description following these guidelines:
  - Use first-person perspective ("we," "our") or refer to "an aging psychologist" — **never** refer to "Dr. Rosowsky" in third person
  - Focus on the **themes and ideas** of the post, not the literary devices used (e.g., don't say "uses a metaphor to explore…")
  - Match the tone of existing summaries — direct, warm, and grounded
  - Accurately represent the post's message; don't attribute positions the author doesn't take

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

### 7. Next Step: Deploy to Staging

After the user has reviewed and approved the post, suggest running:

```
/git-sync --pr
```

This commits the new post on a feature branch, opens a pull request, and triggers an automatic deployment to the staging server where the post can be previewed before going to production.

### 8. Featured Image

After the PR is created and staging is deploying, ask the user if they have a featured image for the post. If they provide one:

1. **Rename** with `xplat rename` to get a web-compatible filename:
   ```bash
   xplat rename --style web --output-dir erlenepsyd.com/content/images <source-image>
   ```
   Then propose a more descriptive name based on the image content (kebab-case, e.g., `picking-lemons-sunny-backyard.jpg`).

2. **Convert** iPhone photos (MPO format) to plain JPEG with `imgpro`:
   ```bash
   imgpro convert <image-path> --format jpg --quality 80 --strip-exif --output erlenepsyd.com/content/images/
   ```

3. **Resize** to 720px wide at 80% quality:
   ```bash
   imgpro resize <image-path> --width 720 --quality 80 --output erlenepsyd.com/content/images/
   ```
   Replace the original with the resized version (imgpro adds a `_720` suffix).

4. **Add to the post** after the tagline, using the site's responsive image class:
   ```markdown
   ![Descriptive alt text]({static}/images/filename.jpg){: .image-process-crisp}
   ```

5. **Commit and push** to the existing feature branch, then verify the staging preview includes the image.
