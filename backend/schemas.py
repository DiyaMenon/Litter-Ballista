from pydantic import BaseModel, Field

class ScoreCreate(BaseModel):
    player_name: str = Field(..., examples=["Diya"])
    score: int = Field(..., examples=[120])

    class Config:
        from_attributes = True