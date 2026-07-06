from fastapi import FastAPI

from backend.app.models.review_request import ReviewRequest
from backend.app.services.review_service import ReviewService

app = FastAPI()

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