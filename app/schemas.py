from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, conint
from datetime import datetime
from typing import List, Literal, Optional

class OrderCreate(BaseModel):
    type: Literal["BUY", "SELL"]
    asset: Literal["BTC"]
    amount: Decimal = Field(gt=0)

class OrderResponse(BaseModel):
    id: int
    wallet_id: int
    type: str
    asset: str
    amount: Decimal
    price: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes = True)

class DepositCreate(BaseModel):
    amount: Decimal = Field(gt=0)

class WithdrawalCreate(BaseModel):
    amount: Decimal = Field(gt=0)

class WalletResponse(BaseModel):
    id: int
    owner_id: int 
    currency: str
    balance: Decimal
    created_at: datetime

    #orders: List[OrderResponse] = []

    model_config = ConfigDict(
        from_attributes = True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #wallets: List[WalletResponse] = []

    model_config = ConfigDict(
        from_attributes = True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


