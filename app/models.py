from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, Numeric, String, Boolean, text, ForeignKey, Double
from sqlalchemy.orm import relationship

#impostazione tabelle:
#tabella utenti con id, email, password, created_at
#tabella wallet con id, owner_id, currency, balance, created_at
#tabella order con id, wallet_id, type(buy,sell), amount, price, status, created_at

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    wallets = relationship("Wallet", back_populates="owner")

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    currency = Column(String, nullable=False)
    balance = Column(Numeric(18, 8), nullable=False, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner = relationship("User", back_populates="wallets")
    orders = relationship("Order", back_populates="wallet")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    asset = Column(String, nullable=False)
    amount = Column(Numeric(18, 8), nullable=False)
    price = Column(Numeric(18, 8), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    wallet = relationship("Wallet", back_populates="orders")