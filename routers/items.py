from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from oauth2 import get_current_admin_user
from database import get_db
from schemas import ItemCreate
from models import User, Item
import time

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/", response_model=list[ItemCreate])
async def get_items(db: Session = Depends(get_db)):
    start_time = time.time()
    items = db.query(Item).all()
    end_time = time.time()
    print(end_time - start_time)
    return items


@router.get("/{id}", response_model=ItemCreate)
async def get_items(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post("/additems", response_model=ItemCreate)
async def create_item(item: ItemCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_admin_user)):
    try:
        if not current_user.role == "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")

        db_item = Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item
    except Exception as e:
        print(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_admin_user)):
    try:
        if not current_user.role == "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        db_item = db.query(Item).filter(Item.id == id).first()
        db.delete(db_item)
        db.commit()
        return {"message": "Item successfully deleted"}
    except Exception as e:
        print(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
