from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config
from app.sqla.models import Base  # Assuming you have a Base model

# Create a synchronous engine
engine = create_engine(config.sqla_engine, echo=True)

# Create a sessionmaker bound to the synchronous engine
SessionLocal = sessionmaker(
    bind=engine,
    class_=sessionmaker,
    expire_on_commit=False,
)
