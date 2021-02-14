## WARNING: This project is in alpha - use at your own risk!


# pcra - Python Create React App

### CLI for template based project scaffolding based on the [React to Python](https://jennasys.com/rtp.html) book

This highly opinionated script will create the initial structure for a React/Material-UI application that is programmed in Python and uses 
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


### Install using Python 3.7 with:
```bash
python3.7 -m pip install git+https://github.com/JennaSys/pcra --user
```
On Windows you can also use:
```bash
py -3.7 -m pip install git+https://github.com/JennaSys/pcra --user
```

## Usage:
`py-create-react-app [-h] [-co] [-nv] [-njs] [-ng] [-t TEMPLATE] FOLDER_NAME`

Python Create React App: Template based Python React project scaffolding creator

positional arguments:
```bash
  FOLDER_NAME           name of the project folder (must not already exist)
```


optional arguments:  
```bash
  -h,          --help               show this help message and exit
  -co,         --client-only        only create client project (not full stack)
  -nv,         --no-virtualenv      DO NOT create virtual environments
  -njs,        --no-javascript      DO NOT install JavaScript libraries
  -ng,         --no-git             DO NOT create Git repository
  -t TEMPLATE, --template TEMPLATE  alternate template folder to use

```
NOTE: Transcrypt requires that this must be run with Python version 3.7
