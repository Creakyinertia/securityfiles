from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from shared.models import Users
from shared.schemas import User
from shared.database import SessionLocal
from datetime import timedelta
from typing import Annotated
from fastapi import Depends,HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(
    
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# @router.get("/")
# def get_all_Users(db: Session):
#     return db.query(Users).all()
@router.get("/")
def get_all_Users(db: Session = Depends(get_db)):
    return db.query(Users).all()

@router.get("/{customer_id}")
def get_customer_based_on_id(customer_id: int,db: Session = Depends(get_db)):
    db_customer = db.query(Users).filter(Users.id == customer_id).first()
    return db_customer

@router.post("/", response_model=User)
def create_new_customer(customer: User, db: Session = Depends(get_db)):
    CAPSname = customer.name.upper()
    new_customer = Users(
        name=CAPSname,
        phone=customer.phone,
        number_of_guests=customer.number_of_guests,
        room_number=customer.room_number,
        Bill=customer.Bill,
        aadhar=customer.aadhar,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: User, db: Session = Depends(get_db)):
    db_customer = db.query(Users).filter(Users.id == customer_id).first()
    if db_customer:
        for attr, value in vars(customer).items():
            setattr(db_customer, attr, value) if value is not None else None
        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None

@router.delete("/{customer_id}",response_model=User)
def delete_customer_record(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Users).filter(Users.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="customer not found")
    db.delete(db_customer)
    db.commit()
    return db_customer

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/users/me/items/") 
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):  
    return [{"item_owner": current_user.username}]