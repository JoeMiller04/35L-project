from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.user import router as user_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the 35L Project API!"}


app.include_router(user_router, tags=["users"])