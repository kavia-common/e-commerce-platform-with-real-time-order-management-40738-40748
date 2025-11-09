from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import Recommendation, User
from .schemas import RecommendationOut

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get(
    "",
    response_model=List[RecommendationOut],
    summary="Get recommendations for current user",
    description="Return personalized product recommendations for the authenticated user.",
)
def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return recommendations for current user ordered by score desc."""
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == current_user.id)
        .order_by(Recommendation.score.desc())
        .all()
    )
    return recs
