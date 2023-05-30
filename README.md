# _This project is no longer Active_
This project was an attempt to mimic what CRA (Create React App) does but for Python/Transcrypt and React. In practice, it became a bit too opinionated and not as useful as it first appeared it might be.  It is no longer being updated and should not be considered active.

---

# pcra - Python Create React App

### CLI for template-based project scaffolding based on the [React to Python](https://pyreact.com) book

This highly opinionated but configurable script will create the initial structure for a React/Material-UI application that is _programmed in Python_ (not JavaScript!) and uses 
[Transcrypt](https://www.transcrypt.org) to transpile the code into JavaScript.

The script performs the following actions:

- Creates a source code folder structure in the specified project folder
- Adds a set of core Python source code modules for creating the React application
- Optionally stubs out a Flask back-end application with basic user session management
- Creates virtual environments for front-end and back-end applications
- PIP installs Transcrypt and Flask into the virtual environments
- NPM installs Parcel and the Transcrypt plug-in for Parcel
- Adds a middleware script for serving the Flask application in development
- NPM installs react, material-ui, and other supporting JavaScript libraries
- Creates a local git repository and does an initial commit
- Initializes npm semver versioning for the front-end application

By default, the sample React application that is installed with `py-create-react-app` is just a placeholder for you to start building your application from.  It is similar to the one you get when using the JavaScript `create-react-app` command.
If you would like to use the framework outlined in the _React to Python_ book, you can use the `--full-stack` command-line option, which will create the scaffolding for a full-stack application with a Flask back-end.
If you only need the client side of that framework, you can use the `--client-only` option.

There are also options to bypass the setup for the virtual environment, installing JavaScript dependencies, and creating a Git repository, if you prefer to set any of those up manually.

If you have your own framework template that follows the same folder structure as PCRA, you can specify that on the command line as well and take advantage of the automated setup features. 

After installing the `pcra` package with pip, you can verify that it works by running it with:

`py-create-react-app my_project`

This will set up the structure of a project in a new **my_project** folder in the current directory.
After it finishes the setup process, you can build and run the application using the following commands:

`cd my_project`  
`source ./venv/bin/activate`  or `venv\Scripts\activate` for Windows  
`npm start -- --open`  


Default React Project  |  React to Python Project
:---------------------:|:------------------------:
![screenshot](https://github.com/JennaSys/pcra/raw/main/pcra_screenshot.png "Python Create React App Screenshot")  |  ![screenshot](https://github.com/JennaSys/pcra/raw/main/rtp_screenshot.png "React to Python Screenshot")

## Installation
### Install using Python 3.7 with:
```bash
python3.7 -m pip install pcra
```
or to get the latest version from GitHub:
```bash
python3.7 -m pip install git+https://github.com/JennaSys/pcra
```
On Windows you can also use:
```bash
py -3.7 -m pip install pcra
```


## Usage:
`py-create-react-app [-h] [-co | -fs] [-nv] [-njs] [-ng] [-t TEMPLATE] FOLDER_NAME`

Python Create React App: Template-based Python React project scaffolding creator

positional arguments:
```bash
  FOLDER_NAME           name of the project folder (must not already exist)
```


optional arguments:  
```bash
  -h,          --help               show this help message and exit
  -co,         --client-only        only create client project (not full stack)
  -fs,         --full-stack         create full-stack project (with Flask back-end)
  -nv,         --no-virtualenv      DO NOT create virtual environments
  -njs,        --no-javascript      DO NOT install JavaScript libraries
  -ng,         --no-git             DO NOT create Git repository
  -t TEMPLATE, --template TEMPLATE  alternate template folder to use

```
NOTE: Transcrypt requires that this must be run with Python version 3.7
