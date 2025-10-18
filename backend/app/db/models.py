from sqlalchemy import Column, String, Text, DateTime, func, Integer
from sqlalchemy.orm import declarative_base
from ..db.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String(120), nullable=True)
    parent_email = Column(String(200), nullable=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False, default="neutral")
    category = Column(String(50), nullable=False, default="Other")
    department = Column(String(50), nullable=False, default="Other")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)