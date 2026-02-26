# ssgweb

Static site source for [ErlenePsyD.com](https://erlenepsyd.com/), a psychology blog by Dr. Erlene Rosowsky. Built with Pelican (Python).

## Content Development Workflow

Most of the content workflow is automated via Claude Code skills:

1. **`/prepare-post`** — Formats a draft for publication (frontmatter, headings, grammar, structure)
2. **`/git-sync --pr`** — Commits to a feature branch, opens a PR, triggers staging deployment
3. **Featured image** — `/prepare-post` walks through image optimization with `xplat` and `imgpro`
4. **Client review** — Review the staging preview, iterate, then merge to deploy to production

For the complete step-by-step process, see **[WORKFLOW.md](WORKFLOW.md)**.

---

## Technical Setup

### Prerequisites

You need Poetry installed to manage the Python environment. Read about your platform here: [Introduction | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/#installation).

If Poetry is installed correctly, this will work:

```bash
poetry --version
```

You'll need to set up your Python environment like this, **in the project root**, which contains the `pyproject.toml` file:

```bash
poetry install
```

## GitHub CLI Setup

For managing GitHub Actions and pull requests from the command line, install the [GitHub CLI](https://cli.github.com/):

```bash
brew install gh        # macOS
```

After installation, authenticate with GitHub:

```bash
gh auth login
```

## Dependency Management

This project uses a hybrid approach for dependency management:

- **Local development**: Use Poetry for managing dependencies and virtual environments
- **CI/CD (GitHub Actions)**: Use pip with `requirements.txt` for faster, more reliable builds

### Adding Dependencies

To add a new dependency:

```bash
poetry add package-name
```

After adding dependencies, regenerate the requirements.txt file for GitHub Actions:

```bash
poetry export --without-hashes --format=requirements.txt --output=requirements.txt
```

## GitHub Actions Automation

The repository includes automated GitHub Actions that:

- **Pull Requests**: Automatically build and deploy preview sites to Firebase
- **Main branch**: Automatically deploy to production Firebase hosting

### Viewing GitHub Actions

To view recent GitHub Actions runs:

```bash
gh run list
```

To view logs from a specific run:

```bash
gh run view <run-id> --log
```

### Preview URLs

When you create a pull request, GitHub Actions will automatically create a preview deployment. The preview URL will be available in the GitHub Actions logs and posted as a comment on the pull request.

## Pelican Configuration and Branch Strategy

The problem: developing and testing Pelican works best with relative URLS -- in other words, links that are stored as paths from the site root ("/") without the protocol and domain (like <https://www.example.com>). This is for two reasons:

- You can test your work on Pelican's local web server at 127.0.0.1 if you use relative URLs
- You can also publish your site to a staging server with any arbitrary domain (<https://staging.example.com> for example) and it will still work just as it did on your local web server.

Unfortunately, many of Pelican's plugins require absolute URLs, like the pelican-seo plugin.

For example, Pelican allows you to force the use of relative URLS, by adding this line in pelicanconf.py on the `staging` branch:

```python
RELATIVE_URLS = True
```

Alternatively, you can set this value to False, like this, on the `production` branch:

```python
RELATIVE_URLS = False
```

This will generate SEO friendly absolute links and feeds, but only on the `production` branch.

## GitHub, branches, and .gitignore to the rescue

One of the benefits of using Pelican for web development is that you can commit your work to a version control system like GitHub. In addition to being able to roll back to any saved version of your files, using GitHub means:

- you can share your work with other developers;
- you have a reliable offsite backup every time you push your work to GitHub;
- you can always regenerate the site from a "known-good" version of the site.

But, not every file in your project needs to be committed to GitHub.

### Generating the site

When you run `pelican content` this generates site content in `ssgweb/erelenpsyd.com/output` -- these are the files that need to go on either the staging or production server.

Because you can re-create the ouput files any time, as long as you have the files in the `content` and `themes` folder, all output files are excluded, via `.gitignore`, from the GitHub repo. This means that the output files you generate only exist on your local development workstation.

## Additional Tools

The content workflow uses these CLI tools (installed via pipx):

- **`xplat`** — Cross-platform file renaming (`xplat rename --style web`)
- **`imgpro`** — Image conversion and resizing (`imgpro convert`, `imgpro resize`)
