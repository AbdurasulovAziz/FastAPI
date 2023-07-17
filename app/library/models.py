from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.account.models import User
from core.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    create_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)

    def _to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "create_date": self.create_date.isoformat(),
            "user_id": self.user_id,
        }
