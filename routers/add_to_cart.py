# routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from oauth2 import get_current_admin_user, get_current_user
from models import User, Cart, Item, CartItem
import schemas

router = APIRouter(
    tags=["Cart"]
)


@router.post("/cart/items", response_model=schemas.CartItem)
async def add_item_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    db_item = db.query(Item).filter(Item.id == item.item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.item_id == item.item_id).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, item_id=item.item_id, quantity=item.quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.get("/cart/checkout", response_model=schemas.CheckoutResponse)
async def checkout_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    total_value = sum(item.item.price * item.quantity for item in cart.items)

    return schemas.CheckoutResponse(total_value=total_value, items=cart.items)


@router.post("/cart/purchase", response_model=dict)
async def purchase_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve the user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

    for cart_item in cart.items:
        db.delete(cart_item)
    db.commit()

    return {"message": "Purchase successful"}
