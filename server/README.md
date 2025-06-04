# 35L Project Backend

This will be a README specifically for the backend.

This project includes a FastAPI backend with MongoDB integration. Below are the details for setting up and running the backend.

## Requirements

Make sure you have the following installed:

- Python 3.7 or higher

### Installation

1. Navigate to the `server` directory:
   ```
   cd server
   ```
2. Install the required packages:
   ```
   conda create --name NAME python=3.13
   conda activate NAME
   pip install -r requirements.txt
   ```

### Running the Application

To start the FastAPI application, run the following command from the `35L-Project` directory:

```
uvicorn server.main:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

### API Documentation

Once the server is running, you can access the interactive API documentation at:

```
http://127.0.0.1:8000/docs
```

### MongoDB

Make sure you have MongoDB installed.
MongoDB definitions and collections can be found in `db/mongodb.py`

### Testing

Run `pytest` in project root directory to confirm that the server and database are working. Some tests may require that the database is up to date.

## API

API requests are handled by FastAPI. The server main is found at `main.py`. API routing is found in `api/`. Models for API request/response and MongoDB interfacing is found is `models/`.

### Course API

This file implements API for managing and querying courses in the database. Some API are protected by admin keys.
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /courses | Create new course (admin only) |
| GET | /courses{course_id} | Get a specific course by ID |
| PUT | /courses{course_id} | Update a course (admin only) |
| DELETE | /courses{course_id} | Delete a course (admin only) |
| GET | /courses | Query courses with filters |
| GET | /courses/catalogs/{subject} | Get all catalog numbers for a subject |
| get | /subjects | Get all available subject codes |

### Description API

This file implements API for fetching descriptions of courses.
Pass in subject and catalog number to receive description and other information for that course.

### Rating API

This file implements API for fetching ratings of courses. Pass in subject and catalog number to receive rating for that course.

### Security API

This file implements the authentication check for the admin key for protected calls. The admin key is stored in a local `.env` file.

### User API

This file contains API that handles user-specific requests. User info is protected by their user id token, which can be accessed by logging in with a username and password.
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /users | Creates a new user |
| GET | /users{user_id} | Returns user info |
| POST | /login | Returns user token |
| DELETE | /users{user_id} | Deletes a user (admin only) |
| POST | /users/{user_id}/courses | Updates a user's past courses |
| GET | /users/{user_id}/courses | Gets a user's past courses |
| POST | /users/{user_id}/course-list | Updates a user's calendar |
| GET | /users/{user_id}/course-list | Gets a user's calendar |

### Upload API

This file implements API for uploading a DARS file. This will read in a user's info from the file an update their past course information appropriately.

## Data

### Bruinwalk Reviews

`data/bruinwalk_reviews/` contains a script to pull ratings from and a script to upload the data to MongoDB.

Please add to description.

### DARS

`data/Dars/` contains a script to read DARS html files an extract past courses.

### Descriptions

`data/Kyle/` contains a script to pull course descriptions from the [UCLA Registrar](https://registrar.ucla.edu/academics/course-descriptions?). It uploads new information to the database.

### Prerequisites

Please add a description.

### Grade Distributions

`data/uclagrades/` contains scripts to process and upload data from UCLA Grades to the database.

### Registar Scraper

`data/scrape-test/` contains a script `scrape.py` that scrapes course info from the [UCLA Registrar](https://sa.ucla.edu/ro/public/soc/). The results are stored as json files. json files in `data/scrape-test/course_data` can be uploaded by `load_scraped.py` to the database. `combine_json_files.py` can combine multiple json files for portability.

### Example Courses

For testing purposes `clone_real_courses.py` can take existing courses in the database and add random times to them. To remove example coures, `clean_db.py` removes all fake courses from the database.

## Mongo Database

The **users** collection stores user data including username, password hash, past courses, and calendar.  
The **courses** collection stores course data for specific courses including term, subject, catalog number, instructor, times, and title.  
The **course_ratings** collection stores ratings for courses.  
The **descriptions** collection stores descriptions for courses.

Please add descriptions for the colections Aliases, pre-reqs, profesor_ratings, sample, previous courses, and future courses.

## Other

### Tests

Tests are saved under `tests/`. They contain pytest tests to verify API for courses, users, descriptions, and ratings.

### src

Please add a description.

### utils

Please add a description.

### services

Please add a description.

## Sources

### UCLA Grade Distributions

UCLA Grade Distributions are saved in `data/uclagrades`
This data was sourced from [uclagrades.com](https://www.uclagrades.com/). See their [Github Repo](https://github.com/nathanhleung/uclagrades.com/tree/main). The grade distribution data was sourced through a February 2023 public records request made under the California Public Records Act.

### UCLA Registrar Website

Course info was read from UCLA Registrar.

### Bruinwalk

Please add a description

### Backend Contributors

- **Joseph Miller**: API, MongoDB, Course Scraping, Grade Distributions, DARS
- **Kyle Reisinger**: Scraper, API, and testing for course descriptions

  Please add role descriptions for Arian Dehnavizadeh, Johnny Duong, Samuel Oh.
