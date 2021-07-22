# VeloRoute Testing

---

## Contents 

1.  [Code Validation](#code-validation)
2.  [Browser Compatibility](#browser-compatibility)
3.  [Responsiveness](#responsiveness)
4.  [Lighthouse Reports](#lighthouse-reports)
5.  [User Story Testing](#user-story-testing)
6.  [Defensive Design Testing](#defensive-design-testing)
7.  [Defects](#defects)

---

## Code Validation
 - **[HTML Validator](https://validator.w3.org/):**
    - ...


- **[CSS Validator](https://jigsaw.w3.org/css-validator/):**

- **[JS Hint](https://jshint.com/):**

- **[Python validator | PEP8](http://pep8online.com/):** 



---

## Browser Compatibility 
- Responsiveness of the site has been tested with [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) and [Responsive Design Checker](https://www.responsivedesignchecker.com/).
- The site has been tested on the following devices: 
    - Desktop: 1024px, 1366px, 1440px, 1600px and 1680px. 
    - Mobile & Tablet: Galaxy S5, iPhone 5/SE, iPhone 6/7/8, iPhone 6/7/8 plus, iPhone x, iPad and  iPad Pro

![Responsiveness testing](testing-files/responsiveness-testing.png)

### Notes
- ....

---

## Responsiveness
![Browser compatibility](testing-files/browser-compatibility.png)

--- 

## Lighthouse Reports
![Browser compatibility](testing-files/browser-compatibility.png)

--- 

## User Story Testing

The user stories below have all been tested against defined acceptance criteria. The full test results for all user stories are detailed in attached [testing report](testing-files/veloroute-user-story-testing.pdf).

### Website Owner

-   As the website owner, I want branding to be clear and consistent across the website so that the user has a consistent experience.
-   As the website owner, I want the website to be search engine optimised so that users can easily find our website.
-   As the website owner, I want the website to be accessible to all users so that all users can use our website.
-   As the website owner, I want the website to be conformant to web development best practices so that I know the development quality meets required standards.
-   As the website owner, I want the  website to be compatible with different browsers so that users have a consistent experience no matter which browser they use.

### Users

-   As a user, I want to be able to access the website on all types of device so that I can use the device that is most convenient to me at the time.
-   As a user, I want a website that is clearly laid out and easy to navigate so that I can find the information I am looking for.
-   As a user, I want to register with VeloRoute with a secure username and password.
-   As a user, I want to find new cycling routes so that I can see try new recommended routes.
-   As a user, I want to be able to add my favourite cycling routes to the website.
-   As a user, I want my routes to be displayed on my profile page so that I can see routes I have previously submitted.
-   As a user, I want to be able to edit or delete routes that I have previously added to the VeloRoute.
-   As a user, I want to be able to view cycling tips that have been added to VeloRoute so that I can find tips to help me with my cycling.
-   As a user, I want to be able to follow a link to cycling routes that have been added to VeloRoute so that I can view the cycling route on platforms such as Strava.

### Admin Users

-   As an admin user, I want to be able to log in to VeloRoute and have access to the same functionality that a standard website user has.
-   As an admin user, I want to be able to edit cycling route, cycling tip and difficulty level categories.
-   As an admin user I want to be able to edit cycling tips so that I can add or delete cycling tips.
-   As an admin user I want to be able to add cycling tips so that I can present new cycling tips to VeloRoute users.

#### IT Users

-   As an IT user, I want to be able to create, edit and delete cycling route, cycling tip and difficulty level categories so that I can make updates to the database when new categories are required.



---

## Defensive Design Testing

1. When deleting routes, cycling tips or categories on the site a modal will appear where the user has to confirm that they want to delete the item. Once they have confirmed then the item will be deleted.
2. Validation has been included on all form fields as listed and tested below:

**Join Us form**

-   Field one
-   Field two

**Log In form**

**Add Route form**

**Add Cycling Tip form**

**Add Category forms**



---

## Defects

1.  It was discovered during testing that the Matrialize modals implementented to confirm the deletion of items across the app were deleting the wrong object. This was resolved by implementing loop indexing which had to be further refined on the Manage Categories page to loop through the individual gategory types to ensure the correct object id was sourced for deletion.
2.  It was noticed during testing that the Materialize sticky footer functionality had stopped working. This was resolved by changing the code for the base.html page to revise the structure and removing an erroneous character from the related CSS code.
3.  A defect was discovered that the images that were presented on the home page were in the reverse order to those on the routes and profile page. This was corrected by adding a reverse sort order to the query for the home page display for small and medium/large devices. The images now display with the most recently added first as with the profile and home pages.

---

[Link to README.md file](README.md).