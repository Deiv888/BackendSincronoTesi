import time
import random
from passlib.context import CryptContext
from decimal import Decimal, InvalidOperation

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(password_inserita, hashed_password):
    return pwd_context.verify(password_inserita, hashed_password)

def get_live_price(asset: str) -> Decimal:

    time.sleep(0.2) 
    
    if asset == "BTC":
        # Prezzo base 45000 + variazione casuale
        return Decimal(45000 + random.randint(-100, 100))
    
    raise ValueError(f"Asset '{asset}' non supportato dal sistema") 
