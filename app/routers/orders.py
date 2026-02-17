import time
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import oauth2
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    tags=['Orders']
)

@router.post("/deposit", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderResponse)
def deposit(deposit: schemas.DepositCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    #recupero il wallet dell'utente
    wallet = db.query(models.Wallet).filter(models.Wallet.owner_id == current_user.id, models.Wallet.currency == "EUR").with_for_update().first()

    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Impossibile recuperare il wallet EUR associato al tuo account")
    wallet.balance += deposit.amount

    #creo la transazione nella tabella orders
    order = models.Order(
        wallet_id = wallet.id,
        type = "DEPOSIT",
        asset = "EUR",
        amount = deposit.amount,
        price = "1",
        status = "COMPLETED"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.post("/withdrawal", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderResponse)
def withdrawal(withdrawal: schemas.WithdrawalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    #recupero il wallet dell'utente
    wallet = db.query(models.Wallet).filter(models.Wallet.owner_id == current_user.id, models.Wallet.currency == "EUR").with_for_update().first()

    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Impossibile recuperare il wallet EUR associato al tuo account")
    if withdrawal.amount > wallet.balance:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Stai cercando di prelevare più del tuo saldo attuale")
    wallet.balance -= withdrawal.amount

    #creo la transazione nella tabella orders
    order = models.Order(
        wallet_id = wallet.id,
        type = "WITHDRAWAL",
        asset = "EUR",
        amount = withdrawal.amount,
        price = "1",
        status = "COMPLETED"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.post("/trade", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderResponse)
def trade(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):


    current_price = utils.get_live_price(order.asset)
    
    #recupero il wallet dell'utente btc
    wallet_btc = db.query(models.Wallet).filter(models.Wallet.owner_id == current_user.id, models.Wallet.currency == "BTC").with_for_update().first()
    #recupero il wallet dell'utente eur
    wallet_eur = db.query(models.Wallet).filter(models.Wallet.owner_id == current_user.id, models.Wallet.currency == "EUR").with_for_update().first()

    if not wallet_eur or not wallet_btc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Impossibile recuperare uno dei wallet associato al tuo account")
    
    
    total = order.amount * current_price

    if order.type == "BUY":
        #se compra bisogna controllare che il suo wallet eur abbia fondi sufficienti
        if wallet_eur.balance < total:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Fondi insufficienti")
        #altrimenti puo comprare quindi scaliamo i fondi dal wallet euro 
        wallet_eur.balance -= total
        #e aggiungiamo i btc
        wallet_btc.balance += order.amount

    elif order.type == "SELL":
        #se vende bisogna controllare che abbia quei btc da vendere
        if wallet_btc.balance < order.amount:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Crypto insufficienti")
        #altrimenti puo vendere e scaliamo i btc
        wallet_btc.balance -= order.amount
        #aggiungiamo gli eur
        wallet_eur.balance += total
    
    #creiamo la transazione
    transaction = models.Order(**order.model_dump(),
                        wallet_id = wallet_btc.id,
                        price = current_price,
                        status = "COMPLETED")
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

