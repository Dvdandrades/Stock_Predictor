from sqlalchemy import Integer, Time, Date, CHAR, DECIMAL, Column, PrimaryKeyConstraint
from stock_predictor.database.session import Base

class Stock(Base):
    __tablename__ = "stock"

    symbol = Column(CHAR(length=6), index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    time = Column(Time)
    open = Column(DECIMAL(precision=18, scale=4))
    high = Column(DECIMAL(precision=18, scale=4))
    low = Column(DECIMAL(precision=18, scale=4))
    close = Column(DECIMAL(precision=18, scale=4), nullable=False)
    volume = Column(Integer)

    __table_args__ = (PrimaryKeyConstraint(symbol, date),)
    
    