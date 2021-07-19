[<img src="static/images/veloroute_logo_crop.png" width="250">](https://velo-route.herokuapp.com/)

# VeloRoute Website

![VeloRoute](readme-files/velo-route-presented.png)

Cycling is a global and accessible sport that has shown a huge increase in popularity over recent years. The global market is for bicycles alone is in excess of $54 billion dollars. Alongside the growth in bicycle sales there has been significant growth in cycling related products such as GPS cycle computers and related software platforms that allow users to record, analyse and share their rides.

VeloRoute has been developed to allow users to share their favourite cycling routes, to search routes that other users have added to the site, to rate routes that have been added and to link to the routes that have been saved to platforms such as Strava and MapMyRide so that the routes can then be downloaded to their GPS devices.

The site was developed using knowledge gained from the Code Institute HTML Essentials, CSS Essentials, User Centric Frontend Development, Interactive Frontend Development and Backend Development modules.

View the live website [here.](https://velo-route.herokuapp.com/)

---

## Contents

1.  [User Experience Design](#user-experience-design)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Testing](#testing)
5.  [Deployment](#deployment)
6.  [Credits](#credits)

---

## User Experience Design

### Strategy

The key goals for developing the website are:

-   To provide users with an attractive interactive website that enables them to search for and find new cycling routes
    and find tips relating to cycling and cycling safety.
-   To allow users to securely register with VeloRoute and set up a username and password.
-   To allow returning users to log in to VeloRoute.
-   To enable users to add their favourite cycling routes.
-   To allow users to edit or delete their cycling routes.
-   To allow users to rate cycling routes that have been added to VeloRoute.
-   To allow admin users to edit cycling route categories and cycling tips.

### Scope

#### User Stories

#### Website Owner

-   As the website owner, I want branding to be clear and consistent across the website so that the user has a consistent experience.
-   As the website owner, I want the website latency to be optimised so that users are less likely to abandon the website whilst using it.
-   As the website owner, I want the website to be search engine optimised so that users can easily find our website.
-   As the website owner, I want the website to be accessible to all users so that all users can use our website.
-   As the website owner, I want the website to be conformant to web development best practices so that I know the development quality meets required standards.
-   As the website owner, I want the  website to be compatible with different browsers so that users have a consistent experience no matter which browser they use.

#### Users

-   As a user, I want to be able to access the website on all types of device so that i can use the device that is most convenient to me at the time.
-   As a user, I want a website that is clearly laid out and easy to navigate so that I can find the information i am looking for.
-   As a user, I want to register with VeloRoute with a secure username and password.
-   As a user, I want to find new cycling routes so that I can see try new recommended routes.
-   As a user, I want to be able to add my favourite cycling routes to the website.
-   As a user, I want my routes to be displayed on my profile page so that I can see routes I have previosuly submitted.
-   As a user, I want to be able to edit or delete routes that I have previously added to the VeloRoute.
-   As a user, I want to be able to view cycling tips that have been added to VeloRoute so that I can find tips to help me with my cycling.
-   As a user, I want to be able to rate cycling routes that have been added to the website.
-   As a user, I want to be able to follow a link to cycling routes that have been added to VeloRoute so that I can view the
    cycling route on platforms such as Strava.

#### Admin Users

-   As an admin user, I want to be able to log in to VeloRoute and have access to the same functionality that a standard website user has.
-   As an admin user, I want to be able to edit cycling route categories.
-   As an admin user I want to be able to edit cycling tips so that I can add or delete cycling tips.

### Structure

The VeloRoute website has been designed to provide an attractive, simple and easy to navigate website. The site has been developed to enable visitors to search for rides that have been submitted by users and to securely register and submit their own cycling routes.

The website has the following key elements:

-   A simple landing page design that provides information about VeloRoute and that presents cycling routes to the user.
-   A registration page that allows users to register with VeloRoute.
-   A log in page so that registered users can log in to VeloRoute.
-   A Routes page that allows users to search rides that have been submitted by registered users.
-   An Add Route page for users to add their favourite cycling routes to VeloRoute.
-   A user profile page that displays the user's details that they registered with and also displays the routes that the
    user has added to VeloRoute. The profile page is where users can edit routes they have previously submitted.
-   A cycling tips page offering tips related to cycling.
-   A categories page for admin users to edit route, difficulty levels and cycling tip categories.
-   A add cycling tips page for admin users to add and to edit or delete cycling tips.
-   A footer containing information about the VeloRoute team, social media links and copyright information.


_Notes:_

_........_

### Skeleton

#### Wireframes

The wireframes were developed using [Balsamiq](https://balsamiq.com/).

-   Small device [wireframes](design/veloroute-small-device.png).
-   Medium device [wireframes](design/veloroute-medium-device.png).
-   Large device [wireframes](design/veloroute-large-device.png).

After the initial design was finalised the following changes were made:

-   Change one ......

### Surface

VeloRoute features a clean and simple design with #263238 used for dark backgrounds and text and #fafafa for light backgrounds and text to provide good contrast. 

#### Branding

A simple VeloRoute logo was created using Canva.

#### Colours

A simple colour palette using #263238 for navigation and footer backgrounds and #fafafa for text to provide a good contrast whilst avoiding the potential eyestrain of using pure black and white. Images are used to add colour to the website. All icons with the exception of the social media icons use colour #607d8b. Social media icons use #fafafa.

#### Typography

Raleway font has been utilised for all text across the website. This is a simple and modern font available from the Google Fonts library which is unobtrusive and easy to read. Font Awesome icons have been utilised for icons throughout the site.

---

## Features

### Existing Features

#### Sections

#### Landing Page

-   VeloRoute logo that links to the home page.
-   A navigation menu on the top right of the website hero section that allows the user to navigate the website by clicking the navigation links. The navigation menu collapses to a burger icon on smaller devices.
-   A call to action button prompting users to join us at VeloRoute.
-   The six most recently added routes are displayed on medium and larger devices and the three most recently added routes are displayed on small devices.

#### Join Us Page

-   The Join Us page has a form for the user to provide their details so that the user can be registered.
-   Upon registration the user's details are stored in the MongoDB database with the password hashed for additional security.

#### Log In Page

-   The log in page provides a form for the user to log in to VeloRoute with the details they provided on registration.
-   The user is directed to their profile page when they log in.

#### Profile Page

-   The profile page displays the logged in user's profile details and the routes they have added which are displayed with the most recently added listed first.
-   The routes dsplyed can be edited by selecting the edit button or they can be deleted.

#### Routes Page

-   A section with introductory text and a map section with dropdown boxes to select a region and a race.
-   On selecting a region the user is presented with races in that region. On selecting a race the information section is populated with details about the race and the map is centred on the race location and a marker added to the map.

#### Cycling Tips Page

-   A section with introductory text and a map section with dropdown boxes to select a region and a race.
-   On selecting a region the user is presented with races in that region. On selecting a race the information section is populated with details about the race and the map is centred on the race location and a marker added to the map.

#### Footer Section

-   This section has copyright wording and links to Facebook, Twitter, YouTube, Instagram and Pinterest social media sites.

_Note: The social media links currently link to the social media websites and not VeloRoute specific pages_

#### Future features

-   The ability for users to add ratings to the routes that have been added.

---

## Technologies Used

The following technologies have been used to complete the UX design, capture user stories and defects and assign for development and to develop the Urban Paws website.

### Languages

-   [HTML5](https://en.wikipedia.org/wiki/HTML5) - used for the structure and content of the Trail Running UK website.
-   [CSS3](https://en.wikipedia.org/wiki/CSS) - used to style the Trail Running UK website.
-   [jQuery](https://jquery.com/)- used for scripts for the why trail running and races sections of the Trail Running UK website and for the newsletter.
-   [Python](https://www.python.org/) - used to style the Trail Running UK website.

### Frameworks - Libraries - Other

-   [Materialize](https://getbootstrap.com/) - utilised for the front-end design framework.
-   [MongoDB](https://www.mongodb.com/) - used as the database for the project.
-   [GitHub](https://github.com/) - for hosting the website repository.
-   [GitPod](https://gitpod.io/) - used as the development environment for the website.
-   [Google Fonts](https://fonts.google.com/) - used to source the Raleway font used throughout the website.
-   [Font Awesome](https://fontawesome.com/) - used to source icons for use throughout website.
-   [Balsamiq](https://balsamiq.com/) - utilised for the development of the website wireframes.
-   [Canva](https://canva.com/) - used for the design of the VeloRoute website logo.
-   [Beautify Tools](https://beautifytools.com/javascript-validator.php) - for the validation of the JavaScript code.
-   [Markup validation service](https://validator.w3.org/) - for the validation of HTML5 code.
-   [CSS validation service](https://jigsaw.w3.org/css-validator/) - for the validation of the CSS3 code.

### Testing tools used

-   [Google Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) - used to edit changes prior to implementing the code changes, to diagnose problems and for performance, accessibility, best practice and search engine optimisation testing.
-   [Autoprefixer](https://autoprefixer.github.io/) - Autoprefixer is used to parse the CSS and to add vendor prefixes to CSS rules. 
-   [Markup validation service](https://validator.w3.org/) - for the validation of HTML5 code.
-   [CSS validation service](https://jigsaw.w3.org/css-validator/) - for the validation of the CSS3 code.
-   [JShint](https://jshint.com/) - used to check for errors in the JavaScript code. 
-   [PEP8](http://pep8online.com/) - used to check for errors in the Python code.

---

## Testing

Full details of testing are contained in the [testing document](README.md).

### Deployment

#### Requirements

To be able to deploy this project you will need the following:

- Python3 
- A Github account 
- A MongoDB account 
- A Heroku account

#### To clone the project locally

To clone this project from GitHub.

1.  Open the project repository on GitHub and click the **Code** dropdown button.
2.  Select the **HTTPS** tab and copy the URL.
3.  Open your terminal (Mac OS, Linux) or Git-Bash terminal (Windows).
4.  Change the current working directory to the location where you want the cloned directory to be created.
5.  Type **git clone**, enter a space and then paste the URL copied from GitHub.
6.  Press **Enter** and the local clone will be created in the specified directory.

#### Working with the local copy

1. Install all the requirements: Go to the workspace of your local copy. In the terminal window of your IDE type: **pip3 install -r requirements.txt**.
2. Create a database in MongoDB  
    - Signup or login to your MongoDB account.
    - Create a cluster and a database.
    - Create six collections in the database: **categories, cycling_tips, cycling_tip_categories, difficulty_levels, routes, users.**
    - Add the data to the collections. See <a href="#ux-architecture">my Information architecture</a> how the database is set up for this project.
3. Create the environment variables 
    - Create a .gitignore file in the root directory of the project.
    - Add the env.py file in the .gitignore.
    - Create the file env.py. This  will contain all the envornment variables.

    ```
    Import os
    os.environ.setdefault("IP", "Added by developer")
    os.environ.setdefault("PORT", "Added by developer")
    os.environ.setdefault("SECRET_KEY", "Added by developer")
    os.environ.setdefault("MONGO_URI", "Added by developer")
    os.environ.setdefault("MONGO_DBNAME", "Added by developer")
    ```
4. Run the app: Open your terminal window in your IDE. Type python3 app.py and run the app.

#### Heroku Deployment  
1. Set up local workspace for Heroku 
    - In terminal window of your IDE type: **pip3 freeze -- local > requirements.txt.** (The file is needed for Heroku to know which filed to install.)
    - In termial window of your IDE type: **python app.py > Procfile** (The file is needed for Heroku to know which file is needed as entry point.)
2. Set up Heroku: create a Heroku account and create a new app and select your region. 
3. Deployment method 'Github'
    - Click on the **Connect to GitHub** section in the deploy tab in Heroku. 
        - Search your repository to connect with it.
        - When your repository appears click on **connect** to connect your repository with the Heroku. 
    - Go to the settings app in Heroku and go to **Config Vars**. Click on **Reveal Config Vars**.
        - Enter the variables contained in your env.py file. it is about: **IP, PORT, SECRET_KEY, MONGO_URI, MONGO_DBNAME**
4. Push the requirements.txt and Procfile to repository. 
     ```
    $ git add requirements.txt
    $ git commit -m "Add requirements.txt"

    $ git add Procfile 
    $ git commit -m "Add Procfile"
    ```
5. Automatic deployment: Go to the deploy tab in Heroku and scroll down to **Aotmatic deployments**. Click on **Enable Automatic Deploys**. By **Manual deploy** click on **Deploy Branch**.

Heroku will receive the code from Github and host the app using the required packages. 
Click on **Open app** in the right corner of your Heroku account. The app wil open and the live link is available from the address bar. 


**To run the project locally**

To clone this project from GitHub.

1.  Open the project repository on GitHub and click the **Code** dropdown button.
2.  Select the **HTTPS** tab and copy the URL.
3.  Open your terminal (Mac OS, Linux) or Git-Bash terminal (Windows).
4.  Change the current working directory to the location where you want the cloned directory to be created.
5.  Type **git clone**, enter a space and then paste the URL copied from GitHub.
6.  Press **Enter** and the local clone will be created in the specified directory.

## Credits

### Content

All text content included in the Urban Paws website is my own.

Comments have been included in the code for code that has been sourced and adapted for this website.

### Media

-   All images, with the exception of the topography image below, were licensed for use from [Adobe Stock](https://stock.adobe.com/).

### Acknowledgements

-   [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/?originalSubdomain=ng) for mentor guidance and support.
