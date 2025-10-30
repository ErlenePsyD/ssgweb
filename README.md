# ssgweb

Erlene's website generation files. This site uses Pelican, which is a Python project.

## Content Development Workflow

This section documents the complete workflow for creating new blog posts and updating the website, designed for collaboration between developers and content creators.

### 1. Create PR and Update Site

#### Create Issue and Branch

1. Go to the repository: [ErlenePsyD/ssgweb](https://github.com/ErlenePsyD/ssgweb)
2. **Create an Issue** for the new post with a descriptive title
3. Create a new branch from the Issue using GitHub's "Create a branch" feature
4. Use a branch name in the form of `post/40-descriptive-name`
5. Clone or fetch the new branch locally:

```bash
git fetch origin
git checkout <branch-name>
```

#### Add Content Files

1. Add new blog post to `erlenepsyd.com/content/blog/`
2. Add supporting images to `erlenepsyd.com/content/images/`
3. Make any other required site updates

### 2. Generate Site Locally and Test

Before generating the site, ensure your local environment is properly configured:

#### Prerequisites Check

```bash
# Verify Poetry is installed
poetry --version

# Verify Python dependencies are installed
poetry install

# Verify GitHub CLI is set up (for PR management)
gh auth status
```

#### Generate and Test Locally

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

### 3. Push Changes to Remote

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "Add new post: [Post Title]"

# Push to remote branch
git push origin <branch-name>
```

Pushing changes automatically triggers GitHub Actions to create a Firebase staging deployment with a preview URL.

### 4. Create Pull Request

```bash
# Create PR using GitHub CLI
gh pr create --title "Add new post: [Post Title]" --body "Adds new blog post and supporting images. Ready for client review."

# Or create PR via GitHub web interface
```

The GitHub Actions will post a comment with the staging URL for review.

### 5. Client Review Cycle

1. Email the staging URL to the client for review
2. Client provides feedback via email
3. Make requested changes locally
4. Test changes with local development server
5. Push updates to the same branch
6. Repeat until client approves

#### Making Updates During Review

```bash
# Make changes to content files
# Test locally as described in step 2
# Commit and push updates
git add .
git commit -m "Update post based on client feedback"
git push origin <branch-name>
```

Each push automatically updates the staging deployment.

### 6. Publish to Live Site

Once client approves all changes:

```bash
# Merge the PR (requires approval)
gh pr merge <pr-number> --merge --delete-branch

# Or merge via GitHub web interface
```

Merging to `main` automatically deploys to the production site via GitHub Actions.

## Automation Opportunities

### Automated Testing Setup

Consider adding Playwright for automated testing:

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

### GitHub Actions Enhancements

Current automation includes:

- Automatic staging deployments on PR creation
- Automatic production deployments on merge to main
- Preview URL generation and commenting

Future enhancements could include:

- Automated accessibility testing
- Link checking
- Image optimization
- Performance testing

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

## Using Pelican

To run the Pelican commands, change to the website directory, generate the site, and serve it up::

```bash
cd erlenepsyd.com
poetry run pelican content/
poetry run pelican --listen --autoreload
```

To stop the web server, press `CTRL-C` in the terminal.

## Using GitHub branches to prepare a Pelican site for a staging and production server

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

## Working with the staging and production branches

All changes to the site's `content` folder, inclduing Markdown (.md) and image files (like .jpg, .gif, and .png files) should be committed first to the `staging` branch, after you've tested them locally.

In addition to site content, other changes should also be committed to `staging` (except for production-specific changes to `pelicanconf.py`).

These changes include:

- Updates to `pyproject.toml` and `poetry.lock`  -- all pelican plugins should be installed on `staging` so the virtual environments are the same for all branches.
- Updates to the site theme, such as changes to `article.html` -- especially if these changes include code to support pelican plugins (for example, `pelican-neighbors` requires changes to `article.html`).
- Updates to the documentation, including this README.md file.
- Updates to `pelicanconf.py` that aren't specifically related to production server configuration. This can lead to some complex merges, so be careful!

## Updating the staging branch

Before you commit your changes to the `staging` branch,

1. Checkout the `staging` branch on your development workstation.
2. Make your changes locally.
3. Generate the site locally: `pelican content`
4. Test the site locally: `pelican --autoreload --listen`

## Deploy to the Firebase staging server

Once you've updated the site so it's ready for client review, push the edits to the Firebase staging server. You can do this before or after you commit your changes to GitHub -- just be sure that `staging` is the currently checked out branch on your computer!

### Deploy to the staging server: firebase commands

Enter these commands in the following order:

```bash
firebase --version      # ensure firebase is working
firebase login --reauth # ensure you're authenticated
firebase use staging    # Use the staging server
firebase deploy         # deploy files to staging
```

**Note**: if you have any problem with the `use` command, your authorization token may have expired. Simply log out and log in again, like this:

```bash
firebase logout
firebase login
```

### Deploy to the production server

Once you're satisfied that the branch is ready to deploy to the production server, follow these steps:

1. Set: `RELATIVE_URLS = False` in `pelicanconf.py`
2. Generate site: `pelican content/`
3. Deploy the generated output to the production server using firebase.

```bash
firebase login --reauth
firebase use production     # Use the production server
firebase deploy             # deploy files to production
```

Now review the site in your favorite browser on the production web server: <https://erlenepsyd.com/>

### Careful commits

You should always try to group related files when you commit. For example, if you add a new Markdown (.md) post and add some new image files to that post, include all of these files in the same commit, since they're all related to adding the new post.

Likewise, changes to documentation, like edits to this README.md file, should not be committed with changes to site content, as the two changes are unrelated.

Finally, **always commit `pelicanconf.py` by itself** to make it easier to resolve any merge issues with the production branch.

## Testing the production branch

Once you've received signoff from the client for the material on the staging server, you can merge the changes from `staging` to `production` with a GitHub Pull Request (PR).

In most cases, this pull request should **not** include changes to `pelicanconf.py`

After you've merged the PR from `staging` to `production` you can use Pelican to test the changes and then finally deploy the updated files to the production server.

To test the production branch locally:

1. Switch to the production branch.
2. To test, set: `RELATIVE_URLS = True` in `pelicanconf.py`
3. Make any other production-specific changes to `pelicanconf.py`
4. Generate site: `pelican content/`
5. Test locally on `http://127.0.0.1:8000/` with `pelican --autoreload --listen`
