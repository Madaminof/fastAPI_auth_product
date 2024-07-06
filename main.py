from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Product
from schemas import SignUp, ProductCreate, Product as ProductSchema
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

app = FastAPI()

class Signup(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True
    is_staff: bool = False

    class Config:
        from_attributes = True

@app.post("/signup/", response_model=Signup)
def signup(user: Signup, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = generate_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[Signup])
def get_users(db: Session = Depends(SessionLocal)):
    return db.query(User).all()

@app.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(SessionLocal)):
    db_product = db.query(Product).filter(Product.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = Product(
        name=product.name,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(SessionLocal)):
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(SessionLocal)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(SessionLocal)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(SessionLocal)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
