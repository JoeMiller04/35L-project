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

API requests are handled by FastAPI. The server main is found at `server/main.py`. API routing is found in `server/api/`. Models for API request/response and MongoDB interfacing is found is `server/models/`.

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

## Sources

### UCLA Grade Distributions

UCLA Grade Distributions are saved in `server/data/uclagrades`
This data was sourced from [uclagrades.com](https://www.uclagrades.com/). See their [Github Repo](https://github.com/nathanhleung/uclagrades.com/tree/main). The grade distribution data was sourced through a February 2023 public records request made under the California Public Records Act.

### Backend Contributors

Joseph Miller, ...
