from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import Order, User
from .schemas import OrderOut, OrderUpdateStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    "",
    response_model=List[OrderOut],
    summary="List orders",
    description="List orders for the current user. Admins not implemented; returns only user's orders.",
)
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all orders for the authenticated user."""
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return orders


@router.get(
    "/{order_id}",
    response_model=OrderOut,
    summary="Get order by id",
    description="Retrieve a specific order by id if it belongs to the current user.",
)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get specific order by id for the authenticated user."""
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch(
    "/{order_id}/status",
    response_model=OrderOut,
    summary="Update order status",
    description="Update the status of an order owned by the current user. Real apps would restrict allowed transitions.",
)
def update_order_status(
    order_id: int,
    payload: OrderUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update order status; basic validation and ownership check."""
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.status = payload.status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
