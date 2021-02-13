# Python Create React App

### Client-Only Structure:

```
    project/
        ├── .gitignore
        ├── .git/
        ├── node_modules/
        ├── src/
        │    ├── common/
        │    │    ├── __init__.py
        │    │    ├── jsutils.py
        │    │    ├── pymui.py
        │    │    ├── pyreact.py
        │    │    └── urlutils.py
        │    ├── main/
        │    │    ├── __init__.py
        │    │    ├── aboutModal.py
        │    │    ├── appData.py
        │    │    ├── appTheme.py
        │    │    └── loginModal.py
        │    ├── static/
        │    │    ├── app_logo.jpg
        │    │    └── favicon.ico
        │    ├── views/
        │    │    ├── __init__.py
        │    │    └── landingPage/
        │    │         ├── __init__.py
        │    │         ├── landingPageMenu.py
        │    │         └── landingPageView.py
        │    ├── app.py
        │    ├── index.html
        │    └── version.py
        ├── venv/
        └── package.json
```
Use `npm start` to build and serve up application.


### Full-Stack Structure:

```
project/
  ├── .git/
  ├── client/
  │     ├── .git/  (Empty folder)
  │     ├── node_modules/
  │     ├── src/
  │     │    ├── common/
  │     │    │    ├── __init__.py
  │     │    │    ├── jsutils.py
  │     │    │    ├── pymui.py
  │     │    │    ├── pyreact.py
  │     │    │    └── urlutils.py
  │     │    ├── main/
  │     │    │    ├── __init__.py
  │     │    │    ├── aboutModal.py
  │     │    │    ├── appData.py
  │     │    │    ├── appTheme.py
  │     │    │    └── loginModal.py
  │     │    ├── static/
  │     │    │    ├── app_logo.jpg
  │     │    │    └── favicon.ico
  │     │    ├── views/
  │     │    │    ├── __init__.py
  │     │    │    └── landingPage/
  │     │    │         ├── __init__.py
  │     │    │         ├── landingPageMenu.py
  │     │    │         └── landingPageView.py
  │     │    ├── app.py
  │     │    ├── index.html
  │     │    └── version.py
  │     ├── venv/
  │     ├── dev-server.js
  │     ├── package.json
  │     └── requirements.txt
  └── server/
        ├── venv/
        ├── admin_routes.py
        ├── appserver.py
        └── requirements.txt
```
Use `npm run dev` to build and serve up application and proxy Flask.
