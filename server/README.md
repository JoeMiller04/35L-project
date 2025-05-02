# 35L Project Backend

This will be a README specifically for the backend.

## Backend

This project includes a FastAPI backend with MongoDB integration. Below are the details for setting up and running the backend.

### Requirements

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

### TODO

Add MongoDB for backend storage.

### UCLA Grade Distributions

UCLA Grade Distributions are saved in `server/data/uclagrades`
This data was sourced from [uclagrades.com](https://www.uclagrades.com/). See their [Github Repo](https://github.com/nathanhleung/uclagrades.com/tree/main). The grade distribution data was sourced through a February 2023 public records request made under the California Public Records Act.

### Backend Contributors

Joseph Miller, ...
