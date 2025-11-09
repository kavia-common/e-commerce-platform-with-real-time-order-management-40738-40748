from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import Return, ReturnPolicy, OrderItem, Order, User
from .schemas import ReturnPolicyOut, ReturnCreate, ReturnOut

router = APIRouter(prefix="/returns", tags=["Returns"])


@router.get(
    "/policies",
    response_model=List[ReturnPolicyOut],
    summary="List return policies",
    description="List all return policies (global or per product).",
)
def list_policies(db: Session = Depends(get_db)):
    """Return all return policies."""
    policies = db.query(ReturnPolicy).order_by(ReturnPolicy.created_at.desc()).all()
    return policies


@router.post(
    "",
    response_model=ReturnOut,
    summary="Create a return request",
    description="Create a return request for an order item owned by the current user.",
)
def create_return(payload: ReturnCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a return request for an order item ensuring ownership."""
    order = db.query(Order).filter(Order.id == payload.order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    item = db.query(OrderItem).filter(
        OrderItem.id == payload.order_item_id,
        OrderItem.order_id == order.id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")

    ret = Return(
        user_id=current_user.id,
        order_id=order.id,
        order_item_id=item.id,
        reason=payload.reason,
    )
    db.add(ret)
    db.commit()
    db.refresh(ret)
    return ret


@router.get(
    "/{return_id}",
    response_model=ReturnOut,
    summary="Get return by id",
    description="Retrieve a return request if it belongs to the current user.",
)
def get_return(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a return request by id owned by current user."""
    ret = db.query(Return).filter(Return.id == return_id, Return.user_id == current_user.id).first()
    if not ret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Return not found")
    return ret
