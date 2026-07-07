from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class LeaderboardRecord(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True, nullable=False)
    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)