from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

# CONFIGURAZIONE DEL POOL
# pool_size: Numero di connessioni mantenute aperte.
# max_overflow: Quante connessioni extra creare se il pool è pieno.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,       # 20 connessioni pronte
    max_overflow=20,    # fino a 40 sotto stress
    pool_timeout=30,    # timeout di 30 sec
    pool_recycle=1800,
    pool_pre_ping=True,  # verifica che la connessione sia disponibile prima di usarla
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()