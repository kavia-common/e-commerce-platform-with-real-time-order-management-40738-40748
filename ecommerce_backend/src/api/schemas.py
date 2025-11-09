from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from .models import OrderStatusEnum, ReturnStatusEnum


# AUTH

class Token(BaseModel):
    """JWT token response."""
    access_token: str = Field(..., description="The JWT access token to use for Authorization header.")
    token_type: str = Field("bearer", description="The token type (always 'bearer').")


class TokenData(BaseModel):
    """Decoded token data."""
    user_id: int = Field(..., description="Authenticated user id.")


class UserBase(BaseModel):
    """Base user fields."""
    email: EmailStr = Field(..., description="Email address of user.")
    full_name: Optional[str] = Field(None, description="Full name of the user.")


class UserCreate(UserBase):
    """User registration payload."""
    password: str = Field(..., description="Plain-text password for registration.")


class UserLogin(BaseModel):
    """User login payload."""
    email: EmailStr = Field(..., description="Email address.")
    password: str = Field(..., description="Plain-text password.")


class UserOut(UserBase):
    """User public profile."""
    id: int = Field(..., description="User id.")
    created_at: datetime = Field(..., description="Creation timestamp.")

    class Config:
        from_attributes = True


# PRODUCTS & ORDERS

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name.")
    description: Optional[str] = Field(None, description="Product description.")
    price: float = Field(..., description="Unit price.")


class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int = Field(..., description="ID of product.")
    quantity: int = Field(..., description="Quantity ordered.")
    unit_price: float = Field(..., description="Unit price at time of order.")


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: OrderStatusEnum = Field(..., description="Order status.")
    total_amount: float = Field(..., description="Order total amount.")


class OrderCreate(BaseModel):
    user_id: int = Field(..., description="Owner user id.")
    items: List[OrderItemBase] = Field(..., description="Line items.")


class OrderUpdateStatus(BaseModel):
    status: OrderStatusEnum = Field(..., description="New order status.")


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: OrderStatusEnum
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True


# RETURNS

class ReturnPolicyOut(BaseModel):
    id: int
    product_id: Optional[int]
    policy_text: str
    days_to_return: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReturnCreate(BaseModel):
    order_id: int = Field(..., description="ID of order being returned.")
    order_item_id: int = Field(..., description="ID of specific order item.")
    reason: Optional[str] = Field(None, description="Reason for the return request.")


class ReturnOut(BaseModel):
    id: int
    user_id: int
    order_id: int
    order_item_id: int
    reason: Optional[str]
    status: ReturnStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# RECOMMENDATIONS

class RecommendationOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    score: float
    created_at: datetime

    class Config:
        from_attributes = True
