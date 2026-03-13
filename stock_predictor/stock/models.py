from sqlalchemy import Integer, Time, Date, CHAR, DECIMAL, Column, PrimaryKeyConstraint
from stock_predictor.database.session import Base

class Stock(Base):
    __tablename__ = "stock"

    symbol = Column(CHAR(length=6), index=True, nullable=False)
    date_stamp = Column(Date, index=True, nullable=False)
    time_stamp = Column(Time)
    open = Column(DECIMAL(precision=18, scale=4), nullable=False)
    high = Column(DECIMAL(precision=18, scale=4), nullable=False)
    low = Column(DECIMAL(precision=18, scale=4), nullable=False)
    close = Column(DECIMAL(precision=18, scale=4), nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (PrimaryKeyConstraint(symbol, date_stamp),)
