# Home Fur Good

**Live URL:** _deployed URL goes here (example: https://homefurgood.onrender.com)_

## Description

Home Fur Good is a full-stack web application that connects users with adoptable dogs via the Petfinder API. It allows users to search for dogs using multiple filters, save favorites, and explore spotlight dogs on the homepage.

The goal of this app is to make it easy and fun for users to find their perfect furry companion — and to help dogs in need find their FURever homes.

## Features

- User registration and login (with secure password hashing)
- Spotlight section highlighting adoptable dogs on the homepage
- Detailed search form with filters (breed, size, age, location, etc.)
- Ability for logged-in users to save favorite dogs
- Favorites page to view and manage saved dogs
- Responsive and mobile-friendly design

## Tests

- Tests are located in the `/tests` folder
- To run all tests:

```terminal
python -m unittest discover -s tests
```

- Tests cover:
  - User model and authentication
  - Favorites routes (saving and removing dogs)
  - Auth routes (signup, login, logout)
  - Form validation
  - Home/search routes (basic checks)

## Standard User Flow

1. User lands on homepage and sees spotlight dogs
2. User can use page without sign up or logging in by clicking **Find a Pup** or the search icon in the nav bar to bring them to the search form to look for adoptable dogs by criteria
3. User can click on the dog photo to bring them to the Petfinder official page to see all the dog's info
4. User can sign up for a new account or log in
5. After logging in, user can search and NOW favorite and unfavorite dogs which will be saved in their favorite dog's list
6. User can view saved dogs on the **My Favorites** page
7. User can log out

There is also a seed file (optional) to run to generate 2 users already signed up with a favorite dog in their list so one can easily see the function of the page in use.

## API Usage

- The app integrates with the [Petfinder API](https://www.petfinder.com/developers/v2/docs/).
- Data used:
  - Dog name, age, breed, photo, description, size, gender, good with dogs, good with cats etc.
- Token-based OAuth2 authentication is implemented to access API.
- Internal logic handles cases where dogs may have missing photos.

## Technology Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (vanilla), Jinja templates
- **Forms & Auth:** Flask-WTF, Flask-Login, Flask-Bcrypt
- **API:** Petfinder API

## Notes

- A stretch goal for this project would be adding an admin dashboard to view user data and manage featured dogs.
- Another stretch goal is to add a weekly newsletter with more spotlighted dogs to generate interest and searching. 
- Most interested in being able to highlight at risk dogs in kill shelters, still figuring out a way to accomplish this! 



© 2025 Home Fur Good — Built by Meghan Spellman 🐾