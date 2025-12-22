from sqlalchemy import Column, Integer, String
from db.database import Base


class DbUser(Base):
    __tablename__: str = 'user'
    id: Column[int] = Column(Integer, primary_key=True, index=True, comment='cest quoi un comment sur une collone d`une table')
    username: Column[str] = Column(String(40))
    email: Column[str] = Column(String(70))
    hashed_password: Column[str] = Column(String)