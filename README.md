# ssgweb

Erlene's website generation files. This site uses Pelican, which is a Python project.

## Content Development Workflow

For complete step-by-step instructions on creating new blog posts, managing client reviews, and publishing updates, see **[WORKFLOW.md](WORKFLOW.md)**.

The workflow document covers:

- Environment setup and prerequisites
- Creating issues and branches
- Adding and testing content locally
- Creating pull requests
- Client review process
- Publishing to production
- Automation features and potential enhancements

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

For managing GitHub Actions and pull requests from the command line, install the GitHub CLI:

```bash
sudo apt update && sudo apt install gh
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

## Legacy: Working with staging and production branches

**Note:** The current workflow uses the `main` branch with GitHub Actions for automated deployments. The information below is maintained for historical reference.

In the legacy workflow, all changes to the site's `content` folder, including Markdown (.md) and image files (like .jpg, .gif, and .png files) were committed first to the `staging` branch, after testing locally.

Changes that were committed to `staging` included:

- Updates to `pyproject.toml` and `poetry.lock` -- all pelican plugins were installed on `staging` so the virtual environments were the same for all branches
- Updates to the site theme, such as changes to `article.html` -- especially if these changes included code to support pelican plugins (for example, `pelican-neighbors` requires changes to `article.html`)
- Updates to the documentation, including this README.md file
- Updates to `pelicanconf.py` that weren't specifically related to production server configuration

## Best Practices

### Careful commits

You should always try to group related files when you commit. For example, if you add a new Markdown (.md) post and add some new image files to that post, include all of these files in the same commit, since they're all related to adding the new post.

Likewise, changes to documentation, like edits to this README.md file, should not be committed with changes to site content, as the two changes are unrelated.

Finally, **always commit `pelicanconf.py` by itself** to make it easier to resolve any merge issues with the production branch.
