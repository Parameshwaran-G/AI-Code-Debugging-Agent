from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.models.review_request import ReviewRequest
from backend.app.services.review_service import ReviewService

app = FastAPI()

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
review_service = ReviewService()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Code Review Agent",
        "status": "Running"
    }


@app.post("/review")
def review_code(request: ReviewRequest):
    return review_service.review(request.code)