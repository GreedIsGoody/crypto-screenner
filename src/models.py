from datetime import datetime
from sqlalchemy  import String, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class Coin(Base):
    __tablename__= 'coins'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    coingecko_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ticker: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    prices: Mapped[list["CoinPrice"]] = relationship(
        back_populates="coin",
        cascade="all, delete-orphan"
    )
    
    
class CoinPrice(Base):
    __tablename__ = "coin_prices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id", ondelete="CASCADE"))
    
    price_usd: Mapped[float] = mapped_column(Numeric(precision=16, scale=4), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    coin: Mapped["Coin"] = relationship(back_populates="prices")