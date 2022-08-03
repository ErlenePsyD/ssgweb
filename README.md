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

Generated content is in `ssgweb/erelenpsyd.com/output` and these are the files that need to go on either the staging or production server. Note that output files are excluded, via `.gitignore`, from the GitHub repo. The output files you generate only exist on your local development workstation.

## Pushing files to Firebase

Once you've updated the site so it's ready for client review, push the edits to the Firebase staging server.

### Using the staging server

Enter these commands in the following order

```bash
firebase --version      # ensure firebase is working
firebase login          # ensure you're authenticated 
firebase use staging    # Use the stagin server
firebase deploy         # deploy files to staging
```
