# ssgweb

Erlene's website generation files. This site uses Pelican, which is a Python project.

You need Poetry installed to manage the Python environment. Read about your platform here: [Introduction | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/#installation).

If Poetry is installed correctly, this will work:

```bash
poetry --version
```

You'll need to set up your Python environment like this, **in the project root**, which contains the `pyproject.toml` file:

```bash
poetry install
```

## Using Pelican

To run the Pelican commands, change to the website directory:

```bash
cd erlenepsyd.com
# set up the Python virtual environment
poetry shell
```

If poetry reports any version issues, update it:

```bash
exit   # to leave the poetry shell environment
poetry update
poetry shell
```

Now you can generate the site, and serve it up:

```bash
pelican content
pelican --autoreload --listen
```

## Using GitHub branches to prepare a Pelican site for a staging and production server

The problem: developing and testing Pelican works best with relative URLS -- in other words, links that are stored as paths from the site root ("/") without the protocol and domain (like "https://www.example.com"). This is for two reasons:

* You can test your work on Pelican's local web server at 127.0.0.1 if you use relative URLs
* You can also publish your site to a staging server with any arbitrary domain ("https://staging.example.com" for example) and it will still work just as it did on your local web server.

Unfortunately, many of Pelican's plugins require absolute URLs, like the pelican-seo plugin.

## GitHub, branches, and .gitignore to the rescue

One of the benefits of using Pelican for web development is that you can commit your work to a version control system like GitHub. In addition to being able to roll back to any saved version of your files, using GitHub means:

* you can share your work with other developers;
* you have a reliable offsite backup every time you push your work to GitHub;
* you can always regenerate the site from a "known-good" version of the site.

### Generating the site

When you run `pelican content` this generates site content in `ssgweb/erelenpsyd.com/output` -- these are the files that need to go on either the staging or production server. Note that all output files are excluded, via `.gitignore`, from the GitHub repo. The output files you generate only exist on your local development workstation.

## Working with the staging and production branches

All changes to the site's `content` folder, inclduing Markdown (.md) and image files (like .jpg, .gif, and .png files) should be committed first to the `staging` branch, after you've tested them locally.

In addition to site content, other changes should also be committed to `staging` (except for production-specific changes to `pelicanconf.py`).

These changes include:

* Updates to `pyproject.toml` and `poetry.lock`  -- all pelican plugins should be installed on `staging` so the virtual environments are the same for all branches.
* Updates to the site theme, such as changes to `article.html` -- especially if these changes include code to support pelican plugins (for example, `pelican-neighbors` requires changes to `article.html`).
* Updates to the documentation, including this README.md file.
* Updates to `pelicanconf.py` that aren't specifically related to production server configuration. This can lead to some complex merges, so be careful!

## Updating the staging branch

Before you commit your changes to the `staging` branch,

1. check out the `staging` branch on your development workstation.
2. Make your changes locally.
3. Generate the site locally: `pelican content`
4. Test the site locally: `pelican --autoreload --listen`

## Deploy to the Firebase staging server

Once you've updated the site so it's ready for client review, push the edits to the Firebase staging server.

### Deploy to the staging server: firebase commands

Enter these commands in the following order

```bash
firebase --version      # ensure firebase is working
firebase login          # ensure you're authenticated 
firebase use staging    # Use the stagin server
firebase deploy         # deploy files to staging
```

## Testing the production branch

1. Switch to the production branch.
2. To test, uncomment: `RELATIVE_URLS = True`
3. Make production-specific changes to `pelicanconf.py`
4. Generate site: `pelican content/`
5. Test locally on `http://127.0.0.1:8000/` with `pelican --autoreload --listen`

## Deploy to the production server
