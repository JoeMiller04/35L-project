# 35L Project Frontend

A React multi-page app for helping UCLA students plan course schedules
This is a README specifically for the frontend

## Frontend

This project was created using Create React App. 

### Setup

1. Navigate to the `client` directory:
   ```
   cd client
   ```

2. Install dependencies

   ```
   npm install
   ```

   A list of dependencies is in the package.json file. 

3. Start the development server

   ```
   npm start
   ```

### File Contents

`public/index.html`: Contains html file where React app is rendered.

`App.css`: Contains styles for `LogIn.js` and `CreateUser.js`.

`App.js`: Contains paths for page navigation.

`CreateUser.js`: This is the file that displays the page to create new users. It can be navigated to from `LogIn.js`.

`LogIn.js`: Contains page for users to login. This is the defualt page that the user is sent to when the app is launched. The user can navigate to the pages associated with `CreateUser.js` or `Home.js` from here. 

`Home.js`: This is the main page of the application that contains the schedule and course query. Users can search for a class based on term, catalog, and/or department, which will lead to results that the user can add to their plan. You can navigate to the Past Classes page, Future Plan page, and Remove Classes Page via buttons at the top. The user can also navigate to the More Info page by clicking on the buttons that are rendered on search results for classes. 

`FuturePlanner.js`: This is the page that allows the user to input their course plans for the future. You can add a plan for classes ranging from 25W to 28F. The Past Courses Page is used to automatically render past courses on the right side of the page. The user can navigate back to the Home page or to Past Classes from here. 

`PastCourses.js`: This page lets the user input their past classes so that they appear on the Future Plan page. There is an upload button that will only take student DARS files. Uploading a DARS file here will automatically check off classes in the list that the user has taken or is currently taking. The user can navigate to Future Planner or Home from here. In both `FuturePlanner.js` and `PastCourses.js`, there is a change major button that can be used to display different courses depending on what major you are. This defaults to CS, and only supports CS and CSE as of now. 

`InfoPage.js`: This page displays all of the classes in your current schedule in a clean format. This is where the user can remove current classes from their schedule. They can also navigate to the info page about classes from here. (the name of this page is not accurate).

`SearchPage.js`: This page displays all the information about a specific class. It can be accessed via home and `InfoPage.js`. It includes a short description, ratings, and grade distributions. 

## Usage

1. **Log-in/Create user**: Users will be prompted to create an account when they first visit the applicaiton
2. **Search for Classes**: Users will be able to query for UCLA classes on the home page. Classes from the last few years will appear with information about the class. 
3. **Add/Remove Classes**: Users have the option to add/remove classes from their schedule
4. **Plan Future Schedule**: Users can add classes to their future schedule and validate 
5. **Add Past Courses**: Users can upload DARS in order to check off classes that they have taken
