# Getting Started with Python Create React App

This project was bootstrapped with [Python Create React App](https://github.com/JennaSys/pcra).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:1234](http://localhost:1234) (or [http://localhost:8080](http://localhost:8080) for a full-stack application) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm run build`

Builds the app for production to the `dist/prod` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

### `npm version`

If Git was installed and the Git working directory is clean, you can use the following npm commands to version your application:  
`npm version patch`  
`npm version minor`  
`npm version major`  

These commands will update the npm **package.json** file, create a **version.py** file so you can access the version number from your application, then tag and commit the project with the current version.

### `npm run dev`

If you provided the `--full-stack` option, you will want to use the `npm run dev` command to build and serve up your application instead of using `npm start`.
The development server that this command starts is also capable of forwarding (or proxying) requests to the back-end Flask server as well.

In development mode, the Flask server can be started using `python -m appserver` and is configured to be listening for requests on port 8000.
Any URLs coming into the development server that start with `/api/` will be forwarded on to the Flask server. 

### Analyzing the Bundle Size

After running a production build, there will be a **report.html** file in the production distribution folder can be opened in a web browser to get a visual breakdown of all of the bundled application dependencies.
