from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas

router = APIRouter()

@router.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Litter Ballista Backend"
    }

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    return []

@router.post("/score")
def submit_score(payload: schemas.ScoreCreate, db: Session = Depends(get_db)):
    return {
        "success": True
    }