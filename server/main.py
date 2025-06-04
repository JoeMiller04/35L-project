from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.user import router as user_router
from server.api.course import router as course_router
from server.api.validation import router as valid_router
from server.api.rating import router as ratings_router
from server.api.your_upload_route import router as upload_router
from server.api.description import router as description_router

app = FastAPI()

origins = [
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the 35L Project API!"}


app.include_router(user_router, tags=["users"])
app.include_router(course_router, tags=["courses"])
app.include_router(valid_router, tags=["valid"])
app.include_router(ratings_router, tags=["ratings"])
app.include_router(upload_router, tags=["uploads"])
app.include_router(description_router, tags=["descriptions"])