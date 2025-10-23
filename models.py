from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from database import Base

class StringModel(Base):
    __tablename__ = "strings"

    id = Column(String, primary_key=True, index=True)  # sha256 hash
    value = Column(String, nullable=False, unique=True)
    properties = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
