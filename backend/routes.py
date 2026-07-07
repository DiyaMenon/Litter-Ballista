from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .models import LeaderboardRecord
from . import schemas

router = APIRouter()

@router.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Litter Ballista Backend"
    }

@router.get("/leaderboard", response_model=List[schemas.LeaderboardResponse])
def get_leaderboard(db: Session = Depends(get_db)):
    # Retrieve records sorted by score in descending order
    leaderboard_data = db.query(LeaderboardRecord).order_by(LeaderboardRecord.score.desc()).all()
    return leaderboard_data

@router.post("/score", response_model=schemas.SuccessResponse)
def submit_score(payload: schemas.ScoreCreate, db: Session = Depends(get_db)):
    # Create a new persistence model instance from payload data
    new_record = LeaderboardRecord(
        player_name=payload.player_name,
        score=payload.score
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    return {
        "success": True
    }