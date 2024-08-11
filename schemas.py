from typing import Optional

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    role: Optional[str] = "user"


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    role: str

    class Config:
        form_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    role: str


class CartItemCreate(BaseModel):
    item_id: int
    quantity: int


class CartItem(BaseModel):
    id: int
    item: ItemCreate
    quantity: int

    class Config:
        from_attributes = True


class Cart(BaseModel):
    id: int
    items: list[CartItem] = []

    class Config:
        from_attributes = True


class CheckoutResponse(BaseModel):
    total_value: float
    items: list[CartItem]

    class Config:
        from_attributes = True
