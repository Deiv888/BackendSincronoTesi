from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db, engine
from typing import List

router = APIRouter(
    tags=['Users']
)

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_new_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):


    #controllo se utente con questa email esiste già
    existing_account = db.query(models.User).filter(models.User.email == new_user.email).first()
    if existing_account:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Esiste già un account con questa email: {new_user.email}")
    
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password

    new_user_to_register = models.User(**new_user.model_dump())
    
    #creo i due wallet eur e btc per user
    new_eur_wallet = models.Wallet(
        currency = "EUR",
        balance = "0",
        )
    new_btc_wallet = models.Wallet(
        currency = "BTC",
        balance = "0",
        )
    
    new_user_to_register.wallets.append(new_eur_wallet)
    new_user_to_register.wallets.append(new_btc_wallet)
    db.add(new_user_to_register)
    db.commit()
    db.refresh(new_user_to_register)
    return new_user_to_register
    

