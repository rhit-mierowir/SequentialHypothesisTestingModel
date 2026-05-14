# Setting Up Code

This repository assumes that you will clone it to your local computer, or whereever you plan to run the code.

## Installing Dependancies
This repository manages dependancies using [Poetry](https://python-poetry.org/). To install dependancies and run the code, (once you installed Poetry) do the following:

``` bash
poetry install
```

This will start the process of installing all of the dependancies in this project.

``` bash
poetry run <command>
```

When you run the above command, replacing `<command>` with the command you want to run, it will be run in the virtual environment the Poetry creates with all of your dependancies installed. 

## Viewing Website
The website that this repository creates is creaked by [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and can be edited and viewed easily locally. 

Viewing the website locally is performed by running a command locally, but it works best if you install Material for MkDocs on your local python instance. This can be done by running the following commands:

``` bash
pip install mkdocs-material 
pip install mkdocs-redirects mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin mkdocs-awesome-nav mkdocs-macros-plugin
```

These commands can also be found near the end of the file for `.github/workflows/deploy_website.yml`, which is used to create the publically viewable website.

To display the website locally, run 

``` bash
mkdocs serve
```

This will then identify a port on your local computer to connect to (e.x. `http://127.0.0.1:8000/`), at which you will be able to see your website. Whenever you update and save files locally that influence this website, it will automatically update.

The files used to create the website are in the `docs` directory.

Whenever you push your code to the github repository, github actions will automatically run, create the website, and then deploy it on Github Pages so it can be publically viewable.